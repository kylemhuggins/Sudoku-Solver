
# coding: utf-8

# In[299]:

import numpy as np


# In[300]:

# later, I will figure out how to import raw data; for now, start with an easy puzzle
puzzle = np.array([[1,0,3,0,0,8,0,0,9],
                   [0,0,0,1,0,4,8,5,0],
                   [5,0,0,0,7,0,2,0,6],
                   [0,0,5,0,3,1,0,9,0],
                   [0,8,4,0,0,0,1,0,5],
                   [3,0,0,0,5,0,6,8,0],
                   [0,0,1,0,0,5,0,7,4],
                   [4,0,7,0,0,3,0,6,0],
                   [0,0,6,0,4,7,0,0,1]])

originalPuzzle = np.array([[1,0,3,0,0,8,0,0,9],
                           [0,0,0,1,0,4,8,5,0],
                           [5,0,0,0,7,0,2,0,6],
                           [0,0,5,0,3,1,0,9,0],
                           [0,8,4,0,0,0,1,0,5],
                           [3,0,0,0,5,0,6,8,0],
                           [0,0,1,0,0,5,0,7,4],
                           [4,0,7,0,0,3,0,6,0],
                           [0,0,6,0,4,7,0,0,1]])


# In[301]:

# dictionary of lists of lists -- 1st set of lists is segments, second is x,y coordinates

segmentParameters = {1:[[0, 1, 2], [0, 1, 2]], 2:[[0, 1, 2], [3, 4, 5]], 3:[[0, 1, 2], [6, 7, 8]], 4:[[3, 4, 5], [0, 1, 2]], 5:[[3, 4, 5], [3, 4, 5]], 6:[[3, 4, 5], [6, 7, 8]], 7: [[6, 7, 8], [0, 1, 2]], 8:[[6, 7, 8], [3, 4, 5]], 9:[[6, 7, 8], [6, 7, 8]]}


# In[302]:

def checkByIndividualCell():

    # the master for loop executes on a single cell of the 81 possible cells in the puzzle
    # valueAtHand, X, and Y are determined by the master for loop
    
    changeCounter = 0
    cellsChanged = []

    for x in range(9):
        for y in range(9):
            
            valueAtHand = puzzle[x,y]
            
            # if the value we're checking isn't 0, then we don't need to check it
            
            if valueAtHand == 0:
                        
                possibilities = [1,2,3,4,5,6,7,8,9]

                valueIndexX = x
                valueIndexY = y

                # valueIndexS is determined by the for loop, referencing segmentParameters

                for key, value in segmentParameters.items():
                    if valueIndexX in value[0]:
                        if valueIndexY in value[1]:
                            valueIndexS = key

                holder = segmentParameters[valueIndexS]
                rangeSX = holder[0]
                rangeSY = holder[1]

                # we will check all other values in the row

                for i in range(9):
                    if i == valueIndexY:
                        pass
                    else:
                        if puzzle[valueIndexX,i] in possibilities:
                            possibilities.remove(puzzle[valueIndexX,i])

                # we will check all other values in the column

                for i in range(9):
                    if i == valueIndexX:
                        pass
                    else:
                        if puzzle[i,valueIndexY] in possibilities:
                            possibilities.remove(puzzle[i,valueIndexY])

                # we will check all other values in the segment

                for i in rangeSX:
                    for j in rangeSY:
                        if i == valueIndexX and j == valueIndexY:
                            pass
                        else:
                            if puzzle[i,j] in possibilities:
                                possibilities.remove(puzzle[i,j])

                if len(possibilities) == 1:
                    puzzle[valueIndexX, valueIndexY] = possibilities[0]
                    changeCounter += 1
                    newHolder = [valueIndexX,valueIndexY]
                    cellsChanged.append(newHolder)
    
    return changeCounter, cellsChanged


# In[303]:

# this feeds into the verifyPurity function

def countCheck(listToCheck):
    
    # the list to check should have len 9
    # if list is cleared as ok, return true (masterCheck = 0 still)
    # if list is NOT cleared as ok, return false and list of numbers for which there are errors
    
    masterCheck = 0
    errorList = []
    
    for i in range(9):
        check = listToCheck.count(i+1)
        if check > 1:
            masterCheck += 1
            errorDigit = i + 1
            errorList.append(errorDigit)
    
    if masterCheck == 0:
        return True, []
    else:
        return False, errorList
            


# In[304]:

# function should ensure no duplicate values (other than 0) in a row, column, or segment

def verifyPurity():
    
    masterCheckPurity = 0
    purityCheck = []
    
    # first verify rows
    
    for i in range(9):
        test = list(puzzle[i, 0:])
        myBolean, myErrorList = countCheck(test)
        if myBolean == True:
            pass
        else:
            masterCheckPurity += 1
            purityCheck.append(myErrorList)
    
    # then verify columns
    
    for i in range(9):
        test = list(puzzle[0:, i])
        myBolean, myErrorList = countCheck(test)
        if myBolean == True:
            pass
        else:
            masterCheckPurity += 1
            purityCheck.append(myErrorList)
    
    # then verify segments
    
    for i in range(9):
        test = []
        segmentID = i + 1
        mySegment = segmentParameters[segmentID]
        testRangeX = mySegment[0]
        testRangeY = mySegment[1]
        
        for j in testRangeX:
            for k in testRangeY:
                test.append(puzzle[j,k])      
        
        myBolean, myErrorList = countCheck(test)
        if myBolean == True:
            pass
        else:
            masterCheckPurity += 1
            purityCheck.append(myErrorList)

    if masterCheckPurity == 0:
        return True, []
    else:
        return False, masterCheckPurity


# In[305]:

# this checks to see if the puzzle is solved yet

def completenessCheck():
    
    masterCompletenessCheck = 0
    
    for i in range(9):
        test = list(puzzle[i, 0:])
        numberLeftInList = test.count(0)
        masterCompletenessCheck += numberLeftInList
    
    if masterCompletenessCheck == 0:
        return True, 0
    else:
        return False, masterCompletenessCheck


# In[306]:

def iteration():
    numberChanged, changedIndices = checkByIndividualCell()
    isPure, impureList = verifyPurity()
    isComplete, leftToComplete = completenessCheck()
    
    print("Number of cells changed are: " + str(numberChanged))
    print("Indices of changed cells are " + str(changedIndices))
    print("Is the puzzle pure still? -- " + str(isPure))
    print("The impure cells are: " + str(impureList))
    print("Is the puzzle complete? -- " + str(isComplete))
    print("Number of cells left to complete are: " + str(leftToComplete))


# In[307]:

iteration()


# In[308]:

iteration()


# In[309]:

iteration()


# In[310]:

iteration()


# In[311]:

iteration()


# In[312]:

iteration()


# In[313]:

puzzle 


# In[314]:

originalPuzzle


# In[ ]:



