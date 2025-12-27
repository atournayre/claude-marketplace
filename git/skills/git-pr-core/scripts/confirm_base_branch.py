#!/usr/bin/env python3
"""
Détecte les branches disponibles et gère la confirmation
Usage: confirm_base_branch.py [--branch <name>]
Output: Nom branche validé (stdout) ou JSON options
"""

import argparse
import json
import subprocess
import sys
import re


def get_remote_branches():
    """Récupère les branches remote et filtre develop/main/master/release/*"""
    try:
        result = subprocess.run(
            ["git", "branch", "-r"],
            capture_output=True,
            text=True,
            check=True
        )

        branches = []
        for line in result.stdout.strip().split('\n'):
            branch = line.strip()
            # Retirer origin/
            branch = re.sub(r'^origin/', '', branch)
            # Ignorer HEAD
            if 'HEAD' in branch:
                continue
            # Filtrer develop/main/master/release/*/hotfix/*
            if branch in ['develop', 'main', 'master'] or branch.startswith('release/') or branch.startswith('hotfix/'):
                branches.append(branch)

        return sorted(set(branches))
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la récupération des branches: {e}", file=sys.stderr)
        sys.exit(1)


def validate_branch(branch_name, available_branches):
    """Valide qu'une branche existe"""
    if branch_name in available_branches:
        return True
    print(f"❌ Branche '{branch_name}' non trouvée", file=sys.stderr)
    print(f"Branches disponibles: {', '.join(available_branches)}", file=sys.stderr)
    return False


def main():
    parser = argparse.ArgumentParser(description="Confirme la branche de base pour la PR")
    parser.add_argument("--branch", help="Nom de la branche de base")
    args = parser.parse_args()

    branches = get_remote_branches()

    if not branches:
        print("❌ Aucune branche develop/main/master/release/hotfix trouvée", file=sys.stderr)
        sys.exit(1)

    # Si --branch fourni, valider et retourner
    if args.branch:
        if validate_branch(args.branch, branches):
            print(args.branch)
            sys.exit(0)
        else:
            sys.exit(1)

    # Sinon, retourner JSON pour AskUserQuestion
    suggested = "develop" if "develop" in branches else branches[0]

    output = {
        "branches": branches,
        "suggested": suggested,
        "needs_user_input": True
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
