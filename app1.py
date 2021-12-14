import streamlit as st
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import preprocessor as p
import nltk
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from PIL import Image

nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')

#Removing stopwords
stop = nltk.corpus.stopwords.words('spanish')


consumer_key = 'UjYQZT9P9vdYq6OzEFPsqSLQB'
consumer_secret = 'LWKnd023OSmb6kfTbDd5zPjo4P0LcQodvg1wRf7LynWCgOH8Nb'
access_token = '384431766-SdZnMYaETCYPiI6NyogMtZSEZq95dAYqZyDNkWhU'
access_token_secret = '5GD2CpP3Bt3ZvsCjiMV0LvkNnh5oBiJiEeJNW9lzdQ38o'

st.set_option('deprecation.showPyplotGlobalUse', False)
#p.set_options(p.OPT.URL, p.OPT.RESERVED,p.OPT.NUMBER,p.OPT.MENTION)

#Create the authentication object
authenticate = tweepy.OAuthHandler(consumer_key, consumer_secret) 
    
# Set the access token and access token secret
authenticate.set_access_token(access_token, access_token_secret) 
    
# Creating the API object while passing in auth information
api = tweepy.API(authenticate, wait_on_rate_limit = True)

    
def app():
    st.title("Tu año en Twitter 🔥")
    st.subheader("Veamos como fueron tus tweets durante el 20201")
    raw_text = st.text_area("Escribe tu nombre de usuario (sin la @)")

    if st.button("Analizar"):
        st.success("Analizando los últimos 100 tweets del 2021")
        
        def datos_usuario(raw_text):
            datos = api.get_user(raw_text) 
            st.write("Nombre: ",datos.name)
            st.write("Descripción: ",datos.description)    
            st.write("Seguidores:", datos.followers_count)
            st.write("Amigos:", datos.friends_count)
            
        def Show_Recent_Tweets(raw_text):
            # Extract 3200 tweets from the twitter user 
            posts = api.user_timeline(screen_name=raw_text, count =100 , lang ="es", tweet_mode="extended")

            
            l=[]
            i=1
            for tweet in posts:
                #l.append(p.clean(tweet.full_text))
                l.append(tweet.full_text)
                i= i+1
            
            return l
    
        recent_tweets= Show_Recent_Tweets(raw_text)
        st.success("¡LISTO!")
        
        st.subheader("Estos son tus datos")
        datos_usuario(raw_text)
        
        st.subheader("Palabras más usadas")
        
        
        
        def gen_wordcloud():
            # Create a dataframe with a column called Tweets
            df = pd.DataFrame([tweet for tweet in recent_tweets], columns=['Tweets'])
			# word cloud visualization
            allWords = ' '.join([twts for twts in df['Tweets']])
            wordCloud = WordCloud(width=700, height=500, random_state=21, max_font_size=110,stopwords=stop).generate(allWords)
            plt.imshow(wordCloud, interpolation="bilinear")
            plt.axis('off')
            plt.savefig('WC.jpg')
            img= Image.open("WC.jpg") 
            return img
        
        img=gen_wordcloud()
        st.image(img,width=700)
        


if __name__ == "__main__":
	app()