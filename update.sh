#!/data/data/com.termux/files/usr/bin/bash

set -e

BASE="$HOME/.ys-ultra15"

if [ -x "$BASE/bin/ys15-update" ]; then
    exec "$BASE/bin/ys15-update"
fi

echo "⁖ 𝐃𝐎𝐍 ⁞ 𝐒𝐇𝐀𝐇𝐄𝐄𝐍-♔"
echo
echo "❌ YS15 update engine is not installed."
exit 1
