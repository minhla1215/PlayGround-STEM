import lxml.html
import nltk
from nltk import bigrams
from nltk import trigrams
from nltk.corpus import stopwords
import re
import urllib
import pickle
import os

#----------------------------------functions-------------------------------------

#Takes in a list of tokens and remove punctuation and numbers
#Return a list of tokens
def removePuncAndNum(tokens):   
    punctuation = re.compile(r'[-?!,":;()|0-9]') 
    for i, token in enumerate(tokens):
        tokens[i] = punctuation.sub("", token)
        
        if tokens[i] == "'s":
            tokens.pop(i)
            i -= 1
        if tokens[i] == '':
            tokens.pop(i)
            i-=1
    return tokens

#Takes in a doc and returns the tokens
#return a list of tokens
def tokenize(s):
    tokens = nltk.word_tokenize(s)
    cleanup = [token.lower() for token in tokens if token.lower() not in stopwords.words('english') and len(token) > 1]
    return removePuncAndNum(cleanup)

#Opens the file and return string of text
#return string
def openFile(text,filename):
    f = open(filename,'r')
    while True:
        testline = f.readline()
        if len(testline) == 0:
            break
        text += testline
    f.close();
    return text

def openURL(text, url):
    try:
        html = urllib.urlopen(url).read()
        text += str(nltk.clean_html(html))
        return text
    except Exception, e:
        print e

def crawlURL(s_list,url):
    try:
        if(len(s_list) > 50):
            return
        root = lxml.html.fromstring(urllib.urlopen(url).read())
        links = root.cssselect("a")
        print "went in recursively " + url
        for link in links:
            test_link = str(link.get('href'))
            if(test_link.find("/wiki/") != -1 and test_link.find("wikipedia") == -1 and \
               test_link.find("/User:") == -1 and test_link.find("/File:") == -1 and \
               test_link.find("/User_talk:") == -1 and test_link.find("/Special") == -1 and \
               test_link.find("/Minecraft_Wiki") == -1 and test_link.find("/Template") == -1 and \
               test_link.find("/Version_history") == -1 and test_link.find("/Minecraft_Wiki_talk") == -1 and \
               test_link.find("/Category") == -1 and test_link.find("/Mods") == -1 and \
               test_link.find("/.minecraft") == -1 and test_link.find("/MediaWiki:") == -1 and \
               test_link.find("/MediaWiki_Talk:") == -1 and test_link.find("/Talk") == -1 and \
               test_link.find("/Upcoming_features") == -1):
                working_link = base_link + test_link
                #print working_link + "   " + test_link
                if(working_link not in s_list or len(s_list) == 0):
                    s_list.append(working_link)
                    crawlURL(s_list, working_link)
        return s_list          
    except Exception, e:
        print e
        pass  
    
#---------------------------End of Function-----------------------------------    
    
#Files and site to scrap
filename = "test.txt"
wiki = "http://www.minecraftwiki.net/wiki/Minecraft_Wiki"
base_link = "http://www.minecraftwiki.net"
site_list = []

#If the list of URL exists, open it. If not, create it
try:
    if os.path.exists("site_list.txt"):
        site_list = pickle.load(open("site_list.txt","rb"))
    else:
        site_list = crawlURL(site_list,wiki)
        pickle.dump(site_list,open("site_list.txt","wb"))
    print len(site_list)
except Exception, e:
    print e

        
#------------------MAIN---------------------------------------------

url_text = ""
url_tokens = None
#load the long list of text or makei t
try:
    if os.path.exists("url_text.txt"):
        #url_text = pickle.load(open("url_text.txt","rb"))
        url_text = pickle.load(open("url_text.txt","rb"))
        print("read")
    else:
        for site in site_list:
            url_text = openURL(url_text, site)
        pickle.dump(url_text,open("url_text.txt","wb"))
except Exception, e:
    print e

#load the tokens or make it

try:
        url_tokens = tokenize(url_text)
        url_bitokens = bigrams(url_tokens)
        url_tritokens = trigrams(url_tokens)
        fout = open("wikipedia_tokens.csv",'wb')
        for item in sorted(set(url_tokens)):
            if url_tokens.count(item) > 100:
                fout.write(item + "," + str(url_tokens.count(item)) + "\n")
        fout.close()
        fout = open("wikipedia_bitokens.csv",'wb')
        for item in sorted(set(url_bitokens)):
            if url_bitokens.count(item) > 80:
                fout.write(str(item) + "," + str(url_bitokens.count(item)) + "\n")
        fout.close()
        fout = open("wikipedia_tritokens.csv",'wb')
        for item in sorted(set(url_tritokens)):
            if url_tritokens.count(item) > 60:
                fout.write(str(item) + "," + str(url_tritokens.count(item)) + "\n")
        fout.close()
except Exception, e:
    print e

#print [(url_tokens.count(item), item) for item in sorted(set(url_tokens)) if url_tokens.count(item) > 100]

doc_text = ""
doc_text = openFile(doc_text,filename)
tokens = tokenize(doc_text)
bi_tokens = bigrams(tokens)
tri_tokens = trigrams(tokens)

#print [(item,tokens.count(item)) for item in tokens if tokens.count(item) > 10]
sorted_Bi_Tokens = sorted(set(bi_tokens))
sorted_Tri_Tokens = sorted(set(tri_tokens))
#print [(tokens.count(item), item) for item in sorted(set(tokens)) if tokens.count(item) > 5]
#print [(sorted_Bi_Tokens.count(item), item) for item in sorted_Bi_Tokens if sorted_Bi_Tokens.count(item) > 0]
#print [(sorted_Tri_Tokens.count(item), item) for item in sorted_Tri_Tokens if sorted_Tri_Tokens.count(item) > 0]
