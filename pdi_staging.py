# Importing all the essential attributes and storing them in lists first

# Using untangle -> Sticking to untangle because working with Python objects
# is much easier.
import untangle
import string
from fuzzywuzzy import fuzz
import itertools
from constant import scores

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

print(len(scores))
# Length of scores list has reduced from 1833 to 729.


# Used to find how many discs have the same multi. attributes within a single CD.

# attridict = {"artist":0,"title":0,"cat":0,"genre":0,"Year":0}
# for i in range(n):
#     if len(disc_list[i].artist) > 1:
#         attridict["artist"] += 1
#     if len(disc_list[i].dtitle) > 1:
#         attridict["title"] += 1
#     if len(disc_list[i].category) > 1:
#         attridict["cat"] += 1
#     try:
#         if len(disc_list[i].genre) > 1:
#             attridict["genre"] += 1
#     except:
#         continue
#     try:
#         if len(disc_list[i].year) > 1:
#             attridict["Year"] += 1
#     except:
#         continue

# print(f"Multiple artist ele. : {attridict['artist']}")
# print(f"Multiple title ele. : {attridict['title']}")
# print(f"Multiple cat ele. : {attridict['cat']}")
# print(f"Multiple genre ele. : {attridict['genre']}")
# print(f"Multiple year ele. : {attridict['Year']}")

