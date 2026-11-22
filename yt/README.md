# Silniki wideo na YouTube

**Automat (od 22.11.2026):** zadania działają według `yt/PROCEDURA-YT.md`; stan w `yt/stan.json`, tematy w `yt/tematy.md`, nagrania lektora Krzysiu wrzuca do `yt-inbox/` na gałęzi `main`.

Dwa silniki, które robią całe odcinki z jednego pliku MP3 z lektorem: animację, efekty, podkład, napisy, opis i Shortsy.

| Kanał | Styl | Folder | Głos ElevenLabs |
|---|---|---|---|
| Ukryta Lekcja | tablica z kredą, maskotka z dziurką od klucza | `yt/ukryta-lekcja/` | klon „yooyo”, Eleven v4 |
| Nie wiem ale bangla | ciemne tło, naklejki, żółty #FFD21F / różowy #FF4FA0, rysowany miś | `yt/bangla/` | „Oscar – Energetic, Direct”, Eleven v4 |

Nie ma tu plików MP3/WAV/MP4: są za duże i odtwarza się je z kodu i nagrania lektora.

## Przywrócenie w nowej sesji

Skrypty mają wpisane ścieżki bezwzględne, więc kopiujemy je dokładnie w te miejsca:

```bash
cd /home/claude && git clone https://github.com/krzysiuhexa-creator/faceless-konta.git && cd faceless-konta && git checkout wideo
bash tools/setup.sh                                   # Poppins i inne czcionki, Playwright, Chrome
(cd tools && npm i @fontsource/caveat @fontsource/kalam)   # czcionki kredy dla Ukrytej Lekcji
pip install --break-system-packages numba scipy numpy
mkdir -p /home/claude/faceless/yt /home/claude/bangla-yt
cp -r yt/ukryta-lekcja/* /home/claude/faceless/yt/
cp -r yt/bangla/* /home/claude/bangla-yt/
```

Potrzebne są też: `ffmpeg` z libass i systemowa czcionka Noto Color Emoji (emoji w Bangli).

## Jak powstaje odcinek (oba kanały tak samo)

1. **Scenariusz** dzielony na fragmenty, między nimi tag `[long pause]` (Eleven v4 robi z niego ok. 1,1 s ciszy). Cały tekst w jednym pliku `.txt`.
2. **Jedno MP3** z ElevenLabs z całym tekstem → `glos/lektor.mp3`.
3. `align.py`: szuka długich pauz (silencedetect), tnie lektora na fragmenty, skraca pauzy i liczy, kiedy pada każde zdanie → `lektor_cut.wav` i `timeline.json`. Liczba długich pauz musi się równać liczbie fragmentów minus 1.
4. `boards.py`: plansze. Każdy element pojawia się w chwili, gdy lektor mówi daną frazę: `A(fid, "fraza")` = początek frazy, `E(fid, "fraza")` = koniec.
5. `qa.py`: kadry kontrolne (najgęstsze momenty), żeby wyłapać nakładające się elementy przed renderem.
6. `render_all.py b01 b02 …`: render scen (Playwright → JPEG → ffmpeg). Na 2 rdzeniach puszczać 2 procesy z połową plansz każdy.
7. `mix.py`: lektor + efekty z animacji + podkład ściszany pod głosem.
8. Sklejenie i głośność -14 LUFS. W Bangli robi to `finish.sh`.
9. `package.py`: napisy `.srt`, opis z rozdziałami i źródłami, miniaturka.
10. `shorts.py`: Shortsy 1080×1920 wycięte z gotowego odcinka (tytuł, nagłówek planszy, napisy, plansza końcowa).

## Publikacja

- Metricool: odcinek ręcznie albo `createScheduledPost` z `youtubeData` (`isAiGeneratedContent: true`, bo głos to AI).
- Pliki dla Metricool wrzucamy na gałąź `media` i podajemy adres `https://raw.githubusercontent.com/krzysiuhexa-creator/faceless-konta/refs/heads/media/<ścieżka>` (krótszy adres bez `refs/heads` daje 404).
- Po publikacji Shortsa ustawić ręcznie w YouTube Studio „Powiązany film” → pełny odcinek.

## Zasady treści

- Fakty podajemy wprost, legendy oznaczamy „podobno” / „według relacji”. W Bangli „(chyba)” tylko przy żartach.
- Wszystkie rysunki są nasze (żadnych logo, cudzych postaci, zdjęć osób publicznych).
