# feh-wallpaper-generator [![Open in Streamlit](https://share.streamlit.io/ze1598/feh-wallpaper-generator)
[live app](https://share.streamlit.io/ze1598/feh-wallpaper-generator)

A web app built with [Streamlit](https://www.streamlit.io/) in Python to create Arknights mobile wallpapers on the fly.
The art was scraped from the [Fire Emblem Heroes Wikia](https://feheroes.fandom.com/wiki/List_of_artists) and images are loaded directly from their source. This scraping is done with with the [requests](https://pypi.org/project/requests/) and [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) libraries.
The default colors for each operator was done manually by me.

Simply choose your favorite heroe, the foreground and background artwork and the wallpaper will be generated on the fly. You can also change the wallpaper color for the heroe shadow and upload your own background to replace the default black one!