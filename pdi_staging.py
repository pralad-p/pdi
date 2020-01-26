# Importing all the essential attributes and storing them in lists first

# Using untangle
import untangle

obj = untangle.parse("cddb_1000.xml")
artist = []
title = []
category =[]
genre =[]
Year = []

n = len(obj.cddb.disc)
print(f"Total length: {n}, Title of first disc: {len(obj.cddb.disc[n-1].dtitle)}")
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

print(f"Artist: {len(artist)}, Title: {len(title)}, Category: {len(category)}, Genre: {len(genre)}, Year: {len(Year)} ")



# Used to find the same multi. attributes within a single CD.

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


# for i in range(0,n+1):
#     artist.append(str(disc.find('artist').text))
#     title.append(str(disc.find('dtitle').text))
#     category.append(str(disc.find('category').text))
#     try:
#         genre.append(str(disc.find('genre').text))
#     except:
#         genre.append('0')
#         continue
#     try:
#         Year.append(str(disc.find('year').text))
#     except:
#         Year.append('NaN')
#         continue



# One way of doing it (Failed with Years tag - no 9763 elements)
# import xml.etree.ElementTree as ET

# tree = ET.parse('cddb_1000.xml')
# root = tree.getroot()
# artist = []
# title = []
# category =[]
# genre =[]
# tracks = []
# Year = []
# for disc in root.findall('disc'):
#     artist.append(str(disc.find('artist').text))
#     title.append(str(disc.find('dtitle').text))
#     category.append(str(disc.find('category').text))
#     try:
#         genre.append(str(disc.find('genre').text))
#     except:
#         genre.append('0')
#         continue
#     try:
#         Year.append(str(disc.find('year').text))
#     except:
#         Year.append('NaN')
#         continue

# print(f"Artist: {len(artist)}, Title: {len(title)}, Category: {len(category)}, Genre: {len(genre)}, Year: {len(Year)} ")

#make a function that looks throug 1 element in each list 
#and make a new string from these elements. 

# def Extract ():
#     listt=[]
#     newlist=[]
#     for x in range (50):
#         listt.append (artist[x])
#         listt.append (genre[x])
#         listt.append (year[x])
#         listt.append (category[x])
#         listt.append (title[x])
#         bla="".join(listt)
#         if (len(listt)%5)==0:
#             newlist.append(bla)
#             listt=[]
#     return newlist 
# stat = Extract()

# Using the FuzzyWuzzy module

# from fuzzywuzzy import fuzz
# import csv
# scores =[]
# fittedrecords=[]
# for x in range (10):
#     for i in range (10):
#         if x==i:
#             break
#         else: 
#             ratio = fuzz.token_set_ratio(stat[x].lower(),stat[i].lower())
#             if ratio > 56:
#                 scores.append(ratio)
#                 with open ('result_first_stage.csv',mode='w') as results:
#                     fieldnames = ['record_1','record_2','score']
#                     writer = csv.DictWriter(results, fieldnames=fieldnames)
#                     writer.writeheader()
#                     writer.writerow({'record_1': x,'record_2': i,'score': scores})
            
# print(scores)

