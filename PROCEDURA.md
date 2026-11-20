# Procedura dzienna – konta faceless

Codziennie rano przygotuj szkice postów w Metricool dla trzech kont Krzyśka. Krzysiu zatwierdza je w aplikacji Metricool. Pisz do niego po polsku.

| Konto | Metricool blogId | Język |
|---|---|---|
| @marketminute.pl (Market Minute pl) | 8253009 | PL |
| @marketminuteng (Market Minute eng) | 8253033 | EN |
| @niewiemalebangla (Nie wiem ale bangla (chyba)) | 8252917 | PL |

**Nigdy** nie twórz postów w marce `krzysiuhexa` (blogId 8229647). Każdy post tworzysz jako **szkic** (`draft: true`). Nic nie publikujesz sam.

## Plan dnia (D = dzisiejsza data w Europe/Warsaw)

| Godzina | Konto | Typ |
|---|---|---|
| 09:00 | Market Minute PL + EN | `mm_carousel`: najważniejszy temat dnia z krypto lub biznesu, 4–5 slajdów |
| 13:00 | Market Minute PL + EN | `mm_numbers`: karta liczbowa (np. Bitcoin, Ethereum, kurs złotego, indeks giełdowy) |
| 18:00 | Market Minute PL + EN | `mm_carousel`: drugi temat dnia, 3–4 slajdy |
| 09:30 | Bangla | `bangla_carousel`: news dnia ze świata albo z Polski |
| 12:30 | Bangla | `bangla_carousel`: ciekawostka „nie wiedziałeś, że…” |
| 16:00 | Bangla | `bangla_carousel`: viral / temat z internetu (bez zdjęć ludzi) |
| 20:00 | Bangla | `bangla_carousel`: dziwna albo śmieszna historia ze świata |
| pn, śr, pt | Bangla (półautomat) | `bangla_photo`: najgorętszy temat polskiego internetu jako nakładka do zdjęcia, które Krzysiu dodaje sam |

Jeśli nie znajdziesz dość sprawdzonych tematów, zrób **mniej postów**. Nigdy nie wypełniaj planu na siłę.

## Kroki

1. **Repozytorium:** dodaj `krzysiuhexa-creator/faceless-konta` (add_repo, access push), sklonuj (`git clone --depth 1`), wejdź do katalogu, uruchom `bash tools/setup.sh`. Jeśli `posts/D/metricool.json` już istnieje, przerwij (dzień zrobiony) i napisz o tym krótko.
2. **Research (WebSearch):** newsy z ostatnich 24–48 h. Każdy fakt i każda liczba muszą być w **co najmniej 2 niezależnych źródłach**. Ceny podawaj z datą i godziną. Zanotuj źródła.
3. **Spec:** zapisz `posts/D/spec.json` według formatu niżej.
4. **Budowa:** `cd tools && python3 build.py ../posts/D/spec.json`. Jeśli są ostrzeżenia (`warnings`), skróć teksty i zbuduj ponownie, aż lista będzie pusta.
5. **Kontrola:** obejrzyj `posts/D/podglad.png` i co najmniej jeden pełny slajd z każdego posta (narzędzie Read). Sprawdź: brak nachodzących tekstów, emoji się wyświetlają, polskie znaki są poprawne, fakty zgadzają się ze źródłami.
6. **Wysyłka grafik:** `git add posts/D && git commit -m "Posty D" && git -c push.negotiate=true push`. Sprawdź `curl -sI` na jeden link raw z każdego posta (ma być 200).
7. **Metricool:** dla każdego wpisu w `posts/D/metricool.json` wywołaj `createScheduledPost` z dokładnie tymi polami `blogId`, `date`, `info`. Jeśli jakiś się nie uda, zanotuj błąd i idź dalej.
8. **Wiadomość do Krzyśka** (ostatnia odpowiedź, krótko):
   - lista szkiców: konto, godzina, temat w 3–5 słowach;
   - podgląd: `https://github.com/krzysiuhexa-creator/faceless-konta/blob/main/posts/D/podglad.png`;
   - w pn/śr/pt nakładka do zdjęcia: link raw do `zdjecie-<slug>-nakladka.png`, opis do wklejenia i co ma być na zdjęciu (`photo_hint`). Instrukcja: w Canvie zdjęcie na całą stronę 1080×1350, nakładka na wierzch, eksport PNG;
   - ewentualne błędy;
   - na końcu: „Zatwierdź w Metricool: Planer → szkice → Zaplanuj”.

## Zasady treści

- **Wszystko własne.** Teksty piszesz sam, bez kopiowania zdań ze źródeł (cytat najwyżej kilka słów). Bez zdjęć, logo i grafik z internetu. Wizualnie tylko szablony, emoji i liczby.
- **Źródła** na grafice (`src`) i w opisie.
- **Market Minute:** zero porad inwestycyjnych, bez „kupuj/sprzedawaj”, bez pewnych prognoz. Prognozy tylko jako „analitycy szacują” ze źródłem. Stopka z zastrzeżeniem dodaje się sama. Tematy: krypto, giełda, duże firmy, gospodarka. Wersja EN to ta sama treść w naturalnym angielskim (daty w formacie „Nov 21, 2026”, liczby „$1.2B”).
- **Bangla:** luźny ton, krótkie zdania, emoji. „(chyba)” wolno tylko w żarcie, nigdy przy fakcie. Polityka wyłącznie informacyjnie, bez komentarza i bez żartów. Bez tragedii, śmierci, przemocy, ofiar przestępstw, chorób i dzieci jako tematów do śmiechu. Bez osób prywatnych z imienia i nazwiska. O znanych osobach tylko sprawdzone fakty, bez plotek i oskarżeń.
- Pisz neutralnie płciowo, gdy to możliwe.
- Opis posta: 1. linijka to hak, potem 2–3 krótkie linijki, wezwanie („Przesuń 👉”, „Wyślij to komuś, kto…”, pytanie do komentarzy), źródła, 3–5 hashtagów. Market Minute kończy opis linijką „Informacja, nie porada inwestycyjna.” / „Information, not financial advice.”
- Kolor akcentu Bangla zmieniaj między postami: `#FFD21F`, `#FF4FA0`, `#3EE6C1`, `#7CFF4F`, `#FF8A3D`.

## Format `spec.json`

Teksty mogą mieć `<b>…</b>` (wyróżnienie) i `&nbsp;` (twarda spacja, np. `115,8&nbsp;mld&nbsp;$`). Bez innych znaczników.

```json
{
 "date": "2026-11-21",
 "posts": [
  {"type": "mm_carousel", "slug": "nvidia", "time": "09:00",
   "pl": {"tag": "BIZNES", "date": "21.11.2026", "src": "Źródła: NVIDIA, Reuters", "caption": "…",
     "slides": [
      {"kind": "cover", "kicker": "NVIDIA", "title": "Krótki nagłówek, max ~60 znaków", "big": "+103%", "big_label": "przychody rok do roku", "down": false},
      {"kind": "bullets", "title": "Co się stało", "items": ["3–4 punkty, każdy max ~70 znaków"]},
      {"kind": "bars", "title": "Przychody w kwartale", "a_label": "rok temu", "a_value": "57,0 mld $", "a": 57.0, "b_label": "teraz", "b_value": "115,8 mld $", "b": 115.8, "note": "1 zdanie"},
      {"kind": "bullets", "title": "Co dalej", "items": ["max 3 punkty"], "stat": "≈130 mld $", "stat_label": "krótki podpis"},
      {"kind": "why", "title": "Dlaczego to ważne", "text": "1–2 zdania, max ~170 znaków"}
     ]},
   "en": {"tag": "BUSINESS", "date": "Nov 21, 2026", "src": "Sources: …", "caption": "…", "slides": ["… to samo po angielsku …"]}},

  {"type": "mm_numbers", "slug": "btc", "time": "13:00",
   "pl": {"tag": "KRYPTO", "date": "21.11.2026", "kicker": "BITCOIN W LICZBACH", "value": "64&#8239;146&nbsp;$", "value_label": "stan na 21.11, 8:00",
          "chart": {"points": [92873, 81443, 64146], "labels": ["rok temu", "miesiąc temu", "dziś"]},
          "rows": [["vs wczoraj", "−1,3%", "dn"], ["vs miesiąc temu", "−21,2%", "dn"], ["Ethereum", "1 797 $", ""]],
          "src": "Źródło: …", "caption": "…"},
   "en": {"…": "…"}},

  {"type": "bangla_carousel", "slug": "glosny", "time": "20:00", "accent": "#FFD21F", "src": "Guinness World Records / AP", "caption": "…",
   "slides": [
    {"kind": "cover", "title": "Nagłówek, max ~55 znaków", "sub": "Podtytuł, max ~60 znaków", "emoji": "📢", "big": "122,4 dB",
     "tags": [["🪚", "piła łańcuchowa"], ["✈️", "start odrzutowca"], ["🚑", "syrena z bliska"]]},
    {"kind": "rows", "title": "Kto to?", "rows": [["🇦🇺", "max 4 wiersze, każdy max ~80 znaków, <b>wyróżnienie</b>"]]},
    {"kind": "bars", "title": "Porównanie", "sub": "…", "bars": [["121,7 dB", "1994<br>„quiet!”", false], ["122,4 dB", "2026<br>„now!”", true]], "note": "1–2 zdania"},
    {"kind": "rows", "title": "Bonus", "rows": [["🤫", "max 3 wiersze, gdy jest cta"]], "cta": "Wyślij to komuś, kto…", "cta_small": "Żart z (chyba)"}
   ]},

  {"type": "bangla_photo", "slug": "gta6", "accent": "#FF4FA0", "title": "Nagłówek", "sub": "Podtytuł", "src": "Źródło", "caption": "…", "photo_hint": "co ma być na zdjęciu"}
 ]
}
```

- `mm_carousel`: od 2 do 5 slajdów, pierwszy zawsze `cover`, ostatni najlepiej `why`. `big` może być pusty; `down: true` maluje liczbę na czerwono. Przy złych wiadomościach (spadki) dodaj w `pl` i `en` pole `"mood": "down"`: wyróżnienia będą czerwone zamiast zielonych.
- `mm_numbers`: `rows[][2]` to klasa: `"dn"` (czerwony), `"upc"` (zielony) albo `""`. Wykres opcjonalny (2–5 punktów).
- `bangla_carousel`: od 1 do 4 slajdów, pierwszy zawsze `cover`. `big` (krótki, max ~10 znaków) i `tags` (0–3) są opcjonalne.
- Okładka Bangla: zamiast `emoji` możesz dać `"hero": "GTA 6"` (duży napis, 1–6 znaków, `hero_size` domyślnie 300). Wtedy nie dawaj `tags`. Hero jest lepszy, gdy temat ma krótką, rozpoznawalną nazwę (gra, firma, liczba). Hero to zwykły tekst naszą czcionką, nigdy logo ani stylizacja cudzej marki.
- Nazwy `slug`: małe litery, bez polskich znaków, unikalne w danym dniu.
