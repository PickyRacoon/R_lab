import os
import asyncio
from googletrans import Translator

async def przetlumacz_tekst(translator, tekst):
    try:
        tlumaczenie = await translator.translate(tekst, src='en', dest='pl')
        return tlumaczenie.text
    except Exception as e:
        print(f"Błąd tłumaczenia: {e}")
        return tekst  # Zwróć oryginalny tekst w przypadku błędu

async def przetlumacz_plik(nazwa_pliku, sciezka_pliku, translator):
    with open(sciezka_pliku, 'r', encoding='utf-8') as plik:
        linie = plik.readlines()

    przetlumaczone_linie = []
    tekst_do_tlumaczenia = ""
    tlumaczenie_rozpoczęte = False

    for linia in linie:
        print(przetlumaczone_linie)
        if "Output:" in linia or "Hint:" in linia:
            if tlumaczenie_rozpoczęte:
                tlumaczenie_tekst = await przetlumacz_tekst(translator, tekst_do_tlumaczenia)
                przetlumaczone_linie.append(poprzedni_tag + ": " + tlumaczenie_tekst + "\n")
                tekst_do_tlumaczenia = ""
            poprzedni_tag = linia.split(":", 1)[0]
            tekst_do_tlumaczenia = linia.split(":", 1)[1].strip()
            tlumaczenie_rozpoczęte = True
        elif linia.endswith(":\n"):
            if tlumaczenie_rozpoczęte:
                tlumaczenie_tekst = await przetlumacz_tekst(translator, tekst_do_tlumaczenia)
                przetlumaczone_linie.append(poprzedni_tag + ": " + tlumaczenie_tekst + "\n")
                tekst_do_tlumaczenia = ""
                tlumaczenie_rozpoczęte = False
            przetlumaczone_linie.append(linia)
        elif tlumaczenie_rozpoczęte:
            tekst_do_tlumaczenia += "\n" + linia.strip()
        else:
            przetlumaczone_linie.append(linia)

    if tlumaczenie_rozpoczęte:
        tlumaczenie_tekst = await przetlumacz_tekst(translator, tekst_do_tlumaczenia)
        przetlumaczone_linie.append(poprzedni_tag + ": " + tlumaczenie_tekst + "\n")

    nazwa_pliku_tlumaczenie = "tlumaczenie_" + nazwa_pliku
    sciezka_pliku_tlumaczenie = os.path.join(os.path.dirname(sciezka_pliku), nazwa_pliku_tlumaczenie)  # Użyj os.path.dirname
    with open(sciezka_pliku_tlumaczenie, 'w', encoding='utf-8') as plik_tlumaczenie:
        plik_tlumaczenie.writelines(przetlumaczone_linie)
    print(f"Przetłumaczono plik: {nazwa_pliku} -> {nazwa_pliku_tlumaczenie}")

async def przetlumacz_pliki_txt(katalog):
    translator = Translator()
    tasks = []
    for nazwa_pliku in os.listdir(katalog):
        if nazwa_pliku.endswith(".yaml"):
            sciezka_pliku = os.path.join(katalog, nazwa_pliku)
            tasks.append(przetlumacz_plik(nazwa_pliku, sciezka_pliku, translator))
    await asyncio.gather(*tasks)

# Użycie funkcji
katalog = "."  # Zmień na ścieżkę do swojego katalogu

async def main():
    await przetlumacz_pliki_txt(katalog)

if __name__ == "__main__":
    asyncio.run(main())