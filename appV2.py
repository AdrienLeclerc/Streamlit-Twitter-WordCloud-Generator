import streamlit as st
from streamlit_tags import st_tags, st_tags_sidebar
import tweepy
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import numpy as np
import requests
import time
import matplotlib.pyplot as plt
from PIL import Image

consumer_key = 'Y0WzAmtM2p7wXZgATbWtKeHDX'
consumer_secret = 'S66YGP02mv389XJJtErXKGnTfbgT5n5hT563iuUS01gO9YV6sc'
access_token = '1450083013384097794-mFm1jJMmHFP9OzwMbjIOEExyQiz7oQ'
access_token_secret = 'lHEFpXKagUsslyHpRxYvUdX7UoL4WFHUair4oshFIcMqP'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth,wait_on_rate_limit=True)

def app():
    
    st.image("https://i.imgur.com/zsNsR6b.png")
    
    st.sidebar.image("https://i.imgur.com/P356Awy.png",width = 300)
    
    st.sidebar.title("Contenu du WordCloud")
    
    raw_text = st.sidebar.text_input("Nom du profil twitter dont vous souhaitez le Word Cloud (sans le @)","MichelleObama")
    
    max_tweets = st.sidebar.slider("Nombre de tweets utilisés pour générer le WordCloud (à partir du tweet le plus récent)", min_value = 100, max_value = 1000, value = 500, step = 50)
    
    max_words = st.sidebar.slider("Nombre maximum de mots présents dans le WordCloud", 50, 500, step = 10, value = 250) 
    
    min_word_length = st.sidebar.slider("Nombre de lettre minmum qu'un mot doit contenir pour apparaitre dans le WordCloud", min_value = 0, max_value = 30, value = 5, step = 1)
    
    
    keyword = st_tags_sidebar(
    label='Mots que vous ne souhaitez pas voir apparaitre dans le WordCloud',
    text='Entrée',
    value=['https'],
    suggestions=['five', 'six', 'seven', 
                 'eight', 'nine', 'three', 
                 'eleven', 'ten', 'four'],
    maxtags = 10,
    key='1')
       
    st.sidebar.title("Design du WordCloud")
    
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
    

    
    color = st.sidebar.color_picker('Couleur du background', '#FFFFFF')
 
    contour_color = st.sidebar.color_picker('Couleur du contour du mask', '#1DA1F2')

    contour_width = st.sidebar.slider("Taille du contour du mask", 0, 20, 10, 1)    
    
    
    posts = api.user_timeline(screen_name = raw_text, count = max_tweets, lang = "en", tweet_mode = "extended")
    
    def load_data():
        df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])
        return df
    
    df = load_data()


    st.spinner(text = "Votre WordCloud se génère !")

    
    def gen_wordcloud():
        
        allWords = ' '.join([twts for twts in df['Tweets']])
        stopwords = set(STOPWORDS)
        stopwords.update(keyword)
        
        wordCloud = WordCloud(mask = mask,
                              contour_width = contour_width,
                              contour_color = contour_color,
                              min_word_length = min_word_length,
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
        st.subheader("Voici les derniers tweets de @" + raw_text)
        st.dataframe(df)
    
    st.sidebar.title("Téléchargement")
    
    with open("WC.jpg", "rb") as file:
           btn = st.sidebar.download_button(
            label="Téléchargez votre WordCloud !",
            data=file,
            file_name= "WordCloud.jpg",
            mime="image/jpg"
            )
    
    
    
if __name__ == "__main__":
	app()
