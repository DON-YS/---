#!/data/data/com.termux/files/usr/bin/bash
set -e

BASE="$HOME/.ys-ultra15"

echo "============================================================"
echo "⁖ 𝐃𝐎𝐍 ⁞ 𝐒𝐇𝐀𝐇𝐄𝐄𝐍-♔"
echo "YS15 UPDATE"
echo "============================================================"

if ! command -v git >/dev/null 2>&1; then
    echo "git is required."
    exit 1
fi

REPO="${YS15_REPO:-}"

if [ -z "$REPO" ]; then
    echo "YS15_REPO is not configured."
    echo
    echo 'Example:'
    echo 'export YS15_REPO="https://github.com/DON-YS/---.git"'
    exit 1
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

git clone --depth 1 "$REPO" "$TMP/repo"

mkdir -p "$BASE"

find "$TMP/repo" -maxdepth 1 -type f \
    ! -name "install.sh" \
    ! -name ".gitignore" \
    -exec cp {} "$BASE/" \;

for d in bin core config bot scripts security templates docs tests; do
    if [ -d "$TMP/repo/$d" ]; then
        mkdir -p "$BASE/$d"
        cp -R "$TMP/repo/$d/." "$BASE/$d/"
    fi
done

mkdir -p "$BASE/secrets"

echo
echo "✓ Update completed."
echo "✓ Existing secrets were preserved."
