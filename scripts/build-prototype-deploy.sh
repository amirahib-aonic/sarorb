#!/bin/sh
set -e
root=$(git rev-parse --show-toplevel)
cd "$root"
src=docs/research/prototypes
out=${1:-"$root/.deploy"}
rm -rf "$out"
mkdir -p "$out/site"
cp "$src/borneo.PROTOTYPE.html" "$out/site/index.html"
cp "$src/borneo.PROTOTYPE.data.js" "$src/live.js" "$out/site/"
mkdir -p "$out/site/api"
cp "$src/api/firms.mjs" "$out/site/api/"
rev=$(git rev-parse --short HEAD)
dirty=$(git status --porcelain -- "$src" | head -1)
[ -n "$dirty" ] && rev="$rev-dirty"
(cd "$out/site" && powershell -NoProfile -Command "Compress-Archive -Force -Path * -DestinationPath ..\\ignis-borneo.zip" 2>/dev/null || zip -qr ../ignis-borneo.zip .)
echo "$rev" > "$out/REVISION"
echo "built $out/ignis-borneo.zip from $rev"
