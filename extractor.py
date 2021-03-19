## Libraries for file management
from os import listdir
import pickle

## Libraries for data management
import numpy as np

## Libraries for website interactions
import urllib3
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer


def soupify(url):
    """Convert a html file via url into bs4 soup with urlib3 and bs4."""
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    html_doc = r.data
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup


def processing(text):
    """Tokenize a given string and create a dictionary. Return stats such as
    number of words, size of the dictionary, number of sentences. Also return
    the dictionary."""
    
    ## Tokenizing the text
    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(text.lower())

    ## Creating a dictionary of the token occurrences
    dictionary = {}
    for word in words:
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary[word] = 1

    ## Creating a list of sentences
    sentences = text.split(". ")
    
    return len(words), len(dictionary), len(sentences), dictionary


def extract(soup):
    """Extracts the text, title, date and categories of the article and then
    dumps it into the database stored in pickle file (overwriting the old version)."""
    
    passages = soup.find_all("p","text_3v_J6Y0G")
    text = " ".join([passage.text for passage in passages])
    text = text.replace('"','').replace("'","")
    
    date = soup.find_all("time")[-1]['datetime']
    categories = [x.text for x in soup.find_all("a", class_="link_2imnEnEf")]
    
    title = soup.find("h1","title_iP7Q1aiP").text
    for x in [".",",",":","/","•","'",'"',"?","*"]:
        title = title.replace(x,"")
    title = title.strip()
    
    w,d,s,dictionary = processing(text)
    
    if len(passages) != 0:
        arr = np.array([text, categories, dictionary, w, d, s], dtype=object)
        
        with open('article_database.pickle', 'rb+') as handle:
            db = pickle.load(handle)
            db[f"{date[:10]}_{title}"] = arr
            pickle.dump(db, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    return None


def scrape(link_categories):
    """Scrape the articles from a given list of categories on the NOS website."""
    
    handle = open('article_database.pickle', 'rb')
    db = pickle.load(handle)
    old_DB_size = len(db)
    handle.close()
    
    print("|",end="")
    for category in link_categories:
        ## Parse each category page
        soup = soupify(f"https://nos.nl/nieuws/{category}/")
        
        ## Find all of the articles and remove all liveblogs
        article_blocks = soup.find_all("a", class_="link-block list-items__link")
        article_links = [f"https://nos.nl{article['href']}" for article in article_blocks if "liveblog" not in article['href']]
        
        
        for link in article_links:
            soup = soupify(link)
            extract(soup)
        print(f" {category} |",end="")
        
    handle = open('article_database.pickle', 'rb')
    db = pickle.load(handle)
    new_DB_size = len(db)
    handle.close()
    
    return new_DB_size-old_DB_size, new_DB_size