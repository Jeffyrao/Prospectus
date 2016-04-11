'''
Created on Apr 2, 2016

@author: jeffy
'''
import sys
import os
import re
import operator
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk import word_tokenize

def loadWordRoots(stemmer):
    dict = {}
    file = open('../wordroot.txt', 'r')
    index = 0
    duplicates = 0
    for line in file.readlines():
        word = stemmer.lemmatize(line.strip().lower())
        if word not in dict.keys():
            dict[word] = index
            index += 1
        else:
            duplicates += 1
            print('duplicate word:' + word)
    print('number of duplicates:' + str(duplicates) + ' dict size:' + str(len(dict.keys())))
    return dict

def writeNewWordRoots(dict):
    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1))
    file = open('../word_root_no_duplicates.txt', 'w')
    for word, index in sorted_dict:
        file.write(word+'\n')
    file.close()

def loadHTMLFileList():
    file = open('../html_file_list.txt', 'r')
    html_list = {}
    for line in file.readlines():
        html_list[line.strip()] = True
    file.close()
    return html_list

#### MAIN Function, Read From Here #######
if __name__ == "__main__": 
    stemmer = WordNetLemmatizer()
    # load word dictionary
    dict = loadWordRoots(stemmer)
    # remove duplicate word roots, and write the new dictionary into a file.
    writeNewWordRoots(dict)
    fileEmptyDict = {}
    # fileWordCounts: a table to store the word count lists,
    # its format is like: (filename, sec_name) -> list of word frequencies
    fileWordCounts = {}
    #htmlFileList = loadHTMLFileList()
    for filename in os.listdir("../sec_files/"):
        splits =  filename.split('_')
        # splits[1] = file name, splits[0] = section name
        fileWordCounts[splits[1]] = {}
        # initialize the word frequency list
        fileWordCounts[splits[1]][splits[0]] = [0]*len(dict.keys())
        file = open('../sec_files/'+filename, 'r')
        filestat = os.stat('../sec_files/'+filename)
        if filestat.st_size == 0: # empty file, skip
            print('empty file: ' + filename)
            fileEmptyDict[filename] = False
        if filename.endswith('.txt'):
            for line in file.readlines():
                line = unicode(line, errors='ignore')
                # splits each line to a list of words
                words = word_tokenize(line.lower())
                for word in words:
                    # lemmatize a word, i.e., likes -> like, trees -> tree
                    word_stem = stemmer.lemmatize(word)
                    if word_stem in dict:
                        fileWordCounts[splits[1]][splits[0]][dict.get(word_stem)] += 1
    newfile = open('../file_wordcounts.txt', 'w')
    for filename in fileWordCounts.keys():
        for sec in fileWordCounts[filename].keys():
            if sec+'_'+filename in fileEmptyDict: # skip empty file
                continue
            wordcount = fileWordCounts[filename][sec]
            # write normalized word counts to a new file
            newfile.write(filename + ',' + sec + ',')
            total = 0
            for count in wordcount:
                total += count
            for count in wordcount:
                frac = 0
                if total != 0: # normalize word frequency to its fraction
                    frac = count*1.0/total
                else:
                    print('zero counts: ' + filename)
                newfile.write(str(frac) + ' ')
            newfile.write('\n')
    newfile.close()   
                
                
                