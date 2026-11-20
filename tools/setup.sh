#!/usr/bin/env bash
# Instaluje czcionki (fontsource z npm) i sprawdza Chrome + Playwright.
set -e
cd "$(dirname "$0")"
if [ ! -d node_modules/@fontsource/poppins @fontsource/anton @fontsource/crimson-pro @fontsource/oswald ]; then
  npm init -y >/dev/null 2>&1 || true
  npm i @fontsource/space-grotesk @fontsource/jetbrains-mono @fontsource/poppins @fontsource/anton @fontsource/crimson-pro @fontsource/oswald >/dev/null 2>&1
fi
python3 -c "import playwright" 2>/dev/null || pip install --break-system-packages playwright >/dev/null 2>&1
test -x /usr/bin/google-chrome || { echo "BRAK /usr/bin/google-chrome"; exit 1; }
fc-list | grep -qi "Noto Color Emoji" || echo "UWAGA: brak systemowej czcionki Noto Color Emoji (emoji się nie wyrenderują)"
echo "setup ok"
