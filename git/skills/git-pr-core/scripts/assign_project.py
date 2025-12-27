#!/usr/bin/env python3
"""
Assigner PR à projet GitHub
Usage: assign_project.py <pr_number> [--project <name>]
Output: Projet assigné ou "ignored" (stdout)
"""

import argparse
import json
import subprocess
import sys
import re
from project_cache import ProjectCache


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
        match = re.search(r'github\.com[:/](.+/.+?)(?:\.git)?$', url)
        if match:
            repo_full = match.group(1)
            owner, repo = repo_full.split('/')
            return owner, repo
        raise ValueError(f"Format URL invalide: {url}")
    except Exception as e:
        print(f"❌ Erreur récupération repo: {e}", file=sys.stderr)
        sys.exit(1)


def get_projects_list(owner):
    """Récupère les projets via gh project list"""
    try:
        result = subprocess.run(
            ["gh", "project", "list", "--owner", owner, "--format", "json"],
            capture_output=True,
            text=True,
            check=True
        )
        projects_data = json.loads(result.stdout)
        projects = []
        for project in projects_data.get('projects', []):
            projects.append({
                'id': project.get('id'),
                'title': project.get('title'),
                'number': project.get('number')
            })
        return projects
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Impossible de récupérer les projets: {e.stderr}", file=sys.stderr)
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Erreur parsing JSON projets: {e}", file=sys.stderr)
        return []


def get_projects_cached(owner):
    """Récupère projets avec cache"""
    cache = ProjectCache()
    if not cache.cache.get("projects"):
        projects = get_projects_list(owner)
        cache.refresh_from_api(projects)
        return projects
    return cache.cache["projects"]


def find_project(owner, query):
    """Cherche projet par query (exact ou alias)"""
    cache = ProjectCache()
    result = cache.find(query)
    if result:
        return result
    projects = get_projects_list(owner)
    cache.refresh_from_api(projects)
    return cache.find(query)




def assign_pr_to_project(pr_number, project_id, owner, repo):
    """Assigne la PR au projet via GraphQL"""
    # Récupérer l'ID de la PR
    try:
        pr_result = subprocess.run(
            ["gh", "pr", "view", str(pr_number), "--json", "id"],
            capture_output=True,
            text=True,
            check=True
        )
        pr_data = json.loads(pr_result.stdout)
        pr_id = pr_data['id']
    except Exception as e:
        print(f"❌ Erreur récupération ID PR: {e}", file=sys.stderr)
        return False

    # Ajouter la PR au projet
    mutation = """
    mutation($projectId: ID!, $contentId: ID!) {
      addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
        item {
          id
        }
      }
    }
    """

    try:
        subprocess.run(
            ["gh", "api", "graphql",
             "-f", f"query={mutation}",
             "-f", f"projectId={project_id}",
             "-f", f"contentId={pr_id}"],
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur assignation projet: {e.stderr}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Assigne une PR à un projet GitHub")
    parser.add_argument("pr_number", type=int, help="Numéro de la PR")
    parser.add_argument("--project", help="Nom du projet à assigner")
    args = parser.parse_args()

    owner, repo = get_repo_info()
    projects = get_projects_cached(owner)

    if not projects:
        print("ℹ️  Aucun projet trouvé - ignoré")
        print("ignored")
        sys.exit(0)

    # Si --project fourni, utiliser find_project pour recherche intelligente
    if args.project:
        try:
            project = find_project(owner, args.project)
            if not project:
                print(f"❌ Projet '{args.project}' non trouvé", file=sys.stderr)
                available = [p['title'] for p in projects]
                print(f"Projets disponibles: {', '.join(available)}", file=sys.stderr)
                sys.exit(1)

            if assign_pr_to_project(args.pr_number, project['id'], owner, repo):
                print(f"✅ Projet '{project['title']}' assigné")
                print(project['title'])
                sys.exit(0)
            else:
                sys.exit(1)
        except Exception as e:
            print(f"❌ Erreur: {e}", file=sys.stderr)
            sys.exit(1)

    # Sinon, retourner JSON pour AskUserQuestion
    projects_list = [
        {
            "id": p["id"],
            "title": p["title"],
            "number": p.get("number")
        }
        for p in projects
    ]

    output = {
        "projects": projects_list,
        "needs_user_input": True
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
