import requests
from bs4 import BeautifulSoup
from finanzamtseite_infos2 import parse_einzelnes_finanzamt2

base_url = "https://www.lohnsteuer-kompakt.de"
start_url = f"{base_url}/start//finanzaemter/28/baden-wuerttemberg"

response = requests.get(start_url)
soup = BeautifulSoup(response.text, "html.parser")


# Alle Links zu Finanzämtern finden
finanzamt_links = []
for a in soup.select("a[href^='/finanzaemter/']"):
    href = a.get("href")
    if href not in finanzamt_links:
        finanzamt_links.append(base_url + href)

finanzamt_links=list(set(finanzamt_links)) # dopplte Einträge löschen



for i in finanzamt_links: #restliche doppelte Einträge löschen
    if i == "https://www.lohnsteuer-kompakt.de/finanzaemter/51/nordrhein-westfalen_" or i == "https://www.lohnsteuer-kompakt.de/finanzaemter/91/bayern_":
        finanzamt_links.remove(i)





# Liste mit den URLs der Bundesländer aus finanzamt_links:
bundesland_urls = {
    "sachsen": "https://www.lohnsteuer-kompakt.de/finanzaemter/32/sachsen",
    "bayern": "https://www.lohnsteuer-kompakt.de/finanzaemter/91/bayern",
    "sachsen-anhalt": "https://www.lohnsteuer-kompakt.de/finanzaemter/31/sachsen-anhalt",
    "brandenburg": "https://www.lohnsteuer-kompakt.de/finanzaemter/30/brandenburg",
    "berlin": "https://www.lohnsteuer-kompakt.de/finanzaemter/11/berlin",
    "thueringen": "https://www.lohnsteuer-kompakt.de/finanzaemter/41/thueringen",
    "hamburg": "https://www.lohnsteuer-kompakt.de/finanzaemter/22/hamburg",
    "niedersachsen": "https://www.lohnsteuer-kompakt.de/finanzaemter/23/niedersachsen",
    "schleswig-holstein": "https://www.lohnsteuer-kompakt.de/finanzaemter/21/schleswig-holstein",
    "mecklenburg-vorpommern": "https://www.lohnsteuer-kompakt.de/finanzaemter/40/mecklenburg-vorpommern",
    "baden-wuerttemberg": "https://www.lohnsteuer-kompakt.de/finanzaemter/28/baden-wuerttemberg",
    "rheinland-pfalz": "https://www.lohnsteuer-kompakt.de/finanzaemter/27/rheinland-pfalz",
    "nordrhein-westfalen": "https://www.lohnsteuer-kompakt.de/finanzaemter/51/nordrhein-westfalen",
    "saarland": "https://www.lohnsteuer-kompakt.de/finanzaemter/10/saarland",
    "bremen": "https://www.lohnsteuer-kompakt.de/finanzaemter/24/bremen",
    "hessen": "https://www.lohnsteuer-kompakt.de/finanzaemter/26/hessen"

}

#jetzt durchsuchen wir die seiten der länder nach den links zu ihren finanzämtern

BASE_URL = "https://www.lohnsteuer-kompakt.de"

alle_links = {}

for name, url in bundesland_urls.items():
    print(f"Verarbeite {name}...")

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    finanzamt_links = []
    for link in soup.select('ul.pfeile li a'):
        relative_link = link.get("href")
        full_url = BASE_URL + relative_link
        finanzamt_links.append(full_url)

    alle_links[name] = finanzamt_links

#jetzt haben wir ein dictionary mit den bundesländer als keys und eine liste der finanzamtlinks als values

for (Bundesland,Finanzämter) in alle_links.items():
    alle_links[Bundesland]=list(set(alle_links[Bundesland])) #doppelte Einträg löschen

#checken wieviele Finanzämter pro Bundesland
for (Bundesland,Finanzämter) in alle_links.items():

    print("Anzahl Finanzämter in ", Bundesland, ": ",len(Finanzämter))


# jetzt mit dem scrapen der Finanzamtseiten beginnen
gesamtzahl=0
Alle_Daten=[]
for (Bundesland,Finanzämter) in alle_links.items():
    gesamtzahl += len(Finanzämter)  # checkt Anzahl Finanzämter
    print(Bundesland, " gescrapt")
    for url in Finanzämter:
        Alle_Daten.append(parse_einzelnes_finanzamt2(url)) #erstellt eine Liste mit einem dict für jedes Finanzamt, welches
                                                                    # durch die parse funktion mit infos gefüllt wird

print("Anzahl Finanzämter: ",gesamtzahl)
print(len(Alle_Daten)) # sollte gleich mit gesamtzahl sein

#Endprodukt is die Alle_Daten liste, diese muss jetzt noch zur excel gemacht  oder anders verarbeitet werden