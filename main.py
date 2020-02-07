########## INITIAL MODULES/PACKAGES USED ################
import untangle
import string
from fuzzywuzzy import fuzz
import itertools
import sys
from xml.sax.saxutils import escape
import progressbar
from time import sleep
import threading

############ GLOBAL INITIALIZATIONS ############
artist = []
title = []
category =[]
genre =[]
Year = []
non_latin_list = set()
disc_for_tracks = list()
s1_pairs = list()
s2_pairs = list()
s1_scores = list()
s2_scores = list()



######### FUNCTIONS ################


def makes1Pairs():
    for ele1,ele2 in zip(range(0,len(s1_scores),3),range(1,len(s1_scores),3)):
        temp_list = []
        temp_list.append(s1_scores[ele1])
        temp_list.append(s1_scores[ele2])
        s1_pairs.append(temp_list)
        

def getAndStoreTrackScores():
    print("Generating Stage 2 track scores! \n")
    n_tracks_1 = 0
    n_tracks_2 = 0
    scores = []
    for i,j in s1_pairs:
        n_tracks_1 = len(disc_for_tracks[i])
        n_tracks_2 = len(disc_for_tracks[j])
        indv_scores = []
        max_ratio = 0
        for l in range(n_tracks_1):
            for m in range(n_tracks_2):
                ratio = fuzz.token_sort_ratio(disc_for_tracks[i][l].lower(),disc_for_tracks[j][m].lower())
                indv_scores.append(ratio)
                if(l==(n_tracks_1-1) and m == (n_tracks_2-1)):
                    indv_scores.sort(reverse=True)
                    max_ratio = sum(indv_scores[0:5])/5
                    if max_ratio > 80:
                        scores.append(i)
                        scores.append(j)
                        scores.append(max_ratio)
    print("Generation complete! Writing to file ... ")
    f = open("constant.txt", 'a')
    f.write('\n')
    f.write(str(scores))
    f.close()
    print("Writing to file complete!")

def makes2Pairs():
    for ele1,ele2 in zip(range(0,len(s2_scores),3),range(1,len(s2_scores),3)):
        # Debugging purposes : view the strings compared
        #print(f" {stat[s1_scores[ele1]]} | {stat[s1_scores[ele2]]}")
        temp_list = []
        temp_list.append(s2_scores[ele1])
        temp_list.append(s2_scores[ele2])
        s2_pairs.append(temp_list)

def workPDLists(obj,n):
    multi_str = list()
    for i in range(n):
        if len(disc_list[i].artist) > 1:
            temp = ""
            for art in disc_list[i].artist:
                multi_str.append(art.cdata)
            for ele in multi_str:
                temp += str(ele)
            artist.append(temp)
            multi_str.clear()
        else:
            artist.append(str(disc_list[i].artist.cdata))
        if len(disc_list[i].dtitle) > 1:
            temp = ""
            for tit in disc_list[i].dtitle:
                multi_str.append(tit.cdata)
            for ele in multi_str:
                temp += str(ele)
            title.append(temp)
            multi_str.clear()
        else:
            title.append(str(disc_list[i].dtitle.cdata))
        category.append(str(disc_list[i].category.cdata))
        try:
            genre.append(str(disc_list[i].genre.cdata))
        except:
            genre.append("NaN")
        try:
            Year.append(str(disc_list[i].year.cdata))
        except:
            Year.append("NaN")



def Extract(a,g,cat,title,n,nlt_list):
    tot_string_list = []
    for i in range(n):
        if i in non_latin_list:
            tot_string_list.append("NA")
        else:
            single_str = ""
            if g[i] == "NaN":
                g[i] = ""
            if cat[i] == "NaN":
                cat[i] = ""
            single_str = str(a[i]) + str(title[i]) + str(g[i]) + str(cat[i])
            tot_string_list.append(single_str)
    return tot_string_list 


def workLatinChar():
    for i,tit in enumerate(title):
        for char in tit:
            if char not in string.printable or tit.count("?") == len(tit) or tit.count("!") == len(tit):
                non_latin_list.add(i)
    for i,tit in enumerate(artist):
        for char in tit:
            if char not in string.printable or tit.count("?") == len(tit) or tit.count("!") == len(tit):
                non_latin_list.add(i)
    for i,tit in enumerate(genre):
        for char in tit:
            if char not in string.printable or tit.count("?") == len(tit) or tit.count("!") == len(tit):
                non_latin_list.add(i)
    # Delete (or to be clear, reset) the attributes for which we have weird characters
    for i in range(n):
        if i in non_latin_list:
            artist[i] = "NA"
            title[i] = "NA"
            category[i] = "NA"
            genre[i] = "NA"
    count = 0
    for i in range(n):
        if title[i] != "NA":
            count += 1

def genTracks():
    # Get all the tracks
    tracks_list = list()
    for i in range(n):
        if i not in non_latin_list:
            tracks_list = []
            if len(disc_list[i].tracks.title) == 0:
                    tracks_list.append(str(disc_list[i].tracks.title.cdata))
            else:
                for j in range(len(disc_list[i].tracks.title)):    
                        tracks_list.append(str(disc_list[i].tracks.title[j].cdata))
            disc_for_tracks.append(tracks_list)
        else:
            disc_for_tracks.append(['NA'])

def getAndStoreScores(stat,threshold):
    bar = progressbar.ProgressBar(maxval=100, \
        widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    updater = 0
    scores =[]
    for i in range(len(stat)):
        for j in range(i + 1,len(stat)):
            # print(f"{i}")
            if i % 96 == 0 and i != 0 and j == len(stat)-1:
                updater += 1
                try:
                    bar.update(updater)
                except:
                    break
                sleep(0.1)
            if i in non_latin_list or j in non_latin_list:
                continue
            else:
                ratio = fuzz.token_sort_ratio(stat[i].lower(),stat[j].lower())
                if ratio > threshold:
                    scores.append(i)
                    scores.append(j)
                    scores.append(ratio)
    print("\n \n",flush=True) 
    print("Score updating complete!")
    print("\n",flush=True)                
    f = open("constant.txt", "w")
    f.write(f"# Scores of stage 1 and stage 2 (with threshold {threshold}%) along with the paired indexes of stage 1 and stage 2.")
    f.write('\n')
    f.write(str(scores))
    f.close()
    


############ GLOBAL POINT ######################
try:
    entr_thresh = int(sys.argv[1])
except:
    entr_thresh = 80
# Get databases from root 
obj = untangle.parse("databases/cddb_1000.xml")
disc_list = obj.cddb.disc
n = len(obj.cddb.disc)
workPDLists(obj,n)
workLatinChar()
genTracks()
stat = Extract(artist,genre,category,title,n,non_latin_list)
generateNewConstant = False
try:
    f1 = open("constant.txt")
    initline = str(f1.readline()).split()[10].rstrip('%)')
    if int(initline) == entr_thresh:
        generateNewConstant = False
    else:
        generateNewConstant = True
    f1.close()
except IOError:
    generateNewConstant = True 
if generateNewConstant:
    print("Generating scores for the first time.")
    print("Be patient. This might take some minutes ... \n",flush = True)
    getAndStoreScores(stat,entr_thresh)
f_main = open("constant.txt", "r")
f_main.readline()
s1_scores = f_main.readline()
s1_scores = s1_scores.lstrip('[').rstrip(']\n').split(',')
for i in range(len(s1_scores)):
    try:
        s1_scores[i] = int(s1_scores[i].strip())
    except:
        s1_scores[i] = float(s1_scores[i].strip())
f_main.close()
makes1Pairs()
getAndStoreTrackScores()
f_main = open("constant.txt", "r")
f_main.readline()
f_main.readline()
s2_scores = f_main.readline()
s2_scores = s2_scores.lstrip('[ ').rstrip(']\n ').split(',')
for i in range(len(s2_scores)):
    try:
        # s2_scores[i] = int(s2_scores[i].strip())
        print("It's an integer.")
    except:
        try:
            s2_scores[i] = float(s2_scores[i].strip())
            print("It's an integer.")
        except ValueError:
            print("It's something else")

f_main.close()
makes2Pairs()
sys.exit()

#################### REFERENCE CHECKING #########################

CRED = '\033[34m'
CEND = '\033[0m'

obj2 = untangle.parse("databases/ref_dups.xml")
titlepairs = []
n2 = len(obj2.cddups.pair)
# print(n2)
multi_str = list()

# Forming list of titles from xml
disc_list = obj2.cddups.pair
for i in range(n2):
    titlespairs = []
    for j in range(2):
        if len(disc_list[i].disc[j].dtitle) > 1:
            temp = ""
            for tit in disc_list[i].disc[j].dtitle:
                multi_str.append(tit.cdata)
            for ele in multi_str:
                temp += str(ele)
            titlespairs.append(temp)
            multi_str.clear()
        else:
            titlespairs.append(str(disc_list[i].disc[j].dtitle.cdata))
        if j == 1:
            titlepairs.append(titlespairs)

# Remove trailing/leading spaces 
for i in range(len(titlepairs)):
    for k in range(len(titlepairs[i])):
        titlepairs[i][k] = titlepairs[i][k].lstrip().rstrip() 

print("Performing reference check!")
print('-'*20)
print('\n')
print('Stage 1 results: ' + '\n')

correct = 0
non_repeat = list()
s1_titles = list()

for ele in s1_pairs:
    templist = []
    templist.append(title[ele[0]])
    templist.append(title[ele[1]])
    s1_titles.append(templist)

print(CRED+f"Using a threshold of {entr_thresh}% on matching primary data"+CEND)
print(f"Number of scored [Stage 1] records: {len(s1_titles)}")

repeat = []

for i in range(len(s1_titles)):
    for k in range(len(titlepairs)):
        if k not in repeat:
            if s1_titles[i][0] == titlepairs[k][0]:
                if s1_titles[i][1] == titlepairs[k][1]:
                    correct += 1
                    repeat.append(k)
                else:
                    pass
            elif s1_titles[i][0] == titlepairs[k][1]:
                if s1_titles[i][1] == titlepairs[k][0]:
                    correct += 1
                    repeat.append(k)
                else:
                    pass
            else:
                pass

print(CRED+f"For Stage 1: "+CEND)
print(f"The correct duplicates are {correct} of number, out of a total of {len(titlepairs)*2} ")
print(f"Gives us the success % of {(((correct/(len(titlepairs)*2))*100))}")

correct = 0
non_repeat = list()
s2_titles = list()

for ele in s2_pairs:
    templist = []
    templist.append(title[ele[0]])
    templist.append(title[ele[1]])
    s2_titles.append(templist)

print(CRED+f"Using a threshold of {entr_thresh}% on matching primary data"+CEND)
print(f"Number of scored [Stage 2] records: {len(s2_titles)}")

repeat = []

for i in range(len(s2_titles)):
    for k in range(len(titlepairs)):
        if k not in repeat:
            if s2_titles[i][0] == titlepairs[k][0] and s2_titles[i][1] == titlepairs[k][1]:
                    correct += 1
                    # print(f"{s2_titles[i][0]} | {titlepairs[k][0]} | {correct}")
                    repeat.append(k)
            elif s2_titles[i][0] == titlepairs[k][1] and s2_titles[i][1] == titlepairs[k][0]:
                    correct += 1
                    # print(f"{s2_titles[i][0]} | {titlepairs[k][1]} | {correct}")
                    repeat.append(k)
            else:
                pass

print(CRED+f"For Stage 2: "+CEND)
print(f"The correct duplicates are {correct} of number, out of a total of {len(titlepairs)*2} ")
print(f"Gives us the success % of >{min((((correct/(len(titlepairs)*2))*100)),100)}%")
print(CRED+"We notice an irregularity at this point, (with a greater than 100% success)"+CEND)
print(CRED+""" -> It is because at this point, we don't notice semantic duplicates in pairs but
even in threes and fours. Such cases are anomalies in the the comparison we perform
between our probable records and the reference file.  """+CEND)
print(CRED+"One such example is the cd's with title 'Laundry Service' by 'Shakira'."+CEND)
print(CRED+">> This affects Stage 1 results too, with an overapproximation."+CEND)


