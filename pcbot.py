from pprint import pprint
import os,re,random,json,nltk,time
from collections import OrderedDict, defaultdict, Counter
from gensim import corpora, models, similarities
from six import iteritems
import numpy as np

def intro():
    os.chdir("./inbox")
    ff = open("./messages.txt","w")
    for root, dirs, files in os.walk(".", topdown = False):
        for name in files:
            if(name == "message.json"):
                    print(os.path.join(root, name))
                    file = open(os.path.join(root, name) , 'r')
                    data = json.load(file)
                    count = 0;
                    length=len(data['messages'])
                    for piece in data['messages']:
                        if(piece["sender_name"]=='Pranav Chaudhari'):
                            if(data['messages'][length-1]["content"] != piece['content']):
                                cplusone=data['messages'][count+1]
                                if(cplusone["sender_name"]!='Pranav Chaudhari'):
                                    cplusone=data['messages'][count+1]["content"]
                                    if('photo' not in cplusone and 'sticker' not in cplusone ):
                                        ff.write(cplusone.lower()+"\n")
                                    if(piece["content"]!='You sent a photo.' and piece["content"]!='You sent a sticker.'):
                                        ff.write(piece["content"].lower()+"\n")
                        count = count+1
                    file.close()

#def cutit():
#    lines_seen = set() 
#    outfile = open("cleanmessages.txt", "w+")
#    for line in open("messages.txt", "r"):
#        if line not in lines_seen: 
#            outfile.write(line)
#            lines_seen.add(line)
#    outfile.close()


def similarityM():
    stoplist = set('a'.split()) #for a of the and to in
    texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1
    texts = [[token for token in text if frequency[token] > 1] for text in texts]
    dictionary = corpora.Dictionary(texts)
    dictionary.save('/tmp/large.dict')
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('/tmp/corpus.mm', corpus)
 
def make_pairs(corpus):
    for i in range(len(corpus)-1):
        yield (corpus[i], corpus[i+1])

def wwdictionary(pairs):
    for word_1, word_2 in pairs:
        if word_1 in word_dict.keys():
            word_dict[word_1].append(word_2)
        else:
            word_dict[word_1] = [word_2]
def checkme(check):
    sett=[]
    for i in pairs:
        if(i["question"]==check):
            sett.append(i["answer"])
    return random.choice(sett)
def catchthis(onetwo):
    chain=[]
    #print(documents[onetwo[0]])
    sss=checkme(documents[onetwo[0]])
    chain.append(sss.split()[0])
    length=random.randint(1, 15)
    for i in range(length):
        try:
            chain.append(random.choice(word_dict[chain[-1]]))
        except(KeyError):
            return print(' '.join(chain))
    print(' '.join(chain))


def query(onetwo):
    if(re.search(r"(?i)^hello$",onetwo) or re.search(r"(?i)^hi$",onetwo)):
        print("Hi!\n")
        return
    elif(re.search(r"(?i)^name$",onetwo)):
        print("PC Bot!\n")
        return
    elif(re.search(r"(?i)^bye$",onetwo)):
        print("Bye!\n")
        time.sleep(2)
        print("You're still here? Use \" quit \" to leave!\n")
        return
    elif(re.search(r"(?i)how do you work",onetwo)):
        print("I use Pranav's Facebook Messenger data from June 2015 to December 2015. To process questions - we use gensim - a package in python to convert Strings to Vectors, and transform those Vectors,  from a set of words into a lower dimensionality space. We then compare the string input by the user, convert to a vector and compare it to the previous corpus, to check which answer set to start the Markov Chain with. Then we take the first word of the set, and generate the rest of the sentence using a Markov chain.\n")
        return
    dictionary = corpora.Dictionary.load('/tmp/large.dict')
    corpus = corpora.MmCorpus('/tmp/corpus.mm')
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=30)    
    index = similarities.MatrixSimilarity(lsi[corpus])
    vec_bow = dictionary.doc2bow(onetwo.lower().split())
    vec_lsi = lsi[vec_bow]
    sims = index[vec_lsi]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    catchthis(random.choice(sims[0:10]))

#
#
#
#
#
#intro()
#cutit()


data = open("./my_messages.txt").read()
data1 = data.split()
pairss = make_pairs(data1)
word_dict = {}
wwdictionary(pairss)



ff = open("./messages.txt","r")
q = True
count = 0
pairs=[]
c = {}
for s in ff:
    #bigrm = list(nltk.bigrams(s.split()))
    if(q):
        q = False
        c['question']=s
    else:
        q= True
        #if(bigrm==[]):
        c['answer']=s
        #else:
        #    c['answer']=s#bigrm
        pairs.append(c)
        c={}

documents=[]
for s in pairs:
    documents.append(s['question'])
"""
This gets us a list of questions to compare the user input to, so we can look at which answer example we need to generate from
"""

similarityM()


print(" .----------------.  .----------------.  .----------------.  .----------------.  .----------------.")
print("| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |")
print("| |   ______     | || |     ______   | || |   ______     | || |     ____     | || |  _________   | |")
print("| |  |_   __ \   | || |   .' ___  |  | || |  |_   _ \    | || |   .'    `.   | || | |  _   _  |  | |")
print("| |    | |__) |  | || |  / .'   \_|  | || |    | |_) |   | || |  /  .--.  \  | || | |_/ | | \_|  | |")
print("| |    |  ___/   | || |  | |         | || |    |  __'.   | || |  | |    | |  | || |     | |      | |")
print("| |   _| |_      | || |  \ `.___.'\  | || |   _| |__) |  | || |  \  `--'  /  | || |    _| |_     | |")
print("| |  |_____|     | || |   `._____.'  | || |  |_______/   | || |   `.____.'   | || |   |_____|    | |")
print("| |              | || |              | || |              | || |              | || |              | |")
print("| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |")
print(" '----------------'  '----------------'  '----------------'  '----------------'  '----------------' ")
print(" est(2015-2015) ")


print("How are you doing?")
print("As always, quit to say goodbye.")
print()
user_response = input()
while not re.search(r"(?i)quit",user_response):
    user_response=user_response.lower()
    query(user_response)
    user_response = input()