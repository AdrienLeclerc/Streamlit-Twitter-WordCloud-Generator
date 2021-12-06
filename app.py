import streamlit as st
from streamlit_tags import st_tags, st_tags_sidebar
import tweepy
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import numpy as np
import re
import requests
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns

consumer_key = 'Y0WzAmtM2p7wXZgATbWtKeHDX'
consumer_secret = 'S66YGP02mv389XJJtErXKGnTfbgT5n5hT563iuUS01gO9YV6sc'
access_token = '1450083013384097794-mFm1jJMmHFP9OzwMbjIOEExyQiz7oQ'
access_token_secret = 'lHEFpXKagUsslyHpRxYvUdX7UoL4WFHUair4oshFIcMqP'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth,wait_on_rate_limit=True)

def app():
    
    st.image("https://i.imgur.com/zsNsR6b.png",width = 700)
    
    st.sidebar.image("https://i.imgur.com/P356Awy.png",width = 300)
    
    raw_text = st.sidebar.text_input("Veuillez entrer le nom du profil twitter dont vous souhaitez le Word Cloud (sans le @)","MichelleObama")
    
    keyword = st_tags_sidebar(
    label='Si vous souhaitez ajouter des stopwords, cest par ici',
    text='Entrée',
    value=['https', 't','co'],
    suggestions=['five', 'six', 'seven', 
                 'eight', 'nine', 'three', 
                 'eleven', 'ten', 'four'],
    maxtags = 10,
    key='1')
    
    color = st.sidebar.color_picker('Choisissez une couleur pour le background', '#FFFFFF')
    
    st.sidebar.image("https://i.imgur.com/mIjkzbH.png",width = 300)   
    
    mask_choice = st.sidebar.selectbox('Choix du mask',('Bird', 'Hashtag','t','Smiley','Cercle'))
    
    if mask_choice == 'Bird' : mask = np.array(Image.open(requests.get("https://i.imgur.com/zLctdKZ.png", stream = True).raw))
    if mask_choice == 'Hashtag' : mask = np.array(Image.open(requests.get("https://i.imgur.com/jxQkCst.png", stream = True).raw))
    if mask_choice == 't' : mask = np.array(Image.open(requests.get("https://i.imgur.com/Ee79lQ8.png", stream = True).raw))
    if mask_choice == 'Smiley' : mask = np.array(Image.open(requests.get("https://i.imgur.com/4VL1aO8.png", stream = True).raw))
    if mask_choice == 'Cercle' : mask = np.array(Image.open(requests.get("https://i.imgur.com/NjhTA1d.png", stream = True).raw))
    
    mask_inverted = st.sidebar.radio('Voulez-vous inverser le mask?',('Non','Oui'))
    
    if mask_inverted == 'Oui' :
        if mask_choice == 'Bird' : mask = np.array(Image.open(requests.get("https://i.imgur.com/T4yt8OI.png", stream = True).raw))
        if mask_choice == 'Hashtag' : mask = np.array(Image.open(requests.get("https://i.imgur.com/Ts2kXpQ.png", stream = True).raw))
        if mask_choice == 't' : mask = np.array(Image.open(requests.get("https://i.imgur.com/iI6rI80.png", stream = True).raw))
        if mask_choice == 'Smiley' : mask = np.array(Image.open(requests.get("https://i.imgur.com/WcpaEad.png", stream = True).raw))
        if mask_choice == 'Cercle' : mask = np.array(Image.open(requests.get("https://i.imgur.com/ZK2E0zu.png", stream = True).raw))
    
    contour_width = st.sidebar.slider("Veuillez choisir la taille du contour du mask", 0, 20, 10, 1)
    
    contour_color = st.sidebar.color_picker('Choix de la couleur du contour du mask', '#1DA1F2')
    
    max_words = st.sidebar.slider("Veuillez choisir le nombre maximum de mots présents dans ce WordCloud", 50, 500, step = 10, value = 250) 
   
    width = st.sidebar.slider("Veuillez choisir la largeur du WorCloud souhaité",100,1000, step = 50, value = 500)
   
    height = st.sidebar.slider("Veuillez choisir la hauteur du WorCloud souhaité",100,1000, step = 50, value = 500)
    
    posts = api.user_timeline(screen_name = raw_text, count = 100, lang = "en", tweet_mode = "extended")
    df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])
    allWords = ' '.join([twts for twts in df['Tweets']])
    stopwords = set(STOPWORDS)
    stopwords.update(keyword)

    
    def gen_wordcloud():
        
        
        wordCloud = WordCloud(width=width,
                              height=height,
                              mask = mask,
                              contour_width = contour_width,
                              contour_color = contour_color,
                              background_color = color,
                              random_state=21,
                              max_font_size=110,
                              max_words = max_words,
                              stopwords = stopwords).generate(allWords)
        
        plt.imshow(wordCloud, interpolation="bilinear")
        plt.axis('off')
        plt.savefig('WC.jpg')
        img= Image.open("WC.jpg") 
        return img
    
    img = gen_wordcloud()
    
    st.image(img)

    
    if st.sidebar.checkbox("Montrer les tweets", False):
        st.subheader("Voici les tweets")
        st.write(df)
    
    with open("WC.jpg", "rb") as file:
           btn = st.sidebar.download_button(
            label="Téléchargez votre WordCloud !",
            data=file,
            file_name= "WordCloud.jpg",
            mime="image/jpg"
            )
    
    
    
if __name__ == "__main__":
	app()