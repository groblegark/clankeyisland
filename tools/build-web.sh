#!/usr/bin/env bash
# Build the browser (WebAssembly) version of Clanker City Chronicles.
#
# Pipeline:
#   1. vendor + patch ScummVM source (vendor/scummvm-src, gitignored)
#   2. compile ScummVM -> wasm via its emscripten port (scumm engine only;
#      build.sh downloads its own pinned emsdk, no system emscripten needed)
#   3. assemble a static site in web/dist: scummvm.{html,js,wasm} + data/,
#      our game files under data/games/chronicles, a seed scummvm.ini, and
#      an index.html that auto-launches the game via the URL fragment
#
# The site is path-prefix sensitive: ScummVM bakes its data dir into the
# wasm as an origin-absolute URL. SITE_PATH must match where the site is
# mounted (default: /clankeyisland for GitHub project pages). Use
# SITE_PATH="" for hosts that serve at the domain root.
#
# Usage:  tools/build-web.sh            # build everything
#         tools/build-web.sh serve      # build, then serve on :8000 with
#                                       # the correct path prefix

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SVM="$ROOT/vendor/scummvm-src"
SITE_PATH="${SITE_PATH-/clankeyisland}"
OUT="$ROOT/web/dist"

# --- 1. ScummVM source + local patches -------------------------------------
if [ ! -d "$SVM" ]; then
    git clone --depth 1 https://github.com/scummvm/scummvm.git "$SVM"
fi
# configure's wasm32 host block clobbers --datadir; patch it to only apply
# the /data default when the user didn't pass one.
if grep -q "^	datadir='/data'\$" "$SVM/configure"; then
    patch -p1 -d "$SVM" < "$ROOT/tools/patches/0002-scummvm-configure-respect-datadir.patch"
fi

# --- 2. game data + wasm build ----------------------------------------------
make -C "$ROOT/game" tentacle

cd "$SVM"
./dists/emscripten/build.sh build \
    --enable-release \
    --disable-all-engines --enable-engine=scumm \
    --disable-detection-full \
    --datadir="$SITE_PATH/data"

# Guard against a stale wasm: the baked data path must match SITE_PATH.
if ! grep -q "DATA_PATH=\\\\\"$SITE_PATH/data\\\\\"" "$SVM/config.mk"; then
    echo "ERROR: config.mk DATA_PATH does not match SITE_PATH=$SITE_PATH" >&2
    exit 1
fi

# --- 3. assemble the site ----------------------------------------------------
rm -rf "$OUT"
mkdir -p "$OUT"
cp -R "$SVM/build-emscripten/." "$OUT/"

mkdir -p "$OUT/data/games/chronicles"
cp "$ROOT/game/build/tentacle.000" "$ROOT/game/build/tentacle.001" \
    "$OUT/data/games/chronicles/"

sed "s|@SITE_PATH@|$SITE_PATH|g" "$ROOT/web/scummvm.ini.in" > "$OUT/scummvm.ini"

# index.json sizes are load-bearing for the HTTP filesystem; regenerate
# after adding the game files.
python3 "$SVM/dists/emscripten/build-make_http_index.py" "$OUT/data"

# Landing page: scummvm.html with the game target pre-set in the fragment
# (custom_shell-pre.js turns the fragment into argv) and our title.
sed -e 's|<head>|<head>\n  <script>if (!location.hash) location.hash = "chronicles";</script>|' \
    -e 's|<title>ScummVM</title>|<title>Clanker City Chronicles</title>|' \
    "$OUT/scummvm.html" > "$OUT/index.html"

touch "$OUT/.nojekyll"

echo "Site assembled in $OUT (SITE_PATH=$SITE_PATH)"

# --- optional local test server ----------------------------------------------
if [ "${1-}" = "serve" ]; then
    # Serve so the site appears under SITE_PATH, like on the real host.
    SRV="$(mktemp -d)"
    if [ -n "$SITE_PATH" ]; then
        ln -s "$OUT" "$SRV$SITE_PATH"
    else
        SRV="$OUT"
    fi
    echo "Serving http://localhost:8000$SITE_PATH/"
    python3 -m http.server 8000 -d "$SRV"
fi
