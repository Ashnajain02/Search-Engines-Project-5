Ashna Jain
Project 5 - Evaluation 

Breakdown - If it is not blatantly obvious (to a human who is not you), please indicate where in your source code the evaluation happens, including where the per-query scores and overall average scoring are handled.
Description - Provide a description of system, design tradeoffs, etc., that you made.
Libraries - List the software libraries you used, and for what purpose. Implementation must be your own work. If you are thinking of using any other libraries for this assignment, please send us an email to check first. Most people will not use any third party libraries.
Dependencies - Provide instructions for downloading dependencies of the code – where do we find that third-party library that you got permission to use? Not expecting anything here but just in case.
Building - Provide instructions for building the code if it is anything other than compiling the .java or .py or whatever files as described in the autograder instructions above.

Breakdown:
    -Everything in eval.py 
Description:
    -To start off I created 3 main data structures. I first parsed through the qrels file and created a rankedDatabase and qrelsFiles dictionaries. 
    For the rankedDatabase, each key was a queryName and the value for each queryName was an array where each element was a size 2 array: [docID, relevanceNum]. I stored the relevanceNum so that I could later sort by this value.
    For the qrelsFiles, each key was also a queryName and the value for each queryname was another dictionary with keys a docIDs and values as the relevance of the specific docuement. 
    
    rankedDatabase = {
        "301" = [[fileA, 0], [fileB, 0], [fileE, 1]],
        "302"= [[fileD, 1], [fileA, 0], [fileF, 1], [fileC, 1]]
    }
    qrelsFiles = {
        "301" = {
            fileA = 0
            fileB = 0
            fileE = 1
        }, 
        "302" = {
            fileD = 1
            fileA = 0
            fileF = 1
            fileC = 1
        }
    }
    I then parsed through the .trecrun file and created a database and trecrunFiles dictionary.
    The keys are queryNames, if the docID is in the qrelsFiles database, then we append a size 2 array to database: [docID, relevance of doc based off of qrelsFiles]
    otherwise, we add [docID, 0]. If its not in qrels then it is not relevant. 
    For trecrunFiles, the values for each key is another dictionary with key as docID and value as an array [rank, score].

    database = {
        "301" = [[fileC, 1], [fileB, 0], [fileE, 1]],
        "302"= [[fileZ, 0], [fileY, 0]]
    }
    trecrunFiles = {
        "301" = {
            fileA = [rank, score]
            fileK = [rank, score]
            fileF = [rank, score]
        }
    }
     
    For the rest of my design, I have functions that calculate the different score. 
    The function use various aspecsts of my 4 dictionaries that I set up in the beginning.

Libraries/Dependencies:
    -import math
    =python 3

Building/Running:
    -After directing to the appropiate folder, just run the file, and the appropiate file (.eval) should be outputted
