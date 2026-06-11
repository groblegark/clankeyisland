#!/usr/bin/env bash
# Bootstrap the ScummC toolchain into vendor/scummc and build it.
# Idempotent: safe to re-run.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENDOR="$REPO_ROOT/vendor/scummc"
BASE_COMMIT="$(cat "$REPO_ROOT/tools/patches/scummc-base-commit.txt")"

command -v xsltproc >/dev/null || { echo "xsltproc missing (ships with macOS)"; exit 1; }
brew list --versions bison >/dev/null 2>&1 || brew install bison
export PATH="/opt/homebrew/opt/bison/bin:$PATH"

if [ ! -d "$VENDOR/.git" ]; then
  git clone https://github.com/AlbanBedel/scummc "$VENDOR"
fi
cd "$VENDOR"
git fetch -q origin
git checkout -q "$BASE_COMMIT"
git checkout -q -- . # drop any previous patch application
for p in "$REPO_ROOT"/tools/patches/0*.patch; do
  git apply "$p"
done

./configure
make

BIN_DIR="$(ls -d "$VENDOR"/build.*/arm64-darwin-* | head -1)"
echo
echo "ScummC built. Binaries in: $BIN_DIR"
"$BIN_DIR/scc" 2>&1 | head -2 || true
