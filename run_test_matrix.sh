#!/usr/bin/env bash
set -euo pipefail

MATRIX=(
  "3.13 5.0"   # Python 3.13 + Django 5.0.x
  "3.9 4.2"    # Python 3.9  + Django 4.2.x
  "3.9 3.2"    # Python 3.9  + Django 3.2.x
)

echo "== Running test matrix with Pipenv =="

for entry in "${MATRIX[@]}"; do
  PY_VER=$(echo "$entry" | awk '{print $1}')
  DJANGO_VER=$(echo "$entry" | awk '{print $2}')

  echo "=============================================="
  echo "→ Python ${PY_VER} / Django ${DJANGO_VER}"
  echo "=============================================="

  export PIPENV_PYTHON="python${PY_VER}"

  pipenv --rm >/dev/null 2>&1 || true

  pipenv install --dev "django~=${DJANGO_VER}" coverage ruff

  pipenv run coverage run manage.py test tests
  pipenv run coverage report
done

cat <<'EOF'

NOTE:
- Pour respecter strictement l'énoncé (Python 2.7), il faudrait une version de Django
  plus ancienne (Django 1.11.x), car Django 3+ ne supporte pas Python 2.7.
- L'application actuelle utilise 'path()' dans urls.py (introduit en Django 2.0),
  elle n'est donc pas directement compatible avec Django 1.x sans adaptation.

EOF
