import nltk
from nltk import bigrams
from nltk import trigrams
from nltk.corpus import stopwords
import re
import urllib

filename = "test.txt"

#Takes in a list of tokens and remove punctuation and numbers
#Return a list of tokens
def removePuncAndNum(tokens):   
    punctuation = re.compile(r'[-.?!,":;()|0-9]') 
    for i, token in enumerate(tokens):
        tokens[i] = punctuation.sub("", token)
        
        if token == "'s":
            tokens.pop(i)
            i -= 1
    return tokens

#Takes in a doc and returns the tokens
#return a list of tokens
def tokenize(s):
    tokens = nltk.word_tokenize(s)
    cleanup = [token.lower() for token in tokens if token.lower() not in stopwords.words('english') and len(token) > 1]
    return removePuncAndNum(cleanup)

#Opens the file and return string of text
#return string
def openFile(filename):
    text = " "
    f = open(filename,'r')
    while True:
        testline = f.readline()
        if len(testline) == 0:
            break
        text += testline
    return text


        
#------------------MAIN---------------------------------------------
html = urllib.urlopen("http://www.minecraftwiki.net/wiki/Blocks").read()
text2 = nltk.clean_html(html)
tokens2=tokenize(text2)
print [(tokens2.count(item), item) for item in sorted(set(tokens2)) if tokens2.count(item) > 5]

text = openFile(filename)
tokens = tokenize(text)
bi_tokens = bigrams(tokens)
tri_tokens = trigrams(tokens)

#print [(item,tokens.count(item)) for item in tokens if tokens.count(item) > 10]
sorted_Bi_Tokens = sorted(set(bi_tokens))
sorted_Tri_Tokens = sorted(set(tri_tokens))
print [(tokens.count(item), item) for item in sorted(set(tokens)) if tokens.count(item) > 5]
print [(sorted_Bi_Tokens.count(item), item) for item in sorted_Bi_Tokens if sorted_Bi_Tokens.count(item) > 0]
print [(sorted_Tri_Tokens.count(item), item) for item in sorted_Tri_Tokens if sorted_Tri_Tokens.count(item) > 0]

'''
text="""This is a test for the trigram. I do not know what it is doing"""
# split the texts into tokens
tokens = nltk.word_tokenize(text)
tokens = [token.lower() for token in tokens if len(token) > 1] #same as unigrams
bi_tokens = bigrams(tokens)
tri_tokens = trigrams(tokens)

# print trigrams count

print [(item, bi_tokens.count(item)) for item in sorted(set(bi_tokens))]
print [(item, tri_tokens.count(item)) for item in sorted(set(tri_tokens))]
'''