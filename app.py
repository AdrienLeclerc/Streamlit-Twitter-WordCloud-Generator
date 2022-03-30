import streamlit as st
from streamlit_tags import st_tags, st_tags_sidebar
import tweepy
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import numpy as np
import requests
import time
import plotly.express as px
#import flair
from afinn import Afinn
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import operator
import emoji
import re
import matplotlib.pyplot as plt
from PIL import Image

consumer_key = 'Y0WzAmtM2p7wXZgATbWtKeHDX'
consumer_secret = 'S66YGP02mv389XJJtErXKGnTfbgT5n5hT563iuUS01gO9YV6sc'
access_token = '1450083013384097794-mFm1jJMmHFP9OzwMbjIOEExyQiz7oQ'
access_token_secret = 'lHEFpXKagUsslyHpRxYvUdX7UoL4WFHUair4oshFIcMqP'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth,wait_on_rate_limit=True)

st.set_page_config(page_title = "Twitter WC & Sentiment Analysis",
                   page_icon = ":bird:",
                   layout = 'wide')

@st.cache
def cleaner(tweet):
    tweet = re.sub("@[A-Za-z0-9]+","",tweet) #Remove @ sign
    tweet = re.sub("RT :"," ", tweet)
    tweet = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", tweet) #Remove http links
    tweet = " ".join(tweet.split())
    tweet = ''.join(c for c in tweet if c not in emoji.UNICODE_EMOJI) #Remove Emojis
    tweet = tweet.replace("#", "").replace("_", " ") #Remove hashtag sign but keep the text
    return tweet


def app():
    
    st.sidebar.image("https://i.imgur.com/P356Awy.png",width = 300)
      
    raw_text = st.sidebar.text_input("Nom du profil (sans le @)","MichelleObama")

    choix = st.sidebar.selectbox("Que souhaitez vous faire?", options = ("WordCloud Generator", "Sentiment Analysis"))
    
    if choix == "WordCloud Generator" : 
        
        st.image("https://i.imgur.com/TEiII8N.png")
    
        max_tweets = st.sidebar.slider("Nombre de tweets utilisés pour générer le WordCloud (à partir du tweet le plus récent)", min_value = 50, max_value = 200, value = 100, step = 10)
        
        posts = api.user_timeline(screen_name = raw_text, count = max_tweets, lang = "en", tweet_mode = "extended")

        def load_data():
            df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])
            return df
    
        df = load_data()
        
        df['Tweets'] = df['Tweets'].map(lambda x: cleaner(x))
    
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
    
        st.sidebar.image("https://i.imgur.com/mIjkzbH.png")   
    
        mask_choice = st.sidebar.selectbox('Choix du mask',('Bird', 'Hashtag','t','Smiley','Cercle'))
    
        if mask_choice == 'Bird' : mask = np.array(Image.open("bird.png"))
        if mask_choice == 'Hashtag' : mask = np.array(Image.open(requests.get("https://i.imgur.com/D2Mqsye.png", stream = True).raw))
        if mask_choice == 't' : mask = np.array(Image.open(requests.get("https://i.imgur.com/DZWpWzB.png", stream = True).raw))
        if mask_choice == 'Smiley' : mask = np.array(Image.open(requests.get("https://i.imgur.com/goSy6mn.png", stream = True).raw))
        if mask_choice == 'Cercle' : mask = np.array(Image.open(requests.get("https://i.imgur.com/cdAig6T.png", stream = True).raw))
    
        mask_inverted = st.sidebar.radio('Voulez-vous inverser le mask?',('Non','Oui'))
    
        if mask_inverted == 'Oui' :
            if mask_choice == 'Bird' : mask = np.array(Image.open(requests.get("https://i.imgur.com/GShVxdM.png", stream = True).raw))
            if mask_choice == 'Hashtag' : mask = np.array(Image.open(requests.get("https://i.imgur.com/DdG6wF9.png", stream = True).raw))
            if mask_choice == 't' : mask = np.array(Image.open(requests.get("https://i.imgur.com/U1Lkoqc.png", stream = True).raw))
            if mask_choice == 'Smiley' : mask = np.array(Image.open(requests.get("https://i.imgur.com/DdyDbLB.png", stream = True).raw))
            if mask_choice == 'Cercle' : mask = np.array(Image.open(requests.get("https://i.imgur.com/FdVlYXH.png", stream = True).raw))
    

    
        color = st.sidebar.color_picker('Couleur du background', '#FFFFFF')
 
        contour_color = st.sidebar.color_picker('Couleur du contour du mask', '#1DA1F2')

        contour_width = st.sidebar.slider("Taille du contour du mask", 0, 20, 10, 1)    
    
    
        posts = api.user_timeline(screen_name = raw_text, count = max_tweets, lang = "en", tweet_mode = "extended")
    
        @st.cache
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
            plt.savefig('WC.png')
            img= Image.open("WC.png") 
            return img
    
        img = gen_wordcloud()
    
        st.image(img, use_column_width= True)
    
        if st.sidebar.checkbox("Montrer les tweets", False):
            st.subheader("Voici les derniers tweets de @" + raw_text)
            st.dataframe(df)
    
        st.sidebar.title("Téléchargement")
    
        with open("WC.png", "rb") as file:
            btn = st.sidebar.download_button(
            label="Téléchargez votre WordCloud !",
            data=file,
            file_name= "WordCloud.jpg",
            mime="image/png"
            )

    if choix == "Sentiment Analysis" : 
        
        st.image("https://i.imgur.com/cuUUlKD.png")
    
        max_tweets = st.sidebar.slider("Nombre de tweets utilisés pour réaliser le Sentiment Analysis (à partir du tweet le plus récent)", min_value = 50, max_value = 200, value = 100, step = 20)
        
        posts = api.user_timeline(screen_name = raw_text, count = max_tweets, lang = "en", tweet_mode = "extended")
        
        @st.cache
        def load_data_sentiment():
            df_sentiment = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])
            return df_sentiment
    
        df_sentiment = load_data_sentiment()
        
        df_sentiment['Tweets'] = df_sentiment['Tweets'].map(lambda x: cleaner(x))
        
        
        #Flair Sentiment Analysis
        #sentiment_model = flair.models.TextClassifier.load('en-sentiment')
        
        #probs = []
        #sentiments = []

        #for tweet in df_sentiment['Tweets'].to_list():
            # make prediction
            #sentence = flair.data.Sentence(tweet)
            #sentiment_model.predict(sentence)
            # extract sentiment prediction
            #probs.append(sentence.labels[0].score)  # numerical score 0-1
            #sentiments.append(sentence.labels[0].value)  # 'POSITIVE' or 'NEGATIVE'

        # add probability and sentiment predictions to tweets dataframe
        #df_sentiment['Flair_probability'] = probs
        #df_sentiment['Flair_sentiment'] = sentiments
        
        #Afinn Sentiment Analysis
        afinn = Afinn()
        afinn_scores = [afinn.score(text) for text in df_sentiment.Tweets]
        df_sentiment['Afinn_Score'] = afinn_scores
        df_sentiment["Afinn_sentiment"] = np.select([df_sentiment["Afinn_Score"] < 0, df_sentiment["Afinn_Score"] == 0, df_sentiment["Afinn_Score"] > 0],
                           ['NEGATIVE', 'NEUTRAL', 'POSITIVE'])
        
        #NLTK Sentiment Analysis
        sia = SentimentIntensityAnalyzer()
        df_sentiment["NLTK_score"] = df_sentiment["Tweets"].apply(lambda x: sia.polarity_scores(x)["compound"])
        df_sentiment["NLTK_sentiment"] = np.select([df_sentiment["NLTK_score"] < 0, df_sentiment["NLTK_score"] == 0, df_sentiment["NLTK_score"] > 0],
                           ['NEGATIVE', 'NEUTRAL', 'POSITIVE'])
        
        #TextBlob Sentiment Analysis
        df_sentiment["TextBlob_score"] = df_sentiment["Tweets"].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
        df_sentiment["TextBlob_sentiment"] = np.select([df_sentiment["TextBlob_score"] < 0, df_sentiment["TextBlob_score"] == 0, df_sentiment["TextBlob_score"] > 0],
                           ['NEGATIVE', 'NEUTRAL', 'POSITIVE'])
        
        df_sentiment['counter'] = 1
        

        
        df_sentiment_color = df_sentiment
        
        df_sentiment_color['Afinn_color'] = np.select([df_sentiment_color["Afinn_Score"] < 0, df_sentiment_color["Afinn_Score"] == 0, df_sentiment_color["Afinn_Score"] > 0], ['#F71D1D', '#CECECE', '#1DA1F2'])
        df_sentiment_color['NLTK_color'] = np.select([df_sentiment_color["NLTK_score"] < 0, df_sentiment_color["NLTK_score"] == 0, df_sentiment_color["NLTK_score"] > 0], ['#F71D1D', '#CECECE', '#1DA1F2'])       
        df_sentiment_color['TextBlob_color'] = np.select([df_sentiment_color["TextBlob_score"] < 0, df_sentiment_color["TextBlob_score"] == 0, df_sentiment_color["TextBlob_score"] > 0], ['#F71D1D', '#CECECE', '#1DA1F2'])
        
       
        
       
        col1, col2, col3 = st.columns(3)
        
        with col1 : 
            st.markdown("<h1 style='text-align: center;'>Afinn</h1>", unsafe_allow_html=True)
    
            afinn_pie = px.pie(df_sentiment_color, values = 'counter', names = 'Afinn_sentiment')
        
            afinn_pie.update_layout(
                       width = 320,
                       height = 350,
                       showlegend = False)
        
            afinn_pie.update_traces(textposition='inside',
                                        textinfo='percent+label',
                                        marker = dict(line = dict(color = '#FFFFFF', width = 1)),
                                        hole = 0.5,
                                        pull = 0.1,
                                        marker_colors = df_sentiment_color['Afinn_color'])

            st.plotly_chart(afinn_pie,use_column_width = True)

            
            afinn_histo = px.histogram(df_sentiment_color,
                                   x = 'Afinn_Score',
                                   #nbins = 25
                                   color = "Afinn_sentiment",
                                   color_discrete_map = {'NEGATIVE' : '#F71D1D', 'NEUTRAL' : '#CECECE', 'POSITIVE' : '#1DA1F2'})

        
            afinn_histo.update_layout(
                       width = 350,
                       height = 350,
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',
                       yaxis = dict(showgrid = False),
                       bargap = 0.2,
                       showlegend = False)
            
            st.plotly_chart(afinn_histo,use_column_width = True)
        
        
        with col2:
        
            st.markdown("<h1 style='text-align: center;'>NLTK</h1>", unsafe_allow_html=True)
            
            NLTK_pie = px.pie(df_sentiment_color, values = 'counter', names = 'NLTK_sentiment')
        
            NLTK_pie.update_layout(
                       width = 320,
                       height = 350,
                       showlegend = False)
        
            NLTK_pie.update_traces(textposition='inside',
                                        textinfo='percent+label',
                                        marker = dict(line = dict(color = '#FFFFFF', width = 1)),
                                        hole = 0.5,
                                        pull = 0.1,
                                        marker_colors = df_sentiment_color['NLTK_color'])
            
            st.plotly_chart(NLTK_pie,use_column_width = True)           
            
            NLTK_histo = px.histogram(df_sentiment_color,
                                   x = 'NLTK_score',
                                   #nbins = 25
                                   color = "NLTK_sentiment",
                                   color_discrete_map = {'NEGATIVE' : '#F71D1D', 'NEUTRAL' : '#CECECE', 'POSITIVE' : '#1DA1F2'})
                                   
        
            NLTK_histo.update_layout(
                       width = 350,
                       height = 350,
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',
                       yaxis = dict(showgrid = False),
                       bargap = 0.2,
                       showlegend = False)
            

            st.plotly_chart(NLTK_histo,use_column_width = True)
            
        with col3:
            
            st.markdown("<h1 style='text-align: center;'>TextBlob</h1>", unsafe_allow_html=True)

            TB_pie = px.pie(df_sentiment_color, values = 'counter', names = 'TextBlob_sentiment')
        
            TB_pie.update_layout(
                         width = 320,
                         height = 350,
                         showlegend = False)
        
            TB_pie.update_traces(textposition='inside',
                                        textinfo='percent+label',
                                        marker = dict(line = dict(color = '#FFFFFF', width = 1)),
                                        hole = 0.5,
                                        pull = 0.1,
                                        marker_colors = df_sentiment_color['TextBlob_color'])
            
            st.plotly_chart(TB_pie,use_column_width = True)            


            TB_histo = px.histogram(df_sentiment_color,
                                   x = 'TextBlob_score',
                                   #nbins = 25
                                   color = "TextBlob_sentiment",
                                   color_discrete_map = {'NEGATIVE' : '#F71D1D', 'NEUTRAL' : '#CECECE', 'POSITIVE' : '#1DA1F2'})
                                   
        
            TB_histo.update_layout(
                       width = 350,
                       height = 350,
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',
                       yaxis = dict(showgrid = False),
                       bargap = 0.2,
                       showlegend = False)
                

            st.plotly_chart(TB_histo,use_column_width = True)
            
        expander = st.expander("Voir les données")
        with expander:
            st.dataframe(df_sentiment)    
    
    
if __name__ == "__main__":
	app()
