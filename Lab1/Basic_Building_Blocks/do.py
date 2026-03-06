import os
from googletrans import Translator

def przetlumacz_pliki_txt(katalog):
    translator = Translator()
    for nazwa_pliku in os.listdir(katalog):
        if nazwa_pliku.endswith(".yaml"):
            sciezka_pliku = os.path.join(katalog, nazwa_pliku)
            with open(sciezka_pliku, 'r', encoding='utf-8') as plik:
                linie = plik.readlines()

            przetlumaczone_linie = []
            tekst_do_tlumaczenia = ""
            tlumaczenie_rozpoczęte = False

            for linia in linie:
                print(przetlumaczone_linie)
                if "Output:" in linia  or "Hint:" in linia:
                    if tlumaczenie_rozpoczęte:
                        tlumaczenie = translator.translate(tekst_do_tlumaczenia, src='en', dest='pl')
                        print(tlumaczenie)
                        przetlumaczone_linie.append(poprzedni_tag + ": " + tlumaczenie.text + "\n")
                        tekst_do_tlumaczenia = ""
                    poprzedni_tag = linia.split(":", 1)[0]
                    tekst_do_tlumaczenia = linia.split(":", 1)[1].strip()
                    tlumaczenie_rozpoczęte = True
                elif linia.endswith(":\n"): # tagi typu "Nazwa:"
                    if tlumaczenie_rozpoczęte:
                        tlumaczenie = translator.translate(tekst_do_tlumaczenia, src='en', dest='pl')
                        przetlumaczone_linie.append(poprzedni_tag + ": " + tlumaczenie.text + "\n")
                        tekst_do_tlumaczenia = ""
                        tlumaczenie_rozpoczęte = False
                    przetlumaczone_linie.append(linia)
                elif tlumaczenie_rozpoczęte:
                    tekst_do_tlumaczenia += "\n" + linia.strip()
                else:
                    przetlumaczone_linie.append(linia)

            if tlumaczenie_rozpoczęte:
                tlumaczenie = translator.translate(tekst_do_tlumaczenia, src='en', dest='pl')
                przetlumaczone_linie.append(poprzedni_tag + ": " + tlumaczenie.text + "\n")

            nazwa_pliku_tlumaczenie = "tlumaczenie_" + nazwa_pliku
            sciezka_pliku_tlumaczenie = os.path.join(katalog, nazwa_pliku_tlumaczenie)
            with open(sciezka_pliku_tlumaczenie, 'w', encoding='utf-8') as plik_tlumaczenie:
                plik_tlumaczenie.writelines(przetlumaczone_linie)
            print(f"Przetłumaczono plik: {nazwa_pliku} -> {nazwa_pliku_tlumaczenie}")

# Użycie funkcji
katalog = "."  # Zmień na ścieżkę do swojego katalogu
przetlumacz_pliki_txt(katalog)