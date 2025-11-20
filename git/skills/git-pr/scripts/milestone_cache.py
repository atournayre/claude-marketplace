#!/usr/bin/env python3
"""Module de cache pour milestones GitHub"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


CACHE_DIR = Path(".claude/cache")
CACHE_FILE = CACHE_DIR / "git-milestones.json"


class MilestoneCache:
    """Gestion cache milestones"""

    def __init__(self):
        self.cache = self.load()

    def load(self) -> dict:
        """Charge cache depuis fichier"""
        if not CACHE_FILE.exists():
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            return {"updated_at": None, "milestones": []}
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {"updated_at": None, "milestones": []}

    def save(self):
        """Sauvegarde cache vers fichier"""
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self.cache["updated_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, indent=2, ensure_ascii=False)

    def find(self, query: str) -> Optional[dict]:
        """Cherche milestone par titre exact ou alias"""
        for milestone in self.cache.get("milestones", []):
            if milestone["title"] == query:
                return milestone
            if query in milestone.get("aliases", []):
                return milestone
        return None

    def add(self, milestone: dict):
        """Ajoute milestone au cache avec génération aliases"""
        aliases = self.generate_aliases(milestone["title"])
        milestone["aliases"] = aliases
        existing = [m for m in self.cache.get("milestones", []) if m["number"] == milestone["number"]]
        if not existing:
            if "milestones" not in self.cache:
                self.cache["milestones"] = []
            self.cache["milestones"].append(milestone)
        self.save()

    def generate_aliases(self, title: str) -> list[str]:
        """Génère aliases depuis titre (version exacte + formes courtes)

        Exemples:
        - "26.1.1 (Hotfix)" → ["26.1.1", "26.1", "26"]
        - "26.1.0" → ["26.1.0", "26.1", "26"]
        - "26.0.0 (Avenant)" → ["26.0.0", "26.0", "26"]

        Logique: extraire version semver et générer formes courtes
        """
        match = re.match(r'^(\d+)\.(\d+)\.(\d+)', title)
        if match:
            major, minor, patch = match.groups()
            aliases = []
            full_version = f"{major}.{minor}.{patch}"
            if full_version != title:
                aliases.append(full_version)
            aliases.append(f"{major}.{minor}")
            aliases.append(major)
            return aliases
        return []

    def refresh_from_api(self, milestones: list[dict]):
        """Remplace cache entièrement avec données API"""
        enriched = []
        for milestone in milestones:
            aliases = self.generate_aliases(milestone["title"])
            enriched.append({
                "number": milestone["number"],
                "title": milestone["title"],
                "aliases": aliases
            })
        self.cache["milestones"] = enriched
        self.save()

    def create(self, title: str) -> dict:
        """Crée milestone sur GitHub via API et l'ajoute au cache

        Récupère repo via get_repo_info()
        gh api repos/{repo}/milestones -f title="99.0.0" -f state="open"
        Retourne: {"number": 43, "title": "99.0.0", ...}
        """
        repo = self.get_repo_info()
        try:
            result = subprocess.run(
                ["gh", "api", f"repos/{repo}/milestones", "-f", f"title={title}", "-f", "state=open"],
                capture_output=True,
                text=True,
                check=True
            )
            milestone = json.loads(result.stdout)
            self.add(milestone)
            return milestone
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur création milestone: {e.stderr}", file=sys.stderr)
            raise
        except json.JSONDecodeError as e:
            print(f"❌ Erreur parsing JSON: {e}", file=sys.stderr)
            raise

    def get_repo_info(self) -> str:
        """Récupère owner/repo depuis git remote"""
        try:
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                capture_output=True,
                text=True,
                check=True
            )
            url = result.stdout.strip()
            match = re.search(r'github\.com[:/](.+/.+?)(?:\.git)?$', url)
            if match:
                return match.group(1)
            raise ValueError(f"Format URL invalide: {url}")
        except Exception as e:
            print(f"❌ Erreur récupération repo: {e}", file=sys.stderr)
            raise

    def normalize_semver(self, version: str) -> str:
        """Normalise version en semver complet

        Exemples:
        - "26" → "26.0.0"
        - "26.1" → "26.1.0"
        - "26.1.1" → "26.1.1"
        - "26.0.0 (Avenant)" → "26.0.0 (Avenant)" (conserve suffixe)
        """
        match = re.match(r'^(\d+)(?:\.(\d+))?(?:\.(\d+))?(.*)?$', version)
        if not match:
            return version
        major = match.group(1)
        minor = match.group(2) or "0"
        patch = match.group(3) or "0"
        suffix = match.group(4) or ""
        return f"{major}.{minor}.{patch}{suffix}"
