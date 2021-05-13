import logging
from bs4 import BeautifulSoup
import requests
import pickle
import datetime
logging.basicConfig(level=logging.INFO)


def scrape_units():
    base_url = "https://feheroes.fandom.com"

    req = requests.get("https://feheroes.fandom.com/wiki/List_of_artists")
    soup = BeautifulSoup(req.content, "lxml", from_encoding="iso-8869-1")

    table_classes = "wikitable default sortable jquery-tablesorter".split()
    main_table = soup.find("table", class_=table_classes)
    table_rows = main_table.tbody.find_all("tr")

    units = dict()
    # First row is for the table headers
    for row in table_rows[1:]:
        row_columns = row.find_all("td")
        artist = row_columns[0].a.text
        # print(row_columns[1].div)
        for unit_div in row_columns[1].div.find_all("div"):
            unit_info = unit_div.a
            unit_name = unit_info["title"]
            unit_relative_url = unit_info["href"]
            unit_page = f"{base_url}{unit_relative_url}"
            if not unit_name.startswith("File"):
                units[unit_name] = unit_page
                #print(f"{unit_name}: {unit_page}")

    # Write this dictionary to a pickle file
    with open("units.pickle", "wb") as f:
        pickle.dump(units, f)
    logging.info(
        f"{datetime.datetime.now()}: Created pickle file with unit pages")


def scrape_art():

    # Load pickle of unit url pages
    with open("units.pickle", "rb") as f:
        unit_urls = pickle.load(f)
    

    #unit_urls = {"Hector": "https://feheroes.fandom.com/wiki/Hector:_General_of_Ostia"}

    art_dict = dict()
    # Get art for each unit
    for unit in unit_urls:
        logging.info(f"{datetime.datetime.now()}: Scraping art for {unit}")

        url = unit_urls[unit]
        req = requests.get(url)
        soup = BeautifulSoup(req.content, "lxml", from_encoding="iso-8869-1")

        # Get the table of unit information
        unit_info_table = soup.find("table", class_="wikitable hero-infobox")
        # The second row has the arts
        art_divs = unit_info_table.tbody.find_all("tr")[1]

        # List for this unit's art urls
        temp_urls = list()
        # In the div of art, look only for the anchors with art
        for art_anchor in art_divs.find_all("div")[0].find_all("a", class_="image"):
            #print(art_anchor.img)
            # Clean string to get the original art dimensions      
            art_relative_url = art_anchor.img["src"].split(".webp")[0] + ".webp"
            temp_urls.append(art_relative_url)
        
        # Add this unit's arts list to the running dictionary
        art_dict[unit] = temp_urls
    
    # Write this dictionary to a pickle file
    with open("unit_arts.pickle", "wb") as f:
        pickle.dump(art_dict, f)
    logging.info(
        f"{datetime.datetime.now()}: Created pickle file with unit arts")
    

if __name__ == "__main__":
    # scrape_units()
    # scrape_art()

    with open("unit_arts.pickle", "rb") as f:
        unit_arts = pickle.load(f)
    
    #print(set([k.split(":")[0] for k in unit_arts.keys()]))
    import numpy as np
    import pandas as pd
    print(np.unique(np.array([k.split(":")[0] for k in unit_arts.keys()])))
    print(pd.DataFrame({
        "heroe": list(unit_arts.keys()),
        "arts": list(unit_arts.values())
    }))