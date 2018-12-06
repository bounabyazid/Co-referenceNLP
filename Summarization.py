#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 16:05:59 2018

@author: Bounab Yazid
"""
import re

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk import pos_tag, word_tokenize

from stanfordcorenlp import StanfordCoreNLP
from nltk.tag import StanfordNERTagger

import numpy as np

import collections
import pandas as pd

from collections import Counter

#https://towardsdatascience.com/very-simple-python-script-for-extracting-most-common-words-from-a-story-1e3570d0b9d0
#https://medium.com/agatha-codes/using-textual-analysis-to-quantify-a-cast-of-characters-4f3baecdb5c

stopwords = stopwords.words('english')
wordcount = {}
PosList = []

#_______________________________________________________________

def TextFile_To_Sentences(TextFile):
    with open(TextFile, encoding="utf8") as f:
         text = f.read()
    sentences = sent_tokenize(text)
    return sentences
#_______________________________________________________________

def Read_TextFile(TextFile):
    with open(TextFile, encoding="utf8") as f:
         Text = f.read()
         f.close()
    punct = re.sub('[A-Za-z]|[0-9]|[\n\t]','',Text)
    SymbList = list(dict.fromkeys(punct).keys())
    #print (SymbList)
    return Text,SymbList
#_______________________________________________________________
    
def Preprocessing_Text(Text,punct):
    Text = re.sub('[0-9]+', ' ', Text)
    Text = Text.replace('é','e')
    for p in punct:
        Text = Text.replace(p,' ')
    
    Text = re.sub(' +',' ', Text)
    Text = Text.strip()
    #Text = Text.lower()
    #print (Text)
    return Text
#_______________________________________________________________

def Term_Frequecy(Text,punct):
    Text = Preprocessing_Text(Text,punct)
    for word in Text.lower().split():
        if word not in stopwords:
           if word not in wordcount:
              wordcount[word] = 1
           else:
                wordcount[word] += 1
    #print(wordcount)
#_______________________________________________________________

def Text_tokenize(Text):
    Tokens = word_tokenize(Text)
    return Tokens

def Tagging(Text):
    Tagged_Text = pos_tag(Text_tokenize(Text))
    return Tagged_Text
#_______________________________________________________________

def NE_Tagger(Text):
    st = StanfordNERTagger('/home/polo/Downloads/stanford-ner-2018-02-27/classifiers/english.all.3class.distsim.crf.ser.gz',
					       '/home/polo/Downloads/stanford-ner-2018-02-27/stanford-ner.jar', encoding='utf-8')

    tokenized_text = word_tokenize(Text)
    classified_text = st.tag(tokenized_text)

    #print(classified_text)
    return classified_text
#_______________________________________________________________
    
def find_proper_nouns(Tagged_Text):
    proper_nouns = []
    i = 0
    while i < len(Tagged_Text):
         if Tagged_Text[i][1] == 'NNP':
            if Tagged_Text[i+1][1] == 'NNP':
               proper_nouns.append(Tagged_Text[i][0].lower()+" " +Tagged_Text[i+1][0].lower())
               i+=1
            else:
                proper_nouns.append(Tagged_Text[i][0].lower())
         i+=1
    return proper_nouns

#_______________________________________________________________

def summarize_text(proper_nouns, top_num):
    counts = dict(Counter(proper_nouns).most_common(top_num))
    return counts

#_______________________________________________________________
    
def MainCharacter(Text,n_print):
    NER_Text = [(x.lower(), y) for x,y in NE_Tagger(Text)]
    NER_Text = dict(NER_Text)
    
    word_counter = collections.Counter(wordcount)

    return max(word_counter, key=word_counter.get)

#_______________________________________________________________

def SentsMainChar(sentences,MainChar):
    #but do the SRL before get sentences that contains the main Char
    MainSents = []
    for sent in sentences:
        if MainChar in sent:
           MainSents.append(sent)
    return MainSents

#_______________________________________________________________

def MostCommon(n_print,Tagged_Text):
    #Tagged_Text = [(x.lower(), y) for x,y in Tagged_Text]
    #PosList = set([X[1] for X in Tagged_Text])
    #print (PosList)
    #print (Tagged_Text)
    #Tagged_Text = dict(Tagged_Text)

    NER_Text = [(x.lower(), y) for x,y in NE_Tagger(Text)]
    NER_Text = dict(NER_Text)
    print (NER_Text)
    
    print("\nOK. The {} most common words are as follows\n".format(n_print))
    word_counter = collections.Counter(wordcount)
    #print(word_counter)
    for word, count in word_counter.most_common(n_print):
        #print(word, ": ", count, ": ",Tagged_Text[word])
        print(word, ": ", count, ": ",NER_Text[word])
    
    print('yazid and abhinay ',max(word_counter, key=word_counter.get))
        
#_______________________________________________________________

def DrawMostCommon(n_print):
    word_counter = collections.Counter(wordcount)
    lst = word_counter.most_common(n_print)
    df = pd.DataFrame(lst, columns = ['Word', 'Count'])
    df.plot.bar(x='Word',y='Count')

#_______________________________________________________________
    
Text,punct = Read_TextFile('Alan Turing.txt')
Precessed_Text = Preprocessing_Text(Text,punct)

Term_Frequecy(Precessed_Text,punct)
n_print = int(input("How many most common words to print: "))
DrawMostCommon(n_print)

print('____________________________________________________')

Tagged_Text = Tagging(Text)
#MostCommon(n_print,Tagged_Text)
MainChar = MainCharacter(Text,n_print)

sentences = TextFile_To_Sentences('Alan Turing.txt')

print ("\n".join(SentsMainChar(sentences,MainChar)))
#proper_nouns = find_proper_nouns(Tagged_Text)
#print (summarize_text(proper_nouns, 10))
