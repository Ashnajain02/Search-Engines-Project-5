#Ashna Jain
#Project 5: Evaluation 

import math
import sys
import matplotlib.pyplot as plt

database = dict()
rankedDatabase = dict()
trecrunFiles = dict()
qrelsFiles = dict()

if __name__ == '__main__':
    # Read arguments from command line, or use sane defaults for IDE.
    argv_len = len(sys.argv)
    runFile = sys.argv[1] if argv_len >= 2 else 'bm25.trecrun'
    qrelsFile = sys.argv[2] if argv_len >= 3 else 'qrels'
    outputFile = sys.argv[3] if argv_len >= 4 else 'bm25.eval'

    with open(qrelsFile, "r") as file:
        count = 0
        for line in file:
            line = line.split()
            queryName = line[0]
            skip = line[1]
            docID = line[2]
            relevanceNum = int(line[3])
            
            if rankedDatabase.get(queryName) == None: 
                rankedDatabase[queryName] = []
            
            rankedDatabase[queryName] += [[docID, relevanceNum]]

            if qrelsFiles.get(queryName) == None: 
                qrelsFiles[queryName] = dict()
            
            qrelsFiles[queryName][docID] = relevanceNum
    #print(qrelsFiles["697"], '\n')
    with open(runFile, "r") as file:
        count = 0
        for line in file:
            line = line.split()
            queryName = line[0]
            skip = line[1]
            docID = line[2]
            rank  = int(line[3])
            score = line[4]
            text = line[5:]

            if queryName not in database:
                database[queryName] = []

            if docID in qrelsFiles[queryName]:
                database[queryName] += [[docID, qrelsFiles[queryName][docID]]]
            else:
                database[queryName] += [[docID, 0]]


            if queryName not in trecrunFiles:
                trecrunFiles[queryName] = dict()
            
            trecrunFiles[queryName][docID] = [rank, score]        
    #print(trecrunFiles["697"], '\n')
        
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
            if count == 75: 
                break
        return total
            
    def calculateNDCG75(queryName):
        DCG = calculateDCG(database[queryName])
        rankedDatabase[queryName].sort(key=lambda x: x[1], reverse=True)
        IDCG = calculateDCG(rankedDatabase[queryName][:75])
        NDCG75 = DCG/IDCG
        return NDCG75

    def calculateRR(queryName):
        for id in trecrunFiles[queryName]:
            if id in qrelsFiles[queryName] and qrelsFiles[queryName][id] > 0:
                rank = trecrunFiles[queryName][id][0]
                return 1/rank
        return 0.0000
        
    def calculateP(queryName, count):
        precision = 0
        c = 1
        for id in trecrunFiles[queryName]:
            if id in qrelsFiles[queryName] and qrelsFiles[queryName][id] > 0:
                precision += 1
            if c == count:
                break
            c += 1
        return precision

    def calculateTotalRelevant(queryName):
        total = 0
        for id in qrelsFiles[queryName]:
            if qrelsFiles[queryName][id] > 0:
                total += 1
        return total

    def calculateR(queryName, count):
        total = calculateTotalRelevant(queryName)
        rel = calculateP(queryName, count)
        return rel/total

    def calculateF1(queryName, count):
        P = calculateP(queryName, count)/count
        R = calculateR(queryName, count)
        if (R+P) == 0:
            return 0.0000 
        return (2*R*P) / (R+P)

    def calculateAP(queryName):
        totalSeen = 0
        totalRelevant = 0
        totaltotal = 0
        suum = 0
        for id in qrelsFiles[queryName]:
            if qrelsFiles[queryName][id] > 0:
                totaltotal += 1
        for id in trecrunFiles[queryName]:
            totalSeen += 1
            if id in qrelsFiles[queryName] and qrelsFiles[queryName][id] > 0:
                totalRelevant += 1
                suum += totalRelevant/totalSeen
        if totaltotal == 0:
            return 0.0000
        return suum/totaltotal

    with open(outputFile, 'w') as file:
        numQueries = len(trecrunFiles.keys())
        sumNDCG = 0
        sumRR = 0
        sumP = 0
        sumR = 0
        sumF1 = 0
        sumAP = 0
        for queryName in trecrunFiles.keys():
            sumNDCG += calculateNDCG75(queryName)
            sumRR += calculateRR(queryName)
            sumP += calculateP(queryName,15)/15
            sumR += calculateR(queryName,20)
            sumF1 += calculateF1(queryName,25)
            sumAP += calculateAP(queryName)

            file.write("NDCG@75" + '                    ' + queryName + '  ' + str(calculateNDCG75(queryName)) + '\n')
            file.write("RR" + '                         ' + queryName + '  ' +str(calculateRR(queryName)) + '\n')
            file.write("P@15" + '                       ' + queryName + '  ' + str(calculateP(queryName,15)/15)+ '\n')
            file.write("R@20" + '                       ' + queryName + '  ' + str(calculateR(queryName,20))+ '\n')
            file.write("F1@25" + '                      ' + queryName + '  ' + str(calculateF1(queryName,25))+ '\n')
            file.write("AP" + '                         ' + queryName + '  ' + str(calculateAP(queryName))+ '\n')
            #print(calculateAP(queryName))
        
        file.write("NDCG@75" + '                    ' + 'all' + '  ' + str(sumNDCG/numQueries) + '\n')
        file.write("MRR" + '                        ' + 'all' + '  ' +str(sumRR/numQueries) + '\n')
        file.write("P@15" + '                       ' + 'all' + '  ' + str(sumP/numQueries)+ '\n')
        file.write("R@20" + '                       ' + 'all' + '  ' + str(sumR/numQueries)+ '\n')
        file.write("F1@25" + '                      ' + 'all' + '  ' + str(sumF1/numQueries)+ '\n')
        file.write("MAP" + '                        ' + 'all' + '  ' + str(sumAP/numQueries)+ '\n')
        #print("MAP", sumAP/numQueries)
    print("done.")

    # queryName = '660'
    # recall = []
    # precision = []
    # count = 1
    # for id in trecrunFiles[queryName]:
    #     recall += [calculateR(queryName, count)]
    #     precision += [calculateP(queryName, count)]
    #     count += 1
    
    # plt.plot(recall, precision)
    # plt.title('recall vs precision')
    # plt.xlabel('recall')
    # plt.ylabel('precision')
    # plt.savefig('graph.png')
    # plt.show()