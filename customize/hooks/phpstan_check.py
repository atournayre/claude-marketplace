#!/usr/bin/env python3
"""
Hook PostToolUse pour vérifier les erreurs PHPStan et les annotations
de suppression après chaque édition de fichier PHP.

Informatif uniquement (exit 0 toujours).
S'active uniquement dans les projets PHP où PHPStan est installé.
"""

import json
import os
import subprocess
import sys


def main():
    try:
        input_data = json.load(sys.stdin)

        tool_input = input_data.get("tool_input", {})

        # Extraire le chemin du fichier modifié
        file_path = tool_input.get("file_path", "")

        # Vérifier si c'est un fichier PHP
        if not file_path.endswith(".php"):
            sys.exit(0)

        # Vérifier si PHPStan est installé dans le projet
        phpstan_bin = os.path.join(os.getcwd(), "vendor", "bin", "phpstan")
        if not os.path.isfile(phpstan_bin):
            sys.exit(0)

        # Vérifier les annotations @phpstan-ignore dans le fichier
        try:
            with open(file_path, "r") as f:
                content = f.read()

            suppressions = []
            for i, line in enumerate(content.splitlines(), 1):
                if "@phpstan-ignore" in line:
                    suppressions.append(f"  L{i}: {line.strip()}")

            if suppressions:
                print(
                    f"⚠️  Annotations @phpstan-ignore détectées dans {os.path.basename(file_path)}:",
                    file=sys.stderr,
                )
                for s in suppressions:
                    print(s, file=sys.stderr)
        except (OSError, IOError):
            pass

        # Lancer PHPStan sur le fichier modifié
        try:
            result = subprocess.run(
                [phpstan_bin, "analyse", "--no-progress", "--error-format=raw", file_path],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode != 0 and result.stdout.strip():
                errors = result.stdout.strip().splitlines()
                print(
                    f"⚠️  PHPStan: {len(errors)} erreur(s) dans {os.path.basename(file_path)}:",
                    file=sys.stderr,
                )
                for error in errors[:5]:
                    print(f"  {error}", file=sys.stderr)
                if len(errors) > 5:
                    print(f"  ... et {len(errors) - 5} autres", file=sys.stderr)
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
            pass

        # Toujours exit 0 (informatif, pas bloquant)
        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception:
        sys.exit(0)


if __name__ == "__main__":
    main()
