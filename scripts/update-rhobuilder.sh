#!/usr/bin/env bash
# Move the pinned rhobuilder submodule to latest upstream main, or to a given commit/tag.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)/vendor/rhobuilder"
git fetch --tags origin
target="${1:-origin/main}"
git checkout --quiet "$target"
echo "rhobuilder now at $(git rev-parse --short HEAD) — $(git log -1 --format=%s)"
cd ../..
git add vendor/rhobuilder
echo "Staged. Review, test, then commit."
