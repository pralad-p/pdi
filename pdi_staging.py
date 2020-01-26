# Importing all the essential attributes and storing them in lists first
import xml.etree.ElementTree as ET

tree = ET.parse('cddb_1000.xml')
root = tree.getroot()
artist = []
title = []
category =[]
genre =[]
tracks = []
Year = []
for disc in root.findall('disc'):
    artist.append(str(disc.find('artist').text))
    title.append(str(disc.find('dtitle').text))
    category.append(str(disc.find('category').text))
    try:
        genre.append(str(disc.find('genre').text))
    except:
        genre.append('0')
        continue
    try:
        Year.append(str(disc.find('year').text))
    except:
        Year.append('NaN')
        continue

print(f"Artist: {len(artist)}, Title: {len(title)}, Category: {len(category)}, Genre: {len(genre)}, Year: {len(Year)} ")

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

