from PIL import Image
import streamlit as st
from streamlit import caching
import pandas as pd
import json
import os
import wallpaper_gen
import utils
st.set_option("deprecation.showfileUploaderEncoding", False)
import pickle
import numpy as np

st.markdown("""
# Fire Emblem Heroes Phone Wallpaper Generator

Create phone wallpapers for your favourite Fire Emblem heroes!

If you're interested in the code, you can find it on my GitHub repository [here](https://github.com/Ze1598/feh-wallpaper-generator).

For feedback, feel free to reach out to me on Twitter [@ze1598](https://twitter.com/ze1598).
""")


@st.cache
def load_pickle():
    """Load the main CSV of operator names, promotion images' URLs and theme colors.
    This function exists so the data can be cached.
    """
    # Load pickle with hero arts
    pickle_path = os.path.join("static", "data", "unit_arts.pickle")
    with open(pickle_path, "rb") as f:
        data = pickle.load(f)

    # DF of hero alt and their list of arts    
    data = pd.DataFrame({
        "heroAlt": list(data.keys()),
        "arts": list(data.values())
    })
    # Column with the unique hero that alt belongs to
    data["hero"] = data["heroAlt"].map(lambda hero_alt: hero_alt.split(":")[0])
    # Sort the DF by alphabetical order of unique heroes
    data.sort_values(by="hero", inplace=True)

    return data


# Reset all app caches
# caching.clear_cache()
# Load the necessary data and sort it by alphabetical order of names
main_data = load_pickle()

# Dropdown to filter by operator rank
hero_chosen = st.selectbox(
    "Choose the hero",
    main_data["hero"].unique().tolist()
)

filtered_data = main_data.query(f"hero == '{hero_chosen}'")

hero_alt_chosen = st.selectbox(
    "Choose the hero alt",
    filtered_data["heroAlt"].tolist()
)

hero_alt_arts = filtered_data.query(f'heroAlt == "{hero_alt_chosen}"').iloc[0]["arts"]
# By default, the foreground art is the portrait art
foreground_art = hero_alt_arts[0]
# By default, the background art is the special art
background_art = hero_alt_arts[2]

art_titles = ["Portrait", "Attack", "Special", "Damage"]
hero_art_dict = dict()
for i, title in enumerate(hero_alt_arts):
    if i <= 3:
        art_title = art_titles[i]
        hero_art_dict[art_title] = hero_alt_arts[i]
    else:
        art_title = f"{art_titles[i-4]} (Resplendent)"
        hero_art_dict[art_title] = hero_alt_arts[i]

# Choose the fore and background art individually
foreground_art = st.selectbox(
    "Which art do you want in the front?",
    list(hero_art_dict.keys())
)
background_art = st.selectbox(
    "Which art do you want in the back?",
    list(hero_art_dict.keys())
)

# Upload a custom background image for the wallpaper
custom_bg_img = st.file_uploader(
    "You can upload a custom background image to replace the default black one with 640x1280 dimensions (otherwise it is resized)", 
    type=["png", "jpg"]
)
# Save the uploaded image (deleted from the server at the end of the script)
if custom_bg_img != None:
    custom_bg_name = "custom_bg_img.png"
    custom_bg_path = os.path.join("static", "resources", custom_bg_name)
    pil_custom_bg_img = Image.open(custom_bg_img).resize((640, 1280)).save(custom_bg_path)

# Change the operator theme color
# Using the beta version until the generally available version is fixed in Streamlit 
#custom_op_color = st.color_picker("Feel free to change the operator theme color", "#4F80B8")
custom_op_color = st.beta_color_picker("Feel free to change the operator theme color", "#4F80B8")


# Get the url for fore and background art
fg_art_url = hero_art_dict[foreground_art]
bg_art_url = hero_art_dict[background_art]

# Create the image name string
wallpaper_name = hero_chosen + ".png"
wallpaper_name = "Unknown.png" if ("???" in wallpaper_name) else wallpaper_name
wallpaper_bg_path = custom_bg_path if custom_bg_img != None else ""


# Generate the wallpaper
wallpaper_gen.main(
    wallpaper_name,
    fg_art_url,
    bg_art_url,
    wallpaper_bg_path,
    custom_op_color
)
# Display the wallpaper
st.image(wallpaper_name, use_column_width=True)

# Encode the image to bytes so a download link can be created
encoded_img = utils.encode_img_to_b64(wallpaper_name)
href = f'<a href="data:image/png;base64,{encoded_img}" download="{wallpaper_name}">Download the graphic</a>'
# Create the download link
st.markdown(href, unsafe_allow_html=True)

# Delete the graphic from the server
os.remove(wallpaper_name)
try:
    os.remove(custom_bg_path)
except:
    pass