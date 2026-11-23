# PROCEDURA-YT: automat odcinków YouTube (Ukryta Lekcja + Nie wiem ale bangla)

Decyzja Krzysia z 22.11.2026: **1 odcinek tygodniowo na kanał**, bank tematów akceptowany raz, **publikacja automatyczna z oknem na weto 48 h**. Jedyny krok ręczny Krzysia: nagranie lektora w ElevenLabs i wrzucenie MP3 do `yt-inbox/` na gałęzi `main`.

Odpowiadasz po polsku. Pliki z tej gałęzi (`wideo`) to kod, scenariusze i stan. Gotowe filmy idą na gałąź `media`.

## 0. Zasady, których nie łamiesz nigdy

- Marka **krzysiuhexa (blogId 8229647)**: nigdy nic nie twórz ani nie zmieniaj.
- Nie zmieniaj i nie usuwaj postów w Metricool, których nie utworzył ten przebieg.
- Nie używaj Higgsfielda (kosztuje kredyty). Nie zakładaj kont, nie kupuj niczego.
- Gałęzi `main` nie zmieniasz (pliki z `yt-inbox/` tylko czytasz).
- **Fakty:** każda liczba, data, cytat i badanie potwierdzone w 2 niezależnych źródłach (dla badań: streszczenie/abstrakt oryginału + jedno rzetelne omówienie). Cytatów nie wymyślasz. Gdy źródła się różnią, lektor mówi to wprost („dla uczciwości: źródła się różnią…”).
- **Bangla:** legendy jako „podobno” / „według relacji”; naklejka „(chyba)” tylko przy żartach, nigdy przy faktach. Osób prywatnych nie podajesz z nazwiska (np. ofiar oszustw). Z tragedii się nie żartuje.
- **Grafika:** wszystko rysujesz sam (SVG/HTML). Żadnych logo, cudzych postaci, kadrów z filmów, zdjęć osób publicznych ani podobizn wzorowanych na zdjęciach. Osoby historyczne = ikonka/sylwetka + podpis.
- **Nie szablon:** YouTube nie monetyzuje treści „masowo produkowanych lub powtarzalnych”. Każdy odcinek ma własną metaforę, własną historię i nowe kompozycje plansz. Nie kopiujesz plansz z poprzednich odcinków; z silnika bierzesz tylko narzędzia (styl, animacje, dźwięk).
- Głos to AI: zawsze `isAiGeneratedContent: true` (YouTube) i `isAiGenerated: true` (Instagram).

## 1. Przygotowanie sesji (oba zadania)

```bash
# po add_repo krzysiuhexa-creator/faceless-konta (access "push")
cd /home/claude && git clone -q https://github.com/krzysiuhexa-creator/faceless-konta.git && cd faceless-konta
git fetch -q origin +refs/heads/wideo:refs/remotes/origin/wideo +refs/heads/media:refs/remotes/origin/media
git worktree add -q -B wideo /home/claude/wideo origin/wideo
```
Stan: `/home/claude/wideo/yt/stan.json`. Tematy: `/home/claude/wideo/yt/tematy.md`.

Silniki (tylko w zadaniu produkcji): `bash tools/setup.sh`, `(cd tools && npm i @fontsource/caveat @fontsource/kalam)`, `pip install --break-system-packages numba scipy numpy`, potem
`mkdir -p /home/claude/faceless/yt /home/claude/bangla-yt && cp -r /home/claude/wideo/yt/ukryta-lekcja/* /home/claude/faceless/yt/ && cp -r /home/claude/wideo/yt/bangla/* /home/claude/bangla-yt/`.
Szczegóły silników: `yt/README.md`.

## 2. Zadanie A: scenariusze (poniedziałek)

Dla każdego kanału osobno:
1. Jeśli w `stan.json` kanał ma `oczekuje` (scenariusz czeka na nagranie): niczego nowego nie pisz. W podsumowaniu przypomnij o nagraniu i wklej jeszcze raz tekst do ElevenLabs.
2. W przeciwnym razie weź **pierwszy temat** z `tematy.md` dla kanału, który nie jest oznaczony `[zrobione]`. Zrób research (zasady z punktu 0).
3. Napisz scenariusz:
   - **Ukryta Lekcja** (schemat: `yt/ukryta-lekcja/SCHEMAT.md`, wzory: odc. 1–2): hook → reframe → mechanizm z jedną metaforą-rysunkiem → dowód (badanie: kto, rok, 1–2 liczby) → mapa 3 kroków → 3 kroki (dlaczego działa + przykład + zadanie na dziś) → ukryta lekcja (krótka historia z maskotką, kończy się żółtym zdaniem „Ukryta lekcja: …”) → outro z zajawką **następnego tematu z banku**. Tytuł: małe litery, „dlaczego …”. 28–34 fragmenty, 650–800 słów.
   - **Bangla „Dziwne historie”** (wzór: odc. 1 Wojtek, odc. 2 Lustig): hook w 3–4 krótkich zdaniach → kim/co → przebieg z napięciem → zwrot → „dla uczciwości” przy spornych miejscach → zakończenie „Dziwna historia? Nie wiem. Ale bangla.” → CTA „wyślij to komuś, kto…” + zajawka **następnego tematu z banku**. 30–36 fragmentów, 600–800 słów, krótkie zdania, energia.
   - Każdy fragment = 1 plansza; pod fragmentem opis planszy. Fragmenty w pliku dla lektora łączysz ciągiem ` [long pause] ` (spacja, tag, spacja). Liczba tagów = liczba fragmentów − 1.
4. Zapisz w `yt/<kanał>/odc<N>/`: `scenariusz.md` (tytuł, miniatura, fragmenty z planszami, źródła) i `lektor.txt`. `<kanał>` = `ukryta-lekcja` albo `bangla`.
5. W `stan.json` ustaw kanałowi `oczekuje = {odc, fragmenty, tytul, scenariusz, lektor, od}`; w `tematy.md` oznacz temat `[w toku odcN]`. Jeśli w banku kanału zostały < 3 tematy, dopisz 6 nowych na końcu jako `(propozycja)` według tych samych kryteriów.
6. Commit + push gałęzi `wideo`.
7. Podsumowanie dla Krzysia (pkt 5).

## 3. Zadanie B: produkcja (codziennie)

1. Wylistuj `yt-inbox/*.mp3` na `main` (`git ls-tree --name-only origin/main yt-inbox/`). Pomiń pliki z listy `przetworzone` w `stan.json`. Brak nowych → zakończ krótko („brak nowych nagrań”), bez podsumowania z listą.
2. **Max 1 odcinek na przebieg.** Przy kilku nowych plikach weź najstarszy; reszta jutro.
3. **Dopasowanie nagrania:** pobierz plik (`git show "origin/main:yt-inbox/<plik>" > /tmp/x.mp3`; nazwę zawsze w cudzysłowie, bywają spacje i `&`). Jeśli w `yt/<kanał>/odc<N>/granice.json` oczekującego odcinka pole `nagranie` = nazwa tego pliku, to jest ten odcinek (granice już policzone i sprawdzone). W przeciwnym razie dla każdego oczekującego odcinka uruchom `python3 -I yt/narzedzia/granice.py /tmp/x.mp3 yt/<kanał>/odc<N>/lektor.txt /tmp/granice-<kanał>.json "<plik>"`. Pasuje odcinek z `"ocena": "ok"` (dwa „ok” → mniejsza `mediana_odchylenia`; podpowiedź z nazwy: „Oscar” = Bangla, „yooyo” = Ukryta Lekcja). **Nigdy nie dopasowuj po samej liczbie długich pauz:** ElevenLabs v4 potrafi w części nagrania zrobić z `[long pause]` pauzę tak krótką jak zwykła przerwa między zdaniami (tak było w odc. 2 Ukrytej), a zwykła pauza w zdaniu bywa dłuższa od pauzy po tagu (odc. 2 Bangla). Nie pasuje do niczego → nic nie produkuj, dopisz plik do `przetworzone` z `blad`, a w podsumowaniu podaj `powod`/`stosunki` i co poprawić.
4. **Folder odcinka:** Bangla: skopiuj wszystkie `.py` + `finish.sh` z `odc1`, zamień ścieżki `/odc1` → `/odc<N>`. Ukryta: skopiuj `.py` + `finish.sh` z **`odc2`** (ciszszy szum tła, Shortsy metodą kadrowania, `finish.sh` z −14 LUFS), zamień `/odc2` → `/odc<N>`; `boards.py` i tak piszesz od nowa. Nagranie → `odc<N>/glos/lektor.mp3`, tekst → plik TXT, z którego czyta `align.py`. Ustaw w `align.py` liczbę fragmentów i pierwsze fragmenty sekcji. **Granice fragmentów bierzesz z `granice.json`:** w `align.py` zamień wybór najdłuższych pauz (`longp = sorted(sorted(...)[:NF - 1])` i ewentualny `assert ... > 1.0`) na `longp = [tuple(p) for p in json.load(open("<ścieżka>/granice.json"))["pauzy"]]`.
5. `align.py` → sprawdź tempo (zn/s) i tryb mapowania każdego fragmentu.
6. **`boards.py` piszesz od nowa** pod ten scenariusz: elementy przypięte do słów `A(fid,"fraza")`, coś zmienia się co 2–4 s, pierwsze 3 sekundy nigdy puste. Styl kanału zachowany, kompozycje nowe.
7. **Kontrola kadrów:** `qa.py` (stopklatki tuż przed końcem każdej planszy + momenty z największą liczbą elementów) → arkusze 2×2 → obejrzyj każdy. Szukaj: nachodzenia tekstów, elementów na logo/źródle u dołu, uciętych napisów, pustych momentów > 2 s. Poprawiaj i powtarzaj, aż czysto.
8. **Tło ciszej (decyzja Krzysia 23.11.2026: „ma być troszkę ciszej”):** Ukryta: w `mix.py` zostaw `AMB = 0.35` i `duck_amb = 1 - 0.6 * envv` (jak w odc2). Bangla: w `mix.py` podkład `mus * 0.27` zamiast `mus * 0.36` (ok. −2,5 dB). Nie podnoś tego z powrotem.
   **Render:** `render_all.py` w 2 procesach w tle (`nohup … &`, połowa plansz każdy), sprawdzaj co kilka minut. Potem `mix.py`, sklejenie i głośność −14 LUFS (Bangla `finish.sh`; Ukryta: concat scen `-c copy` + `volume`/`alimiter` jak w `finish.sh`, sprawdź ebur128: I ≈ −14, TP ≤ −1).
9. **Kontrola gotowego pliku:** 20+ klatek wyciągniętych z mp4 w arkuszach; czas trwania; dźwięk bez ciszy na starcie/końcu. Popraw i przerenderuj tylko zepsute sceny.
10. `package.py`: `napisy-pl.srt`, `opis.txt` (opis **bez linków** – kanały niezweryfikowane; źródła z nazwy; rozdziały od 0:00, min. 3, każdy ≥ 10 s), `miniaturka.jpg` 1280×720.
11. **3 Shortsy** 1080×1920: Bangla metodą z `bangla/odc1/shorts.py` (kadr z gotowego filmu + nagłówek + napisy + plansza końcowa); Ukryta wersją pionową z `ukryta-lekcja/odc1/shorts.py` albo tą samą metodą kadrowania. Każdy zaczyna się od mocnego zdania, 25–50 s. Obejrzyj po 3 klatki z każdego.
12. **Pliki na `media`:** `media/<kanał>-yt-odc<N>/` → `film.mp4`, `miniaturka.jpg`, `short-s1..3.mp4`, `lektor.mp3`. Commit + push. Adresy: `https://raw.githubusercontent.com/krzysiuhexa-creator/faceless-konta/refs/heads/media/media/<kanał>-yt-odc<N>/<plik>` (sprawdź curl → 200).
13. **Metricool** (Ukryta: blogId `8254291`; Bangla: blogId `8252917`), `createScheduledPost`, `autoPublish: true`, `draft: false` (wyjątek: niepewny fakt → `draft: true` i powód w podsumowaniu):
    - **Odcinek:** tylko `youtube`; `youtubeData = {title, type:"video", privacy:"public", tags, category:"EDUCATION", madeForKids:false, isAiGeneratedContent:true}`; `text` = opis z `opis.txt`; `videoThumbnailUrl` = miniaturka (jeśli błąd `VIDEO_THUMBNAIL_NOT_APPLICABLE`, wyślij jeszcze raz bez niej i zapisz to w podsumowaniu).
    - **Termin (okno na weto):** pierwszy slot ≥ 48 h od teraz. Ukryta: **czwartek lub niedziela 18:00**; Bangla: **sobota lub wtorek 18:00** (Europe/Warsaw).
    - **Shortsy:** 3 kolejne dni po odcinku; Ukryta **17:30**, Bangla **19:00**; `providers` youtube + instagram; `youtubeData {title …#shorts, type:"short", privacy:"public", tags, category:"EDUCATION", madeForKids:false, isAiGeneratedContent:true}`; `instagramData {type:"REEL", showReelOnFeed:true, isAiGenerated:true}`; opis z CTA do całego odcinka na kanale YouTube.
    - Przed utworzeniem sprawdź `getScheduledPosts` danej marki: nie twórz drugi raz tego samego i nie wstawiaj Shortsa na zajętą godzinę (wtedy dzień później).
    - Po utworzeniu potwierdź `getScheduledPosts`.
14. **Zapis:** kod, scenariusz i `granice.json` odcinka do `yt/<kanał>/odc<N>/` (bez mp4/wav/mp3), `stan.json`: kanałowi `oczekuje = null`, dopisz do `odcinki` (odc, tytul, data publikacji, id postów Metricool), plik do `przetworzone`; w `tematy.md` `[zrobione odcN]`. Commit + push `wideo`.
15. Podsumowanie (pkt 5).

## 4. Gdy coś nie działa

GitHub, Metricool albo render nie działa → nie obchodź tego innymi drogami. Zrób, co się da, nic nie publikuj z połowy, opisz problem. Nie powtarzaj w kółko tej samej nieudanej operacji (max 2 próby).

## 5. Podsumowanie dla Krzysia (krótko, po polsku)

**Zadanie A:** dla każdego kanału: tytuł, 2 zdania o odcinku, głos do użycia (Ukryta: klon „yooyo”, Bangla: „Oscar – Energetic, Direct”, model Eleven v4), cały tekst do ElevenLabs w bloku kodu i link do `lektor.txt`, instrukcja: „Wklej całość, tagów [long pause] nie usuwaj, pobierz MP3 i wrzuć na GitHub: faceless-konta → main → folder yt-inbox → Add file → Upload files”. Jeśli dopisałeś propozycje tematów – lista do ewentualnego skreślenia.

**Zadanie B:** kanał, tytuł, kiedy wyjdzie odcinek i 3 Shortsy, linki do podglądu (`film.mp4`, `miniaturka.jpg`, Shortsy), szkice review z powodem, błędy. Na końcu zawsze:
„Wyjdzie samo. Żeby zatrzymać: Metricool → Planer → post → Usuń. Po publikacji Shortsów ustaw w YouTube Studio ‚Powiązany film’ na cały odcinek. Napisy (opcjonalnie): YouTube Studio → Napisy → wgraj plik z linku.”
