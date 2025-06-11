import pandas as pd
import openpyxl
from main import Alle_Daten

# list of dictonaries with the same keys gets turned into an excel file

# Einfacher Export direkt:
df = pd.DataFrame(Alle_Daten)

#  "bewertungen" ist ein dict im Dict, deswegen splitten wir es auf:
bewertungen_df = df['bewertungen'].apply(pd.Series)

# Dann die Bewertungen-Spalten an das Haupt-DataFrame anhängen:
df = pd.concat([df.drop(columns=['bewertungen']), bewertungen_df], axis=1)

# Excel-Datei speichern
df.to_excel("Finanzaemter_Bewertungen.xlsx", index=False)

print("Excel-Datei Finanzaemter_Bewertungen.xlsx wurde erstellt.")
