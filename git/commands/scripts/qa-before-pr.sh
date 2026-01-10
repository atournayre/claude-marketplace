#!/bin/bash
set -e

echo "🔍 Exécution QA complète avant création PR..."

# Détection automatique des outils disponibles
ERRORS=0

# 1. PHPStan (plusieurs méthodes possibles)
if [ -f "Makefile" ] && grep -q "^phpstan:" Makefile; then
  echo "▶️  PHPStan (via make)..."
  make phpstan || ERRORS=$((ERRORS+1))
elif [ -f "vendor/bin/phpstan" ]; then
  echo "▶️  PHPStan (via vendor/bin)..."
  vendor/bin/phpstan analyse || ERRORS=$((ERRORS+1))
elif [ -f "composer.json" ] && grep -q "phpstan" composer.json; then
  echo "▶️  PHPStan (via composer)..."
  composer phpstan || ERRORS=$((ERRORS+1))
else
  echo "⚠️  PHPStan non détecté, ignoré"
fi

# 2. Tests unitaires (plusieurs méthodes)
if [ -f "Makefile" ] && grep -q "^test:" Makefile; then
  echo "▶️  Tests (via make)..."
  make test || ERRORS=$((ERRORS+1))
elif [ -f "vendor/bin/phpunit" ]; then
  echo "▶️  Tests (via PHPUnit)..."
  vendor/bin/phpunit || ERRORS=$((ERRORS+1))
elif [ -f "composer.json" ] && grep -q "\"test\"" composer.json; then
  echo "▶️  Tests (via composer)..."
  composer test || ERRORS=$((ERRORS+1))
else
  echo "⚠️  Tests non détectés, ignoré"
fi

# 3. Linting/Formatage (optionnel)
if [ -f "Makefile" ] && grep -q "^lint:" Makefile; then
  echo "▶️  Lint (via make)..."
  make lint || ERRORS=$((ERRORS+1))
elif [ -f "vendor/bin/php-cs-fixer" ]; then
  echo "▶️  PHP-CS-Fixer (dry-run)..."
  vendor/bin/php-cs-fixer fix --dry-run --diff || ERRORS=$((ERRORS+1))
fi

# 4. Build (si applicable)
if [ -f "Makefile" ] && grep -q "^build:" Makefile; then
  echo "▶️  Build (via make)..."
  make build || ERRORS=$((ERRORS+1))
fi

# Résumé
echo ""
if [ $ERRORS -eq 0 ]; then
  echo "✅ QA passée avec succès"
  exit 0
else
  echo "❌ QA échouée : $ERRORS erreur(s) détectée(s)"
  exit 1
fi
