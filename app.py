import streamlit as st
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns
import base64
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize,word_tokenize


consumer_key = ####################
consumer_secret = #########################
access_key = ############################
access_secret = ##########################


auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_key,access_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)






def app():
	#st.title('Tweet Analysis')
	


	img = Image.open("ana.jpg")
	
	st.image(img,width=200)
	
	activity = ['Tweet Analyzer','Generate CSV']

	choice = st.sidebar.selectbox("Select What to want",activity)

	if choice == 'Tweet Analyzer':

		html_temp1 = """
		<div style="background-color:#FFE4C4;padding:10px">
		<h3 style="color:#0080ff;text-align:center;">Analysis Tweets</h3>
		</div>
		"""
		st.markdown(html_temp1,unsafe_allow_html=True)
		st.subheader('Enter Username (without @) :')
		#st.write('Most Recent Tweets')
		#st.write('Word Cloud')
		#st.write('Bar Graph')

		text = st.text_input('')

		user_choice = st.selectbox("Select Option",['Recent Tweet','WordCloud','View Data and Download','Visualize types of comments'])

		if st.button('Analysis'):

			if user_choice == 'Recent Tweet':
				st.success('Fetching Recent Tweets')

				def show_recent(text):

					posts = api.user_timeline(screen_name=text,count=100,lang='en',tweet_mode='extended')

					def get_tweet():
						l=[]
						i=1
						for tw in posts[:5]:
							l.append(tw.full_text)
							i=i+1

						return l 
						
					recent_tweet = get_tweet()
					return recent_tweet

				recent_tweet = show_recent(text)
				
				st.write(recent_tweet)


			elif user_choice == 'WordCloud':
				st.success('Generating Cloud')
				def gen_cloud():
					posts = api.user_timeline(screen_name=text,count=100,lang='en',tweet_mode='extended')

					df =pd.DataFrame([tw.full_text for tw in posts],columns=['Tweets'])	
					all_words = ' '.join([tw for tw in df['Tweets']])
					wordCloud = WordCloud(width=500, height=300, random_state=21, max_font_size=110).generate(all_words)
					plt.imshow(wordCloud,interpolation='bicubic')
					plt.axis('off')
					plt.savefig('WC.jpg')
					plt.show()
					img = Image.open('WC.jpg')
					return img 

				img = gen_cloud()
				
				st.image(img)


			elif user_choice == 'View Data and Download':
				def get_csv():
					st.success("Generating CSV and Downloading Link")
					posts = api.user_timeline(screen_name=text,count=100,lang='en',tweet_mode='extended')
					df =pd.DataFrame([tw.full_text for tw in posts],columns=['Tweets'])

					def cleanTxt(textt):

						textt = re.sub('@[A-Za-z0–9]+', '', textt) #Removing @mentions
						textt = re.sub('#', '', textt) # Removing '#' hash tag
						textt = re.sub('RT[\s]+', '', textt) # Removing RT
						textt = re.sub('https?:\/\/\S+', '', textt) # Removing hyperlink

						return textt 

					df['Tweets'] = df['Tweets'].apply(cleanTxt)

					def getSub(textt):
						return TextBlob(textt).sentiment.subjectivity

					def getpolar(textt):
						return TextBlob(textt).sentiment.polarity	

					df['Subjectivity'] = df['Tweets'].apply(getSub)
					df['Polarity'] = df['Tweets'].apply(getpolar)	


					def getanlysis(score):
						if score<0:
							return 'Negative'
						elif score == 0:
							return 'Neutral'
						else: 
							return 'Positive' 

					df['Analysis'] = df['Polarity'].apply(getanlysis)


					
					
					return df 


				df = get_csv()
				st.write(df)
				def get_link():
					data = df

					csv = data.to_csv(index=False)
					b64 = base64.b64encode(csv.encode()).decode()


					return f'<a href="data:file/csv;base64,{b64}" download="xyz.csv">Download csv file</a>'

				st.markdown(get_link(),unsafe_allow_html=True)



			else: 
				def Plot_Analysic():
					st.success("Generating Visualisation for Sentiment Analysis")
					posts = api.user_timeline(screen_name=text,count=100,lang='en',tweet_mode='extended')
					df =pd.DataFrame([tw.full_text for tw in posts],columns=['Tweets'])

					def cleanTxt(textt):

						textt = re.sub('@[A-Za-z0–9]+', '', textt) #Removing @mentions
						textt = re.sub('#', '', textt) # Removing '#' hash tag
						textt = re.sub('RT[\s]+', '', textt) # Removing RT
						textt = re.sub('https?:\/\/\S+', '', textt) # Removing hyperlink

						return textt 

					df['Tweets'] = df['Tweets'].apply(cleanTxt)

					def getSub(textt):
						return TextBlob(textt).sentiment.subjectivity

					def getpolar(textt):
						return TextBlob(textt).sentiment.polarity	

					df['Subjectivity'] = df['Tweets'].apply(getSub)
					df['Polarity'] = df['Tweets'].apply(getpolar)	


					def getanlysis(score):
						if score<0:
							return 'Negative'
						elif score == 0:
							return 'Neutral'
						else: 
							return 'Positive' 

					df['Analysis'] = df['Polarity'].apply(getanlysis)
					
					return df 

				df = Plot_Analysic()	

				st.write(sns.countplot(x=df["Analysis"],data=df))
				#st.write(sns.pie(x=df["Analysis"],data=df))
				st.pyplot(use_container_width=True)


	else: 
		html_temp4 = """
		<div style="background-color:#FFE4C4;padding:10px">
		<h3 style="color:#0080ff;text-align:center;">Analysis Using NLP</h3>
		</div>
		"""
		st.markdown(html_temp4,unsafe_allow_html=True)
		st.subheader('Click On button to get data from web')
		if st.button('Web Scrapping'):
			st.success('Scrapping Done')
			status = st.radio("See data",("Data","Hide Data"))
			if status == 'Data':
				def web_data():
					htmlfile = open('Reserve Bank of India - Speeches.html',encoding="utf8").read()
					soup = BeautifulSoup(htmlfile)
					for speech_text_1 in soup.findAll(attrs={'class' : 'tablecontent2'}):
						speech_text_1 = speech_text_1.text.strip()


						lines = (line.strip() for line in speech_text_1.splitlines())

						chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

						speech_1 = '\n'.join(chunk for chunk in chunks if chunk)

					return speech_1
			speech = web_data()	

			st.write(speech)

		elif st.button('Tokenize'):
			def tokenn(spee):
				a = word_tokenize(spee)

				return a 
			
			token = tokenn(speech)
			st.write(token)	

			

		#if st.button('Tokanize data'):
						










if __name__ =='__main__':
	app()




				






				






