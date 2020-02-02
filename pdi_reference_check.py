import pdi_staging as p
from constant import s1_pairs,s2_pairs
import untangle

obj2 = untangle.parse("ref_dups.xml")
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

# print(f"Length of pair of duplicate titles: {len(titlepairs)}")

# Checking if scored elements in dupl. file (error calculation):
# Using only titles as checking var.

# for i in range(len(titledups)):
    # print(f"Dup. Title: {titledups[i]} | Dup. Artist: {artistdups[i]}")

# Remove trailing/leading spaces 
for i in range(len(titlepairs)):
    for k in range(len(titlepairs[i])):
        titlepairs[i][k] = titlepairs[i][k].lstrip().rstrip() 

# Stage 1
correct = 0
non_repeat = list()
s1_titles = list()

for ele in s1_pairs:
    templist = []
    templist.append(p.title[ele[0]])
    templist.append(p.title[ele[1]])
    s1_titles.append(templist)

print("Using a threshold of 80% on matching primary data")
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

print(f"For Stage 1: ")
print(f"The correct duplicates are {correct} of number, out of a total of {len(s1_titles)} ")
print(f"Gives us the success % of {(((correct/len(s1_titles))*100))}")

# Stage 2
correct = 0
non_repeat = list()
s2_titles = list()

for ele in s2_pairs:
    templist = []
    templist.append(p.title[ele[0]])
    templist.append(p.title[ele[1]])
    s2_titles.append(templist)

print("Using a threshold of 80% on matching primary data")
print(f"Number of scored [Stage 2] records: {len(s2_titles)}")

repeat = []

for i in range(len(s2_titles)):
    for k in range(len(titlepairs)):
        if k not in repeat:
            if s2_titles[i][0] == titlepairs[k][0] and s2_titles[i][1] == titlepairs[k][1]:
                    correct += 1
                    print(f"{s2_titles[i][0]} | {titlepairs[k][0]} | {correct}")
                    repeat.append(k)
            elif s2_titles[i][0] == titlepairs[k][1] and s2_titles[i][1] == titlepairs[k][0]:
                    correct += 1
                    print(f"{s2_titles[i][0]} | {titlepairs[k][1]} | {correct}")
                    repeat.append(k)
            else:
                pass

print(f"For Stage 2: ")
print(f"The correct duplicates are {correct} of number, out of a total of {len(s2_titles)} ")
print(f"Gives us the success % of >{min((((correct/len(s2_titles))*100)),100)}%")
print("We notice an irregularity at this point, (with a greater than 100% success)")
print(""" -> It is because at this point, we don't notice semantic duplicates in pairs but
even in threes and fours. Such cases are anomalies in the the comparison we perform
between our probable records and the reference file.  """)
print("One such example is the cd's with title 'Laundry Service' by 'Shakira'.")


