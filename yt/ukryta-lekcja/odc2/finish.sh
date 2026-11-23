#!/usr/bin/env bash
# Sklejenie scen + głośność -14 LUFS (Ukryta Lekcja odc2). Po render_all.py i mix.py.
set -e
cd "$(dirname "$0")"
python3 -c "
from boards import build
open('lista.txt','w').write(''.join(f\"file 'sceny/scena_{b.name}.mp4'\n\" for b in build()))"
ffmpeg -loglevel error -y -f concat -safe 0 -i lista.txt -c copy _obraz.mp4
I=$(ffmpeg -hide_banner -i dzwiek_mix.wav -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -1 | awk '{print $2}')
G=$(python3 -c "print(round(-14.0-($I)+0.3,2))")
ffmpeg -loglevel error -y -i dzwiek_mix.wav -af "volume=${G}dB,alimiter=limit=0.84:attack=3:release=80:level=false" dzwiek_final.wav
mkdir -p paczka
ffmpeg -loglevel error -y -i _obraz.mp4 -i dzwiek_final.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -ar 48000 -movflags +faststart paczka/film.tmp.mp4
mv paczka/film.tmp.mp4 paczka/film.mp4
ffmpeg -hide_banner -i paczka/film.mp4 -vn -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):"
