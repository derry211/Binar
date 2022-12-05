# Import Library yang akan dibutuhkan dalam teks analitik
import pandas as pd
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from datetime import datetime
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns
from nltk.util import ngrams
from collections import defaultdict

from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
nltk.download('punkt')
nltk.download('wordnet')

# Happy Emoticons
emoticons_happy = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
    ])
 
# Sad Emoticons
emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ])

def data_cleaning(text):
    # menghilangkan html tag
    # Format html
    html_tag = re.compile(r'<.*?>')
    text = re.sub(html_tag, r'', text)

    # menghilangkan url
    # Format URL
    http_link = re.compile(r'https://\S+')
    www_link = re.compile(r'www\.\S+')
    text = re.sub(http_link, r'', text)
    text = re.sub(www_link, r'', text)

    # menghilangkan tanda baca
    # Tanda baca yang tidak diperlukan
    punctuation = re.compile(r'[^\w\s]')
    text = re.sub(punctuation, r'', text)

    #remove angka
    text = re.sub('[0-9]+', '', text)
    
    # remove stock market tickers like $GE
    text = re.sub(r'\$\w*', '', text)
 
    # remove old style retweet text "RT"
    text = re.sub(r'^RT[\s]+', '', text)
    
    # remove hashtags
    # only removing the hash # sign from the word
    text = re.sub(r'#', '', text)   

    # remove stock market tickers like $GE
    text = re.sub(r'\$\w*', '', text)
 
    # remove old style retweet text "RT"
    text = re.sub(r'^RT[\s]+', '', text)
 
    # remove hyperlinks
    text = re.sub(r'https?:\/\/.*[\r\n]*', '', text)
    
    # remove hashtags
    # only removing the hash # sign from the word
    text = re.sub(r'#', '', text)
    
    #remove coma
    text = re.sub(r',','',text)
    
    #remove angka
    text = re.sub('[0-9]+', '', text)
 
    # tokenize tweets
    # tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
    # text_tokens = tokenizer.tokenize(text)
 

    return text

#fungsi preprocessing
def prepros (data, name_column_dataset):
    data[name_column_dataset] = data[name_column_dataset].apply(lambda x: x.lower())
    data["remove_punc"] = data[name_column_dataset].apply(lambda x: data_cleaning(x))
    data["clean"] = data["remove_punc"].apply(lambda x: word_tokenize(x))

    start = datetime.now()
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    data["clean"] = data["clean"].apply(lambda x: " ".join(stemmer.stem(word) for word in x))
    end_stem = datetime.now()
    print ("stemmer done",(start-end_stem))

    factory = StopWordRemoverFactory()
    stopword = factory.create_stop_word_remover()
    data["clean"] = data["clean"].apply(lambda x: " ".join(stopword.remove(x) for x in x.split()))
    end_stop = datetime.now()
    print ("stopword done", (end_stop - end_stem))
    data["clean"] = data["clean"].apply(lambda x:re.sub(' +', ' ',x))

    return(data)

# def load_data():
#         data = pd.read_csv('indo_data50.csv')
#     return (data)