import math


database = dict()

database["name"] = []
print(database)
database['name'] += [["a", 3]]
database['name'] += [["b", 2]]
database['name'] += [["c", 3]]
database['name'] += [["d", 0]]
database['name'] += [["e", 0]]
database['name'] += [["f", 1]]
database['name'] += [["g", 2]]
database['name'] += [["h", 2]]
database['name'] += [["i", 3]]
database['name'] += [["j", 0]]


def calculateDCG(data):
    total = 0
    index = 0
    count = 0
    for item in data:
        count += 1
        index += 1
        relevanceNum = item[1]
        if index == 1:
            total += relevanceNum
        else:
            total += relevanceNum/math.log2(index)
        if count == 4: 
            break
    return total
        

def calculateNDCG75(database, queryName):
    DCG = calculateDCG(database[queryName])
    print("DCG: ", DCG)
    database[queryName].sort(key=lambda x: x[1], reverse=True)
    IDCG = calculateDCG(database[queryName])
    print("IDCG: ", IDCG)
    NDCG75 = DCG/IDCG
    return NDCG75

        
print(calculateNDCG75(database, 'name'))

def calculateAP(arr):
    totalSeen = 0
    totalRelevant = 0
    suum = 0
    
    for id in arr:
        totalSeen += 1
        if id == 1:
            totalRelevant += 1
            suum += totalRelevant/totalSeen
            
    return 2

arr = [1, 0, 1, 0, 0, 1, 0, 0, 1, 1]
arr2 = [0,1,1,1,0,1,0,0,0,1,1,0,0,0,0,0,0,1,0,1]
arr2 = [0,0,0,0]
print(calculateAP(arr2))


import matplotlib.pyplot as plt
   
year = [1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
unemployment_rate = [9.8, 12, 8, 7.2, 6.9, 7, 6.5, 6.2, 5.5, 6.3]
  
plt.plot(year, unemployment_rate)
plt.title('unemployment rate vs year')
plt.xlabel('year')
plt.ylabel('unemployment rate')
plt.show()