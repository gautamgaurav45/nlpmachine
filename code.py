import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer

def nltk_company(txt):
    custom_sent_tokenizer=PunktSentenceTokenizer(txt)
    tokenized=custom_sent_tokenizer.tokenize(txt)
    company=[]
    try:
        for i in tokenized:
            words=nltk.word_tokenize(i)
            tagged=nltk.pos_tag(words)
            namedEnt=nltk.ne_chunk(tagged)
            #namedEnt.draw()
            for subtree in namedEnt.subtrees():
                if subtree.label() == 'ORGANIZATION':
                    company=np.append(company,subtree[0][0])
                    #print(subtree[0][0])        
    except Exception as e:
        print(str(e))
    return np.unique(company)


def getName(txt):
    try:
        text=txt.split(" ")
        text=text.remove("India") #removing word india
        txt=" ".join(text)
    except:
        txt=txt
    match = re.findall(r'[\w\.-]+\s+[\w\.-]+\s+[\w\.-]+@[\w\.-]+', txt)
    #print (match)
    authors=[]
    if len(match)>0: #if list is not empty
        for mail in range(len(match)):
            person= re.findall('[A-Z][a-z]+', match[mail])
            person=" ".join(person)
            authors=np.append(authors,person)
    return authors

def getInstitution(txt):
    instt=[]
    inst=re.findall(r'[\w\.-]*\s*[\w\.-]*\s*[\w\.-]*\sSecurities\s[\w\.-]*\s*[\w\.-]*\s*', txt)
    inst=np.append(inst,re.findall(r'[\w\.-]+\s+[\w\.-]+\s+[\w\.-]+\s+Technology\s+[\w\.-]+\s+[\w\.-]+\s+', txt))
    inst=np.append(inst,re.findall(r'[\w\.-]+\s+[\w\.-]+\s+[\w\.-]+\s+Research\s+[\w\.-]+\s+[\w\.-]+\s+', txt))
    #print(inst)
    if len(inst)>0: #if list is not empty
        for com in range(len(inst)):
            tmp= re.findall('[A-Z][A-Za-z]+', inst[com])
            tmp=" ".join(tmp)
            instt=np.append(instt,tmp)
    else:
        instt=np.append(instt,['Others'])
    return instt[0]

def getCompanies(txt):
    comp=re.findall(r'[\w\.-]+\s+[\w\.-]+\s+[\w\.-]+\s+[\w\.-]+\s+[\w\.-]+\sLtd', txt)
    comp=np.append(comp,re.findall(r'[\w\.-]+\s+[\w\.-]+\s+[\w\.-]+\s+[\w\.-]+\s[\w\.-]+\sLTD', txt))
    comp=np.append(comp,re.findall(r'[\w\.-]+\s+[\w\.-]+\s+[\w\.-]+\s+[\w\.-]+\s+[\w\.-]+\sLimited', txt))
    company=[]
    #print(comp)
    if len(comp)>0: #if list is not empty
        for com in range(len(comp)):
            #print(com)
            tmp= re.findall('[A-Z][A-Za-z]+', comp[com])
            tmp=" ".join(tmp)
            company=np.append(company,tmp)
    return np.unique(company)


def getinfo(txt,meta_auth):
    person=getName(txt)
    inst=getInstitution(txt)
    com=getCompanies(txt)
    com=np.append(com,nltk_company(txt))
    return person,inst,com

def code(file):
    pdfFileObj = open(file, 'rb')
    try:
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        if pdfReader.isEncrypted:
            pdfReader.decrypt("")
    except:
        return 'File not opened!','File not opened!','File not opened!'
    meta_auth=pdfReader.getDocumentInfo().author
    pages=pdfReader.getNumPages()  #returns number of pages
    auth='Nan'
    inst=[]
    comp=[]
    for i in range(pages):
        pageObj = pdfReader.getPage(i)
        try:
            txt=pageObj.extractText()
            if i==0:
                auth,inst,comp=getinfo(txt,meta_auth)
            else:
                comp=np.append(comp,getCompanies(txt))
                comp=np.append(comp,nltk_company(txt))
        except:
            continue
    return auth,inst,comp
    
import numpy as np
import re
import csv
import PyPDF2
from os import listdir

test_files = listdir("golden_dir")
csvData = ['File Name','Author','Institution','Company']
with open('output.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(csvData)
csvFile.close()
    
for fileName in test_files:
    auth,inst,comp=code('golden_dir/'+fileName)
    csvData = [str(fileName),str(auth),str(inst),str(comp)]
    with open('output.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(csvData)
    csvFile.close()
