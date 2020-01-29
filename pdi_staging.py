# Importing all the essential attributes and storing them in lists first

# Using untangle -> Sticking to untangle because working with Python objects
# is much easier.
import untangle
import string
from fuzzywuzzy import fuzz
import itertools
from constant import *

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


obj = untangle.parse("cddb_1000.xml")
artist = []
title = []
category =[]
genre =[]
Year = []

n = len(obj.cddb.disc)
# Initial check to see untangle functions as needed
# print(f"Total length: {n}, Title of first disc: {len(obj.cddb.disc[n-1].dtitle)}")
disc_list = obj.cddb.disc
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

# print(f"Artist: {len(artist)}, Title: {len(title)}, Category: {len(category)}, Genre: {len(genre)}, Year: {len(Year)} ")

# Returns indexes of non-printable strings - Title, Artist, Genre
# Category has no non-printable strings - checked.
non_latin_list = set()

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

# Just an intermediate check
# print(f"Artists = {len(artist)}, Titles = {len(title)}, Categories = {len(category)}, Genres = {len(genre)}")

# print(disc_list[0].tracks.title[0].cdata)
disc_for_tracks = list()
tracks_list = list()


# Get all the tracks
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

# Diagnostic check
# for i in range(20,40):
#     print(f"Track number {i+1}")
#     print(disc_for_tracks[i])
#     print("\n")


stat = Extract(artist,genre,category,title,n,non_latin_list)

# Another diagnostic
# print(len(stat))   

# Get the scores - only once
# scores =[]
# for i in range(len(stat)):
#     for j in range(i + 1, len(stat)):
#         if i in non_latin_list or j in non_latin_list:
#             continue
#         else:
#             ratio = fuzz.token_sort_ratio(stat[i].lower(),stat[j].lower())
#             if ratio > 80:
#                 scores.append(i)
#                 scores.append(j)
#                 scores.append(ratio)
                
# print(scores)

# print(len(s1_scores))
# Length of scores list has reduced from 1833 to 729.

s1_pairs = list()

for ele1,ele2 in zip(range(0,len(s1_scores),3),range(1,len(s1_scores),3)):
    # Debugging purposes : view the strings compared
    #print(f" {stat[s1_scores[ele1]]} | {stat[s1_scores[ele2]]}")
    temp_list = []
    temp_list.append(s1_scores[ele1])
    temp_list.append(s1_scores[ele2])
    s1_pairs.append(temp_list)

# Stage 1 scores 

# print(s1_pairs)
# print(len(s1_pairs))

# Do the FuzzyWuzzy for the tracks comparing 1st ele. of each list in 
# s1_pairs to 2nd ele. in s1_pairs.

# For PP - how to iterate
# print(s1_pairs[0:5])
# for ele in zip(range(5),s1_pairs):
#     print(ele[1][0])

# Get the conce. strings for tracks to do the matching
# iterated = set()
# for ele in s1_pairs:
#     for index in ele:
#         iterated.add(index)

# print(len(iterated))    # is 399
# Compare tracks (had to be run only once)
# n_tracks_1 = 0
# n_tracks_2 = 0
# s2_scores = []
# for i,j in s1_pairs:
#     n_tracks_1 = len(disc_for_tracks[i])
#     n_tracks_2 = len(disc_for_tracks[j])
#     indv_scores = []
#     max_ratio = 0
#     for l in range(n_tracks_1):
#         for m in range(n_tracks_2):
#             ratio = fuzz.token_sort_ratio(disc_for_tracks[i][l].lower(),disc_for_tracks[j][m].lower())
#             indv_scores.append(ratio)
#             if(l==(n_tracks_1-1) and m == (n_tracks_2-1)):
#                 max_ratio = max(indv_scores)
#                 if max_ratio > 80:
#                     s2_scores.append(i)
#                     s2_scores.append(j)
#                     s2_scores.append(max_ratio)

for ele1,ele2 in zip(disc_for_tracks[1988],disc_for_tracks[7093]):
    print(f"{ele1} | {ele2} ")



# Get the [s2] scores - only once
# s2_scores =[]
# for i in range(len(stat)):
#     for j in range(i + 1, len(stat)):
#         if i in non_latin_list or j in non_latin_list:
#             continue
#         else:
#             ratio = fuzz.token_sort_ratio(stat[i].lower(),stat[j].lower())
#             if ratio > 80:
#                 s2_scores.append(i)
#                 s2_scores.append(j)
#                 s2_scores.append(ratio)
                
# print(len(s2_scores))
# With threshold at 80, gives us 147 confirmed records.