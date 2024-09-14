import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
import numpy as np
from scipy import stats
f = open ('wordsim_relatedness_goldstandard.txt', 'r')
f1 = open ('wordsim_similarity_goldstandard.txt', 'r')
s = {f, f1}
c = 0
print('\t\t',"File name: wordsim_similarity_goldstandard.txt: ")
for x in s:
    c += 1
    l = list()
    l2 = list()
    l3 = list()
    brown_ic = wordnet_ic.ic('ic-brown.dat')
    for w in x:
        li = list()
        lines = w.split()
        li.append(lines)
        count = 0
        flG = 0
        for a in lines :
            syns = wn.synsets(a.lower())
            count += 1
            if (count == 3): 
                syns1 = syns
                break
            if (count == 1): syns1= syns
            elif (count == 2): 
                for i in range(min(len(syns1), len(syns))) :
                    if(syns1[i].pos() == syns[0].pos()):
                        flG = 1
                        syns1[0] = syns1[i]
                    elif (syns1[0].pos() == syns[i].pos()) : 
                        flG = 1
                        syns[0] = syns[i]
                    if (flG): 
                        break
                if (flG): 
                    li.append(["wup:", round(10*syns1[0].wup_similarity(syns[0]), 6)])
                    li.append( ["jcn:", round(10*syns1[0].jcn_similarity(syns[0] , brown_ic), 6)])
                    li.append([ "lch:", round(syns1[0].lch_similarity(syns[0]), 6)])
                elif (len(syns1)!=0 and len(syns)!=0): 
                    li.append(["wup:", round(10*syns1[0].wup_similarity(syns[0]), 6)])
                else: 
                    li.append(["one of these words no",0])
        l.append(li)
    l = sorted(l, key= lambda x: x[1][1], reverse = True)
    y1 = list()
    y  = list()
    for i in l:
        for j in i:
            for k in j:
                print(str(k).ljust(13), end = ' ')
            print(end='\t')
        print()   
    
        y1.append(np.array([round(float(i[0][2]))]))
        y.append(np.array([i[1][1]]))
    res = stats.spearmanr(y, y1)
    print("Мера Спирмана: ", res.statistic)
    if (c == 1):
     print('\t\t',"Next file name: wordsim_relatedness_goldstandard.txt ")
f.close()
f1.close()