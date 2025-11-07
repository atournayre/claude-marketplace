#!/usr/bin/env python3
"""Tests unitaires pour milestone_cache"""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from milestone_cache import MilestoneCache, CACHE_DIR, CACHE_FILE


class TestNormalizeSemver(unittest.TestCase):
    """Test normalisation semver"""

    def test_normalise_un_chiffre_ajoute_zero_zero(self):
        cache = MilestoneCache()
        self.assertEqual(cache.normalize_semver("26"), "26.0.0")

    def test_normalise_deux_chiffres_ajoute_zero(self):
        cache = MilestoneCache()
        self.assertEqual(cache.normalize_semver("26.1"), "26.1.0")

    def test_normalise_trois_chiffres_reste_identique(self):
        cache = MilestoneCache()
        self.assertEqual(cache.normalize_semver("26.1.1"), "26.1.1")

    def test_normalise_conserve_suffixe(self):
        cache = MilestoneCache()
        self.assertEqual(cache.normalize_semver("26.0.0 (Avenant)"), "26.0.0 (Avenant)")


class TestGenerateAliases(unittest.TestCase):
    """Test génération aliases stricte"""

    def test_genere_alias_pour_titre_avec_parentheses(self):
        cache = MilestoneCache()
        self.assertEqual(cache.generate_aliases("26.1.1 (Hotfix)"), ["26.1.1"])

    def test_genere_alias_pour_titre_avec_avenant(self):
        cache = MilestoneCache()
        self.assertEqual(cache.generate_aliases("26.0.0 (Avenant)"), ["26.0.0"])

    def test_genere_pas_alias_pour_titre_sans_parentheses(self):
        cache = MilestoneCache()
        self.assertEqual(cache.generate_aliases("26.1.0"), [])

    def test_genere_pas_alias_pour_titre_non_semver(self):
        cache = MilestoneCache()
        self.assertEqual(cache.generate_aliases("Release Candidate"), [])


class TestFindExactMatch(unittest.TestCase):
    """Test recherche exacte"""

    def test_trouve_par_titre_exact(self):
        cache = MilestoneCache()
        cache.cache = {
            "milestones": [
                {"number": 42, "title": "26.0.0 (Avenant)", "aliases": ["26.0.0"]}
            ]
        }
        result = cache.find("26.0.0 (Avenant)")
        self.assertIsNotNone(result)
        self.assertEqual(result["number"], 42)

    def test_ne_trouve_pas_si_titre_different(self):
        cache = MilestoneCache()
        cache.cache = {
            "milestones": [
                {"number": 42, "title": "26.0.0 (Avenant)", "aliases": ["26.0.0"]}
            ]
        }
        result = cache.find("27.0.0")
        self.assertIsNone(result)


class TestFindByAlias(unittest.TestCase):
    """Test recherche par alias"""

    def test_query_trouve_via_alias(self):
        cache = MilestoneCache()
        cache.cache = {
            "milestones": [
                {"number": 43, "title": "26.1.1 (Hotfix)", "aliases": ["26.1.1"]}
            ]
        }
        result = cache.find("26.1.1")
        self.assertIsNotNone(result)
        self.assertEqual(result["title"], "26.1.1 (Hotfix)")

    def test_query_trouve_milestone_sans_parentheses(self):
        cache = MilestoneCache()
        cache.cache = {
            "milestones": [
                {"number": 44, "title": "26.1.0", "aliases": []}
            ]
        }
        result = cache.find("26.1.0")
        self.assertIsNotNone(result)
        self.assertEqual(result["number"], 44)


class TestNoCollisionMatch(unittest.TestCase):
    """Test pas de collision entre versions"""

    def test_query_partielle_ne_trouve_pas_version_complete(self):
        cache = MilestoneCache()
        cache.cache = {
            "milestones": [
                {"number": 43, "title": "26.1.1 (Hotfix)", "aliases": ["26.1.1"]}
            ]
        }
        result = cache.find("26.1")
        self.assertIsNone(result)

    def test_query_majeure_ne_trouve_pas_version_mineure(self):
        cache = MilestoneCache()
        cache.cache = {
            "milestones": [
                {"number": 42, "title": "26.0.0 (Avenant)", "aliases": ["26.0.0"]}
            ]
        }
        result = cache.find("26")
        self.assertIsNone(result)


class TestFindWithNormalization(unittest.TestCase):
    """Test recherche avec normalisation"""

    def test_query_normalisee_trouve_milestone(self):
        cache = MilestoneCache()
        cache.cache = {
            "milestones": [
                {"number": 44, "title": "26.1.0", "aliases": []}
            ]
        }
        normalized = cache.normalize_semver("26.1")
        result = cache.find(normalized)
        self.assertIsNotNone(result)
        self.assertEqual(result["title"], "26.1.0")

    def test_query_majeure_normalisee_trouve_avenant(self):
        cache = MilestoneCache()
        cache.cache = {
            "milestones": [
                {"number": 42, "title": "26.0.0 (Avenant)", "aliases": ["26.0.0"]}
            ]
        }
        normalized = cache.normalize_semver("26")
        result = cache.find(normalized)
        self.assertIsNotNone(result)
        self.assertEqual(result["title"], "26.0.0 (Avenant)")


class TestCachePersistence(unittest.TestCase):
    """Test sauvegarde/chargement"""

    def test_charge_cache_vide_si_fichier_inexistant(self):
        cache = MilestoneCache()
        cache.cache = {"milestones": []}
        self.assertEqual(cache.cache["milestones"], [])


class TestCreateMilestone(unittest.TestCase):
    """Test création milestone inexistant"""

    @patch('milestone_cache.subprocess.run')
    def test_cree_milestone_via_api(self, mock_run):
        mock_run.side_effect = [
            MagicMock(stdout="git@github.com:owner/repo.git\n"),
            MagicMock(stdout='{"number": 50, "title": "99.0.0"}')
        ]
        cache = MilestoneCache()
        result = cache.create("99.0.0")
        self.assertEqual(result["number"], 50)
        self.assertEqual(result["title"], "99.0.0")


class TestCreateWithNormalization(unittest.TestCase):
    """Test création avec normalisation semver"""

    @patch('milestone_cache.subprocess.run')
    def test_cree_milestone_normalise_depuis_majeure(self, mock_run):
        mock_run.side_effect = [
            MagicMock(stdout="git@github.com:owner/repo.git\n"),
            MagicMock(stdout='{"number": 51, "title": "26.0.0"}')
        ]
        cache = MilestoneCache()
        normalized = cache.normalize_semver("26")
        result = cache.create(normalized)
        self.assertEqual(result["title"], "26.0.0")

    @patch('milestone_cache.subprocess.run')
    def test_cree_milestone_normalise_depuis_mineure(self, mock_run):
        mock_run.side_effect = [
            MagicMock(stdout="git@github.com:owner/repo.git\n"),
            MagicMock(stdout='{"number": 52, "title": "26.1.0"}')
        ]
        cache = MilestoneCache()
        normalized = cache.normalize_semver("26.1")
        result = cache.create(normalized)
        self.assertEqual(result["title"], "26.1.0")


if __name__ == "__main__":
    unittest.main()
