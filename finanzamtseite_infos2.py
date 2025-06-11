from bs4 import BeautifulSoup
import requests
import re

# funktionen die mit try und except verhindern dass der code jedes mal abbricht wenn eine info nicht verfügbar ist
def safe_find_text(soup, tag, class_=None, default="N/A"):
    try:
        if class_:
            return soup.find(tag, class_=class_).text.strip()
        else:
            return soup.find(tag).text.strip()
    except:
        return default

def safe_find_attr(soup, tag, class_, attr, default="N/A"):
    try:
        return soup.find(tag, class_=class_)[attr]
    except:
        return default

def safe_re_search(pattern, text, group=1, default="N/A"):
    m = re.search(pattern, text)
    if m:
        return m.group(group)
    else:
        return default

def safe_find_all(soup, tag, class_=None):
    try:
        if class_:
            return soup.find_all(tag, class_=class_)
        else:
            return soup.find_all(tag)
    except:
        return []


# funktion die die einzelnen unterseiten über die jeweiligen Finanzämter dursucht und diese in ein dictionary abspeichert

def parse_einzelnes_finanzamt2(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")

    # 1. Finanzamtsnummer, Name, Bundesland
    text = safe_find_text(soup, "div", class_="medium-7 cell", default="")

    finanzamt_name = safe_re_search(r'Finanzamt ([^<]+)</strong>', str(soup.find("strong")), default="N/A")
    bundesland = safe_re_search(r'liegt im Bundesland ([^,]+),', text, default="N/A")
    nummer = safe_re_search(r'Bundesfinanzamtsnummer (\d+)', text, default="N/A")

    # 2. Adresse
    street = safe_find_text(soup, "span", class_="street-address")
    postal_code = safe_find_text(soup, "span", class_="postal-code")
    city = safe_find_text(soup, "span", class_="locality")

    # 3. Telefonnummer
    try:
        telefon = soup.find("span", class_="tel").find("span", class_="value").text.strip()
    except:
        telefon = "N/A"

    # 4. Website
    website = safe_find_attr(soup, "a", "url", "href")

    # 5. Gemeinden
    gemeinden_p = None
    try:
        gemeinden_p = soup.find("p", string=re.compile("Gemeinden des Finanzamt"))
    except:
        pass
    if gemeinden_p:
        try:
            gemeinden_text = gemeinden_p.find_next_sibling("p").text.strip()
            gemeinden_text = re.sub(r'<a.*', '', str(gemeinden_p.find_next_sibling("p")))
            gemeinden_list = [g.strip() for g in gemeinden_text.split(",") if g.strip()]
        except:
            gemeinden_list = []
    else:
        gemeinden_list = []

    # 6. Durchschnittliche Bearbeitungsdauer
    bearbeitungsdauer_tag = soup.find("span", class_="badge_bearbeitungszeit")
    if bearbeitungsdauer_tag:
        try:
            bearbeitungsdauer = bearbeitungsdauer_tag.find("b").text.strip()
        except:
            bearbeitungsdauer = "N/A"
    else:
        bearbeitungsdauer = "N/A"

    # 7. Bewertungen
    bewertungen = {}
    tables = safe_find_all(soup, "table", class_="stack unstriped")

    if tables and len(tables) > 0 and tables[0].find_all("span"):
        try:
            gesamt_note = tables[0].find_all("span")[0].text.strip()
        except:
            gesamt_note = "N/A"
    else:
        gesamt_note = "N/A"
    bewertungen["Gesamtnote"] = gesamt_note

    if tables and len(tables) > 1:
        try:
            for tr in tables[1].find_all("tr"):
                tds = tr.find_all("td")
                if len(tds) >= 2:
                    kategorie = tds[0].text.strip()
                    wert = tds[1].text.strip()
                    bewertungen[kategorie] = wert
        except:
            pass

    finanzamt = {
        "name": finanzamt_name,
        "nummer": nummer,
        "bundesland": bundesland,
        "adresse": (street, postal_code, city),
        "telefon": telefon,
        "website": website,
        "gemeinden": gemeinden_list,
        "bearbeitungsdauer": bearbeitungsdauer,
        "bewertungen": bewertungen
    }
    return finanzamt

