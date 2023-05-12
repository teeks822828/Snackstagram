import io
import openai
import random
import streamlit as st
from PIL import Image
import urllib
import requests
import pyttsx3

# ---- Constants ----
openai.api_key = "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"
dalle_api_key = "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"
headers = {"Authorization": f"Bearer {dalle_api_key}"}

# ---- Text-to-Speech ----
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.say(text)
    engine.runAndWait()

# ---- Recipe Generator ----
def generate_recipe(ingredients):
    prompt = f" Please return this exact list. Don't add extra text. Here is the list:{(ingredients)}. Can you make a nice unique recipe from those food ingredients - don't use other ingredients except for seasonings and other basic items people would have in their fridge or pantry"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

# ---- Image Generator ----
def generate_image(prompt):
    response = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers=headers,
        json={
            "model": "image-alpha-001",
            "prompt": prompt,
            "num_images": 1,
            "size": "1024x1024",
            "response_format": "url"
        }
    )
    if "data" in response.json():
        image_url = response.json()["data"][0]["url"]
        image_data = urllib.request.urlopen(image_url).read()
        image = Image.open(io.BytesIO(image_data))
        st.image(image, caption="", use_column_width=True)
        return image 

# ---- Streamlit App ----
def app():
    st.set_page_config(page_title="Snackstagam Recipe Generator", page_icon=":fork_and_knife:", layout="centered")
    st.title("Angry Chef's Recipe Generator")
    st.subheader("Enter up to 20 ingredients and generate a recipe!")
    ingredients = st.text_input("Enter Ingredients (comma-separated) e.g., tomatoes, eggs, milk", "")

    if st.button("Generate Recipe"):
        ingredients_list = [ing.strip() for ing in ingredients.split(",")]
        if len(ingredients_list) > 20:
            st.error("Please enter up to 20 ingredients only.")
        else:
            replies = ["CHOKE ON THIS YOU DORK!","YOUR DEMENTED GRANDMOTHER makes a better chef than you ever will","Here's what I came up with, YOU DONKEY OF A MULE:", "Voilà! Your recipe is ready, you hopeless amateur chef, I bet a 5-year-old cooks better than you:", "Congratulations, you've unlocked a new level of culinary disaster with this recipe:", "Hope you're hungry, because this recipe is gonna be amazing, not.","I'm not sure what you were going for, but this recipe is a real head-scratcher, you mad scientist of the kitchen:", "I've never tasted anything quite like this before. Your recipe is complete, you flavor adventurer:", "Congratulations, you've just invented a new kind of cuisine. It's called 'Awfukll', NOW GET TO WORK! Here's your recipe, you gastronomic pioneer:", "Here's what I came up with, you culinary craptastrophe:"]
            reply = random.choice(replies)
            recipe = generate_recipe(ingredients_list)
            generate_image(recipe)
            text_to_speech(reply)
            st.markdown(f'**{reply}** \n\n{recipe}', unsafe_allow_html=True)

# ---- Main ----
if __name__ == "__main__":
    app()

