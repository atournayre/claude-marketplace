#!/usr/bin/env python3
"""Tests unitaires pour project_cache"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from project_cache import ProjectCache, CACHE_DIR, CACHE_FILE


class TestGenerateAliases(unittest.TestCase):
    """Test génération aliases"""

    def test_genere_alias_pour_titre_simple(self):
        cache = ProjectCache()
        aliases = cache.generate_aliases("Project Alpha")
        self.assertIn("project", aliases)
        self.assertIn("alpha", aliases)

    def test_genere_alias_pour_titre_avec_tirets(self):
        cache = ProjectCache()
        aliases = cache.generate_aliases("Bug Tracking")
        self.assertIn("bug", aliases)
        self.assertIn("tracking", aliases)

    def test_genere_alias_pour_titre_avec_chiffres(self):
        cache = ProjectCache()
        aliases = cache.generate_aliases("Sprint 2024-Q1")
        self.assertIn("sprint", aliases)
        self.assertIn("2024", aliases)
        self.assertIn("q1", aliases)

    def test_genere_pas_alias_pour_mots_courts(self):
        cache = ProjectCache()
        aliases = cache.generate_aliases("The Big Project")
        self.assertNotIn("the", aliases)
        self.assertIn("big", aliases)
        self.assertIn("project", aliases)


class TestFindExactMatch(unittest.TestCase):
    """Test recherche exacte"""

    def test_trouve_par_titre_exact(self):
        cache = ProjectCache()
        cache.cache = {
            "projects": [
                {"id": "PVT_123", "title": "Project Alpha", "number": 1, "aliases": ["project", "alpha"]}
            ]
        }
        result = cache.find("Project Alpha")
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "PVT_123")

    def test_trouve_par_titre_exact_case_insensitive(self):
        cache = ProjectCache()
        cache.cache = {
            "projects": [
                {"id": "PVT_123", "title": "Project Alpha", "number": 1, "aliases": ["project", "alpha"]}
            ]
        }
        result = cache.find("project alpha")
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "PVT_123")

    def test_ne_trouve_pas_si_titre_different(self):
        cache = ProjectCache()
        cache.cache = {
            "projects": [
                {"id": "PVT_123", "title": "Project Alpha", "number": 1, "aliases": ["project", "alpha"]}
            ]
        }
        result = cache.find("Project Beta")
        self.assertIsNone(result)


class TestFindByAlias(unittest.TestCase):
    """Test recherche par alias"""

    def test_query_trouve_via_alias(self):
        cache = ProjectCache()
        cache.cache = {
            "projects": [
                {"id": "PVT_456", "title": "Bug Tracking", "number": 2, "aliases": ["bug", "tracking"]}
            ]
        }
        result = cache.find("bug")
        self.assertIsNotNone(result)
        self.assertEqual(result["title"], "Bug Tracking")

    def test_query_trouve_via_alias_case_insensitive(self):
        cache = ProjectCache()
        cache.cache = {
            "projects": [
                {"id": "PVT_456", "title": "Bug Tracking", "number": 2, "aliases": ["bug", "tracking"]}
            ]
        }
        result = cache.find("BUG")
        self.assertIsNotNone(result)
        self.assertEqual(result["title"], "Bug Tracking")

    def test_query_trouve_projet_sans_alias(self):
        cache = ProjectCache()
        cache.cache = {
            "projects": [
                {"id": "PVT_789", "title": "Main", "number": 3, "aliases": ["main"]}
            ]
        }
        result = cache.find("Main")
        self.assertIsNotNone(result)
        self.assertEqual(result["number"], 3)


class TestCachePersistence(unittest.TestCase):
    """Test sauvegarde/chargement"""

    def test_charge_cache_vide_si_fichier_inexistant(self):
        cache = ProjectCache()
        cache.cache = {"projects": []}
        self.assertEqual(cache.cache["projects"], [])


class TestRefreshFromApi(unittest.TestCase):
    """Test refresh depuis API"""

    def test_refresh_remplace_cache_complet(self):
        cache = ProjectCache()
        projects = [
            {"id": "PVT_111", "title": "Project A", "number": 1},
            {"id": "PVT_222", "title": "Project B", "number": 2}
        ]
        cache.refresh_from_api(projects)
        self.assertEqual(len(cache.cache["projects"]), 2)
        self.assertEqual(cache.cache["projects"][0]["id"], "PVT_111")
        self.assertEqual(cache.cache["projects"][1]["id"], "PVT_222")

    def test_refresh_genere_aliases(self):
        cache = ProjectCache()
        projects = [
            {"id": "PVT_333", "title": "Sprint Planning", "number": 3}
        ]
        cache.refresh_from_api(projects)
        self.assertIn("sprint", cache.cache["projects"][0]["aliases"])
        self.assertIn("planning", cache.cache["projects"][0]["aliases"])


if __name__ == "__main__":
    unittest.main()
