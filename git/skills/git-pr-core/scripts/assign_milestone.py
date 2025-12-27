#!/usr/bin/env python3
"""
Lister milestones et gérer assignation
Usage: assign_milestone.py <pr_number> [--milestone <name>]
Output: Milestone assigné ou "ignored" (stdout)
"""

import argparse
import json
import subprocess
import sys
import re
from milestone_cache import MilestoneCache


def get_repo_info():
    """Récupère owner/repo depuis git remote"""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            check=True
        )
        url = result.stdout.strip()
        # Extraire owner/repo depuis URL GitHub
        match = re.search(r'github\.com[:/](.+/.+?)(?:\.git)?$', url)
        if match:
            return match.group(1)
        raise ValueError(f"Format URL invalide: {url}")
    except Exception as e:
        print(f"❌ Erreur récupération repo: {e}", file=sys.stderr)
        sys.exit(1)


def get_open_milestones(repo):
    """Récupère les milestones ouverts via gh API"""
    try:
        result = subprocess.run(
            ["gh", "api", f"repos/{repo}/milestones", "--jq",
             "[.[] | select(.state == \"open\") | {number, title}]"],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur récupération milestones: {e.stderr}", file=sys.stderr)
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Erreur parsing JSON milestones: {e}", file=sys.stderr)
        return []


def get_open_milestones_cached(repo):
    """Récupère milestones avec cache"""
    cache = MilestoneCache()
    if not cache.cache.get("milestones"):
        milestones = get_open_milestones(repo)
        cache.refresh_from_api(milestones)
        return milestones
    return cache.cache["milestones"]


def find_milestone(repo, query):
    """Cherche milestone par query (exact ou partiel)"""
    cache = MilestoneCache()
    result = cache.find(query)
    if result:
        return result
    normalized = cache.normalize_semver(query)
    result = cache.find(normalized)
    if result:
        return result
    milestones = get_open_milestones(repo)
    cache.refresh_from_api(milestones)
    result = cache.find(normalized)
    if result:
        return result
    return cache.create(normalized)


def assign_milestone(pr_number, milestone_title):
    """Assigne un milestone à la PR"""
    try:
        subprocess.run(
            ["gh", "pr", "edit", str(pr_number), "--milestone", milestone_title],
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur assignation milestone: {e.stderr}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Assigne un milestone à une PR")
    parser.add_argument("pr_number", type=int, help="Numéro de la PR")
    parser.add_argument("--milestone", help="Nom du milestone à assigner")
    args = parser.parse_args()

    repo = get_repo_info()
    milestones = get_open_milestones_cached(repo)

    if not milestones:
        print("ℹ️  Aucun milestone ouvert - ignoré")
        print("ignored")
        sys.exit(0)

    # Si --milestone fourni, utiliser find_milestone pour recherche intelligente
    if args.milestone:
        try:
            milestone = find_milestone(repo, args.milestone)
            if assign_milestone(args.pr_number, milestone['title']):
                print(f"✅ Milestone '{milestone['title']}' assigné")
                print(milestone['title'])
                sys.exit(0)
            else:
                sys.exit(1)
        except Exception as e:
            print(f"❌ Erreur: {e}", file=sys.stderr)
            sys.exit(1)

    # Sinon, retourner JSON pour AskUserQuestion
    # Suggérer le premier milestone (généralement le plus récent)
    milestones_with_suggestion = [
        {
            "number": m["number"],
            "title": m["title"],
            "is_suggested": i == 0
        }
        for i, m in enumerate(milestones)
    ]

    output = {
        "milestones": milestones_with_suggestion,
        "needs_user_input": True
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
