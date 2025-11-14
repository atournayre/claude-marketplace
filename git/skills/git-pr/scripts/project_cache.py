#!/usr/bin/env python3
"""Module de cache pour projets GitHub"""

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


CACHE_DIR = Path(".claude/cache")
CACHE_FILE = CACHE_DIR / "git-projects.json"


class ProjectCache:
    """Gestion cache projets"""

    def __init__(self):
        self.cache = self.load()

    def load(self) -> dict:
        """Charge cache depuis fichier"""
        if not CACHE_FILE.exists():
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            return {"updated_at": None, "projects": []}
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {"updated_at": None, "projects": []}

    def save(self):
        """Sauvegarde cache vers fichier"""
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self.cache["updated_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, indent=2, ensure_ascii=False)

    def find(self, query: str) -> Optional[dict]:
        """Cherche projet par titre exact ou alias (case-insensitive)"""
        query_lower = query.lower()
        for project in self.cache.get("projects", []):
            if project["title"].lower() == query_lower:
                return project
            if query_lower in [alias.lower() for alias in project.get("aliases", [])]:
                return project
        return None

    def add(self, project: dict):
        """Ajoute projet au cache avec génération aliases"""
        aliases = self.generate_aliases(project["title"])
        project["aliases"] = aliases
        existing = [p for p in self.cache.get("projects", []) if p["id"] == project["id"]]
        if not existing:
            if "projects" not in self.cache:
                self.cache["projects"] = []
            self.cache["projects"].append(project)
        self.save()

    def generate_aliases(self, title: str) -> list[str]:
        """Génère aliases depuis titre

        Exemples:
        - "Project Alpha" → ["project", "alpha"]
        - "Sprint 2024-Q1" → ["sprint", "2024", "q1"]
        - "Bug Tracking" → ["bug", "tracking"]

        Logique: extraire mots-clés significatifs
        """
        aliases = []
        words = re.findall(r'[\w]+', title.lower())
        for word in words:
            if len(word) >= 2 and word not in ['the', 'and', 'for']:
                aliases.append(word)
        return list(set(aliases))

    def refresh_from_api(self, projects: list[dict]):
        """Remplace cache entièrement avec données API"""
        enriched = []
        for project in projects:
            aliases = self.generate_aliases(project["title"])
            enriched.append({
                "id": project["id"],
                "title": project["title"],
                "number": project.get("number"),
                "aliases": aliases
            })
        self.cache["projects"] = enriched
        self.save()

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
                repo_full = match.group(1)
                owner, _ = repo_full.split('/')
                return owner
            raise ValueError(f"Format URL invalide: {url}")
        except Exception as e:
            print(f"❌ Erreur récupération repo: {e}", file=sys.stderr)
            raise
