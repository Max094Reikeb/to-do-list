#!/usr/bin/env bash
set -euo pipefail

# ---- Config ----
APP_NAME="todolist"
SETTINGS_FILE="todo/settings.py"

# ---- Parse arguments ----
if [ $# -lt 1 ]; then
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

if [ -z "$VERSION" ]; then
  echo "Error: version cannot be empty"
  exit 1
fi

echo "Building version: $VERSION"

# ---- Check that we're in a git repo ----
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Error: this directory is not a git repository."
  exit 1
fi

# ---- Update APP_VERSION in settings.py ----
if [ ! -f "$SETTINGS_FILE" ]; then
  echo "Error: settings file '$SETTINGS_FILE' not found."
  exit 1
fi

echo "Updating APP_VERSION in $SETTINGS_FILE ..."

python - <<EOF
from pathlib import Path
import re
settings_path = Path("$SETTINGS_FILE")
text = settings_path.read_text(encoding="utf-8")

pattern = r'APP_VERSION\s*=\s*["\']([^"\']*)["\']'
replacement = f'APP_VERSION = "{ "$VERSION" }"'

new_text, count = re.subn(pattern, replacement, text)
if count == 0:
    raise SystemExit("APP_VERSION variable not found in settings.py")

settings_path.write_text(new_text, encoding="utf-8")
EOF

echo "APP_VERSION updated to $VERSION."

# ---- Create git tag ----
echo "Tagging current commit with '$VERSION' ..."
git tag "$VERSION" || {
  echo "Error: could not create git tag '$VERSION'. (Maybe it already exists?)"
  exit 1
}

echo "Tag '$VERSION' created."
echo "Remember to push it later with: git push origin \"$VERSION\""

# ---- Create archive ----
ARCHIVE_NAME="${APP_NAME}-${VERSION}.zip"

echo "Creating archive: $ARCHIVE_NAME ..."
git archive --format=zip --output "$ARCHIVE_NAME" HEAD

echo "Archive created: $ARCHIVE_NAME"

echo "Done. Version: $VERSION, tag: $VERSION, archive: $ARCHIVE_NAME"
