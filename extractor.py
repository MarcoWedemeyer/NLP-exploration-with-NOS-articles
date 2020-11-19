#!/usr/bin/env python
# coding: utf-8

# In[1]:


from os import listdir
import numpy as np
import matplotlib.pyplot as plt

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


def processing(text:str, verbose=False):
    """Tokenize a given string and create a dictionary. Return stats such as
    number of words, size of the dictionary, number of sentences. Also return
    the dictionary."""
    
    ## Tokenizing the text
    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(text.lower())
    if verbose: print(f"Number of words: {len(words)}")

    ## Creating a dictionary of the token occurrences
    dictionary = {}
    for word in words:
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary[word] = 1
    if verbose: print(f"Length of Dictionary: {len(dictionary)}")

    ## Creating a list of sentences
    sentences = text.split(". ")
    if verbose: print(f"Number of sentences: {len(sentences)}")
    
    return len(words), len(dictionary), len(sentences), dictionary


def extract(soup, save_file=False, verbose=False):
    """Extract the text, title, date and categories of the article. Optionally save
    the file."""
    
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

    if save_file:
        if len(passages) != 0:
            arr = np.array([text, categories, dictionary, w, d, s])
            np.save(f"articles\\{date[:10]}_{title}", arr)
            if verbose: print(f"Saved file under 'articles\\{date[:10]}_{title}.txt'")
    
    return None


def scrape(link_categories):
    """Text"""
    
    for category in link_categories:
        ## Parse each category page
        soup = soupify(f"https://nos.nl/nieuws/{category}/")
        
        ## Find all of the articles and remove all liveblogs
        article_blocks = soup.find_all("a", class_="link-block list-items__link")
        article_links = [f"https://nos.nl{article['href']}" for article in article_blocks if "liveblog" not in article['href']]
        
        print(f"{category:>16} |",end="")
        for link in article_links:
            soup = soupify(link)
            extract(soup, save_file=True)
            print("=",end="")
        print("|")
    print()
    return None

