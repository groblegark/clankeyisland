#!/usr/bin/env bash
# Deploy Clanker City Chronicles to GitHub Pages — gated by the
# walk-through-er: if the performer can't finish the full run (boot to
# the Act Two threshold), we don't ship.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

./tools/build-web.sh

echo "== validate gate: the full run must pass =="
python3 walkthrough/driver/walkthrough.py --serve \
    walkthrough/screenplay/full-run.play.yaml

echo "== deploying gh-pages =="
TMP=$(mktemp -d)
cp -R web/dist/. "$TMP"
git -C "$TMP" init -q -b gh-pages
git -C "$TMP" add -A
git -C "$TMP" -c user.email=matthewcbaker0122@gmail.com \
    -c user.name="Matthew Baker" commit -qm "Deploy $(git rev-parse --short HEAD)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
git -C "$TMP" push -qf https://github.com/groblegark/clankeyisland.git gh-pages
rm -rf "$TMP"
echo "live in ~1 min: https://groblegark.github.io/clankeyisland/"
