#!/usr/bin/env bash
set -euo pipefail

# ---- Config ----
APP_NAME="todolist"
SETTINGS_FILE="todo/settings.py"

# ---- Parse arguments ----
if [ "$#" -lt 1 ]; then
  echo "Usage: ./build.sh version=X.Y.Z"
  exit 1
fi

case "$1" in
  version=*)
    VERSION="${1#version=}"
    ;;
  *)
    echo "Usage: ./build.sh version=X.Y.Z"
    exit 1
    ;;
esac

if [ -z "${VERSION}" ]; then
  echo "Error: version cannot be empty"
  exit 1
fi

echo "Building version: ${VERSION}"

# ---- Check that we're in a git repo ----
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Error: this directory is not a git repository."
  exit 1
fi

# ---- Update APP_VERSION in settings.py ----
if [ ! -f "${SETTINGS_FILE}" ]; then
  echo "Error: settings file '${SETTINGS_FILE}' not found."
  exit 1
fi

# ---- Run Ruff linter first to check if it passes ----
if command -v ruff >/dev/null 2>&1; then
  echo "Running Ruff linter..."
  if ! ruff check .; then
    echo "Ruff checks failed. Aborting build."
    exit 1
  fi
else
  echo "Ruff not found, skipping lint step."
fi

# ---- Run axe-core accessibility checks (WCAG 2.1 A) ----
echo "Running accessibility checks with axe-core (WCAG 2.1 A)..."

python manage.py runserver 127.0.0.1:8000 > /dev/null 2>&1 &
SERVER_PID=$!
echo "Django dev server started with PID ${SERVER_PID}"
sleep 3

set +e
python run_axe_a11y.py
A11Y_EXIT=$?
set -e

kill "${SERVER_PID}" 2>/dev/null || true

if [ "${A11Y_EXIT}" -ne 0 ]; then
  echo "Accessibility checks failed. Aborting build."
  exit 1
fi

echo "Accessibility checks passed."

echo "Updating APP_VERSION in ${SETTINGS_FILE} ..."

python - "${SETTINGS_FILE}" "${VERSION}" << 'EOF'
from pathlib import Path
import re
import sys

settings_path = Path(sys.argv[1])
version = sys.argv[2]

text = settings_path.read_text(encoding="utf-8")

pattern = r'APP_VERSION\s*=\s*["\']([^"\']*)["\']'
replacement = f'APP_VERSION = "{version}"'

new_text, count = re.subn(pattern, replacement, text)
if count == 0:
    raise SystemExit("APP_VERSION variable not found in settings.py")

settings_path.write_text(new_text, encoding="utf-8")
EOF

echo "APP_VERSION updated to ${VERSION}."

# ---- Create git tag ----
echo "Tagging current commit with '${VERSION}' ..."
git tag "${VERSION}" || {
  echo "Error: could not create git tag '${VERSION}'. (Maybe it already exists?)"
  exit 1
}

echo "Tag '${VERSION}' created."
echo "Remember to push it later with: git push origin \"${VERSION}\""

# ---- Create archive ----
ARCHIVE_NAME="${APP_NAME}-${VERSION}.zip"

echo "Creating archive: ${ARCHIVE_NAME} ..."
git archive --format=zip --output "${ARCHIVE_NAME}" HEAD

echo "Archive created: ${ARCHIVE_NAME}"

echo "Done. Version: ${VERSION}, tag: ${VERSION}, archive: ${ARCHIVE_NAME}"
