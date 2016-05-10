# @author Joshua

import sys

#---------------------------------------Function Definitions------------------------------------------------

#Evaluation Function
def getEvaluationValue(boardState, boardValues, gamePlayer ):

    playerValue = 0
    enemyPlayerValue = 0

    gameEnemyPlayer = getEnemy(gamePlayer)
    for i in range(0,5):
        for j in range(0,5):
            if boardState[i][j] == gamePlayer:
                playerValue += int(boardValues[i][j])
            elif boardState[i][j] == gameEnemyPlayer:
                enemyPlayerValue += int(boardValues[i][j])

    return playerValue-enemyPlayerValue

#Checks whether the input position can be sneaked or not.
#Returns a boolean
def isSneakable(currentBoardState, player , iPosition , jPosition):

    if iPosition-1 >= 0 and str(currentBoardState[iPosition-1][jPosition]) == player:
        return False
    elif iPosition+1 <= 4 and str(currentBoardState[iPosition+1][jPosition]) == player:
        return False
    elif jPosition-1 >= 0 and str(currentBoardState[iPosition][jPosition-1]) == player:
        return False
    elif jPosition+1 <= 4 and str(currentBoardState[iPosition][jPosition+1]) == player:
        return False

    return True

#Return the enemy of the input player
def getEnemy (player):
    if player == 'X':
        return 'O'
    else:
        return 'X'

#Checks whether the position is occupied or not
def isOccupied(currentBoardState, iPosition, jPosition):
    if (currentBoardState[iPosition][jPosition] != '*'):
        return True
    else:
        return False

#Checks the outcome value on performing raid on the input position
def getRaidValue(currentBoardState, boardValues, player, iPosition, jPosition):
    raidValue = int(boardValues[iPosition][jPosition])
    enemyPlayer = getEnemy(player)

    if iPosition-1 >= 0 and currentBoardState[iPosition-1][jPosition] == enemyPlayer:
        raidValue += int(boardValues[iPosition-1][jPosition])

    if iPosition+1 <= 4 and currentBoardState[iPosition+1][jPosition] == enemyPlayer:
        raidValue += int(boardValues[iPosition+1][jPosition])

    if jPosition-1 >= 0 and currentBoardState[iPosition][jPosition-1] == enemyPlayer:
        raidValue += int(boardValues[iPosition][jPosition-1])

    if jPosition+1 <= 4 and currentBoardState[iPosition][jPosition+1] == enemyPlayer:
        raidValue += int(boardValues[iPosition][jPosition+1])

    return raidValue

#Performs raid and sneak operation on the given raid position
def performOperation(currentBoardState, gamePlayer, iRaidPosition, jRaidPosition, operation):
    if operation == 'raid':
        enemyPlayer = getEnemy(gamePlayer)
        currentBoardState[iRaidPosition][jRaidPosition] = gamePlayer

        if (iRaidPosition-1 >= 0 and currentBoardState[iRaidPosition-1][jRaidPosition] == enemyPlayer):
            currentBoardState[iRaidPosition-1][jRaidPosition] = gamePlayer

        if (jRaidPosition-1 >= 0 and currentBoardState[iRaidPosition][jRaidPosition-1] == enemyPlayer):
            currentBoardState[iRaidPosition][jRaidPosition-1] = gamePlayer

        if (jRaidPosition+1 <=4  and currentBoardState[iRaidPosition][jRaidPosition+1] == enemyPlayer):
            currentBoardState[iRaidPosition][jRaidPosition+1] = gamePlayer

        if (iRaidPosition+1 <= 4 and currentBoardState[iRaidPosition+1][jRaidPosition] == enemyPlayer):
            currentBoardState[iRaidPosition+1][jRaidPosition] = gamePlayer

    elif operation == 'sneak':
        currentBoardState[iRaidPosition][jRaidPosition] = gamePlayer

#Prints the log for minimax
#@param boardPosition:Alphanumeric position on the board ex.A1,B2
def printLog(boardPosition, depth, evaluationUtility, traverseLogFile, printFlag):

    if printFlag == True:
        if evaluationUtility == float('inf'):
            traverseLogFile.write(boardPosition+','+str(depth)+','+'Infinity')
        elif evaluationUtility == -float('inf'):
            traverseLogFile.write(boardPosition+','+str(depth)+','+'-Infinity')
        else:
            traverseLogFile.write(boardPosition+','+str(depth)+','+str(evaluationUtility))

        traverseLogFile.write('\n')

#Prints the log for alpha beta pruning
#@param boardPosition:Alphanumeric position on the board ex.A1,B2
def printABLog(boardPosition, depth, evaluationUtility, alpha, beta, traverseLogFile, printFlag):

    if printFlag == True:
        if evaluationUtility == float('inf'):
            evaluationUtility = 'Infinity'
        elif evaluationUtility == -float('inf'):
            evaluationUtility = '-Infinity'

        if alpha == float('inf'):
            alpha = 'Infinity'
        elif alpha == -float('inf'):
            alpha = '-Infinity'

        if beta ==  float('inf'):
            beta = 'Infinity'
        elif beta == -float('inf'):
            beta = '-Infinity'

        traverseLogFile.write(boardPosition+','+str(depth)+','+str(evaluationUtility)+','+str(alpha)+','+str(beta))

        traverseLogFile.write('\n')

#Returns the alphanumeric board position
def getBoardPosition(iPosition, jPosition):
    return str(chr(65+jPosition))+str(iPosition+1)

#Returns a boolean whether the board is full or not.
def isBoardFull (boardState):
    for i in range(0,5):
        for j in range(0,5):
            if not(isOccupied(boardState,i,j)):
                return False
    return True

#Gives the next move for the given player and algo
def getNextMove(boardState, boardValues, player, playerAlgo, cutoff, traverseLogFile):

    iNext = -1
    jNext = -1

    if playerAlgo == 1:
        trash,iNext,jNext = GBFS(boardState,boardValues,player)
    elif playerAlgo == 2:
        trash,iNext,jNext = MINIMAX(boardState,boardValues,player,player,cutoff,0,-99,-99,traverseLogFile,False)
    elif playerAlgo == 3:
        trash,iNext,jNext = ABPrune(boardState,boardValues,player,player,cutoff,0,-99,-99,-float('inf'),float('inf'),traverseLogFile,False)

    return iNext,jNext

#----------------------------------------Algorithms--------------------------------------------------------

#Algorithm for Greedy BFS algorithm
def GBFS(boardState, boardValues, gamePlayer):

    maxEvaluationValue = -float('inf')
    iNextPosition = -1
    jNextPosition = -1

    for i in range(0,5):
        for j in range(0,5):

            if (not(isOccupied(boardState,i,j))):
                newBoardState = [eachRow[:] for eachRow in boardState]

                if (isSneakable(boardState,gamePlayer,i,j)):
                    newBoardState[i][j] = gamePlayer
                else:
                    enemyPlayer = getEnemy(gamePlayer)
                    newBoardState[i][j] = gamePlayer

                    if (i-1 >= 0 and newBoardState[i-1][j] == enemyPlayer):
                        newBoardState[i-1][j] = gamePlayer

                    if (j-1 >= 0 and newBoardState[i][j-1] == enemyPlayer):
                        newBoardState[i][j-1] = gamePlayer

                    if (j+1 <=4  and newBoardState[i][j+1] == enemyPlayer):
                        newBoardState[i][j+1] = gamePlayer

                    if (i+1 <= 4 and newBoardState[i+1][j] == enemyPlayer):
                        newBoardState[i+1][j] = gamePlayer

                evaluationValue = getEvaluationValue(newBoardState,boardValues,gamePlayer)

                if evaluationValue > maxEvaluationValue:
                    maxEvaluationValue = evaluationValue
                    iNextPosition = i
                    jNextPosition = j

    return maxEvaluationValue,iNextPosition,jNextPosition

#Algorithm for Minimax
#Constant parameters :{boardValue, gamePlayer, cutoffDepth, traverseLogFile }
def MINIMAX(boardState, boardValues, gamePlayer, player, cutoffDepth, currentDepth, iSelfPosition, jSelfPosition, traverseLogFile,printFlag):

    evaluationUtility = -99
    iNextPosition = -1
    jNextPosition = -1

    #Base Condition
    if currentDepth == cutoffDepth or isBoardFull(boardState):
        evaluationUtility = getEvaluationValue(boardState,boardValues,gamePlayer)
        if currentDepth != 0:
            printLog(getBoardPosition(iSelfPosition,jSelfPosition),currentDepth,evaluationUtility,traverseLogFile,printFlag)
        else:
            printLog('root',currentDepth,evaluationUtility,traverseLogFile,printFlag)
        return evaluationUtility,iNextPosition,jNextPosition

    #Recursive Element
    if currentDepth%2 == 0:
        evaluationUtility = -float('inf')
    else:
        evaluationUtility = float('inf')

    if (currentDepth != 0):
        printLog(getBoardPosition(iSelfPosition,jSelfPosition),currentDepth,evaluationUtility,traverseLogFile,printFlag)
    else:
        printLog("root",currentDepth,evaluationUtility,traverseLogFile,printFlag)

    for i in range(0,5):
        for j in range(0,5):

            if (not(isOccupied(boardState,i,j))):
                #Initializing the new board state for next move
                newBoardState = [eachRow[:] for eachRow in boardState]
                if (isSneakable(boardState,player,i,j)):
                    newBoardState[i][j] = player
                else:
                    enemyPlayer = getEnemy(player)
                    newBoardState[i][j] = player

                    if (i-1 >= 0 and newBoardState[i-1][j] == enemyPlayer):
                        newBoardState[i-1][j] = player

                    if (j-1 >= 0 and newBoardState[i][j-1] == enemyPlayer):
                        newBoardState[i][j-1] = player

                    if (j+1 <=4  and newBoardState[i][j+1] == enemyPlayer):
                        newBoardState[i][j+1] = player

                    if (i+1 <= 4 and newBoardState[i+1][j] == enemyPlayer):
                        newBoardState[i+1][j] = player

                childUtility,trash1,trash2 = MINIMAX(newBoardState,boardValues,gamePlayer,getEnemy(player),cutoffDepth,currentDepth+1,i,j,traverseLogFile,printFlag)

                if currentDepth%2 == 0:
                    if (childUtility > evaluationUtility):
                        evaluationUtility = childUtility

                        if currentDepth == 0:
                            iNextPosition = i
                            jNextPosition = j
                else:
                    if (childUtility < evaluationUtility):
                        evaluationUtility = childUtility


                if currentDepth != 0:
                    printLog(getBoardPosition(iSelfPosition,jSelfPosition),currentDepth,evaluationUtility,traverseLogFile,printFlag)
                else:
                    printLog("root",currentDepth,evaluationUtility,traverseLogFile,printFlag)

    return evaluationUtility,iNextPosition,jNextPosition

#Algorithm for Alpha Beta Pruning
#Constant parameters :{boardValue, gamePlayer, cutoffDepth, traverseLogFile }
def ABPrune (boardState, boardValues, gamePlayer, player, cutoffDepth, currentDepth, iSelfPosition, jSelfPosition, alpha, beta, traverseLogFile,printFlag ):

    evaluationUtility = -99
    iNextPosition = -1
    jNextPosition = -1

    #Base Condition
    if currentDepth == cutoffDepth or isBoardFull(boardState):
        evaluationUtility = getEvaluationValue(boardState,boardValues,gamePlayer)

        if (currentDepth != 0):
            printABLog(getBoardPosition(iSelfPosition,jSelfPosition),currentDepth,evaluationUtility,alpha,beta,traverseLogFile,printFlag)
        else:
            printABLog('root',currentDepth,evaluationUtility,alpha,beta,traverseLogFile,printFlag)

        return evaluationUtility, iNextPosition, jNextPosition

    #Recursive Element
    if currentDepth%2 == 0:
        evaluationUtility = -float('inf')
    else:
        evaluationUtility = float('inf')

    if (currentDepth != 0):
        printABLog(getBoardPosition(iSelfPosition,jSelfPosition),currentDepth,evaluationUtility,alpha,beta,traverseLogFile,printFlag)
    else:
        printABLog('root',currentDepth,evaluationUtility,alpha,beta,traverseLogFile,printFlag)

    isBreak = False
    for i in range(0,5):
        if isBreak == True:
            break

        for j in range(0,5):

            if (not(isOccupied(boardState,i,j))):
                #Initializing the new board state for next move
                newBoardState = [eachRow[:] for eachRow in boardState]
                if (isSneakable(boardState,player,i,j)):
                    newBoardState[i][j] = player
                else:
                    enemyPlayer = getEnemy(player)
                    newBoardState[i][j] = player

                    if (i-1 >= 0 and newBoardState[i-1][j] == enemyPlayer):
                        newBoardState[i-1][j] = player

                    if (j-1 >= 0 and newBoardState[i][j-1] == enemyPlayer):
                        newBoardState[i][j-1] = player

                    if (j+1 <=4  and newBoardState[i][j+1] == enemyPlayer):
                        newBoardState[i][j+1] = player

                    if (i+1 <= 4 and newBoardState[i+1][j] == enemyPlayer):
                        newBoardState[i+1][j] = player

                childUtility,trash1,trash2 = ABPrune(newBoardState,boardValues,gamePlayer,getEnemy(player),cutoffDepth,currentDepth+1,i,j,alpha,beta,traverseLogFile,printFlag)

                if currentDepth%2 == 0:
                    if childUtility > evaluationUtility:
                        evaluationUtility = childUtility

                    if childUtility > alpha:

                        if currentDepth == 0:
                            iNextPosition = i
                            jNextPosition = j

                        if childUtility < beta:
                            alpha = childUtility
                        else:
                            isBreak = True
                            break
                else:
                    if childUtility < evaluationUtility:
                        evaluationUtility = childUtility

                    if childUtility < beta:

                        if childUtility > alpha:
                            beta = childUtility
                        else:
                            isBreak = True
                            break

                if currentDepth != 0:
                    printABLog(getBoardPosition(iSelfPosition,jSelfPosition),currentDepth,evaluationUtility,alpha,beta,traverseLogFile,printFlag)
                else:
                    printABLog('root',currentDepth,evaluationUtility,alpha,beta,traverseLogFile,printFlag)

    if isBreak == True:
        if currentDepth  != 0:
            printABLog(getBoardPosition(iSelfPosition,jSelfPosition),currentDepth,evaluationUtility,alpha,beta,traverseLogFile,printFlag)
        else:
            printABLog('root',currentDepth,evaluationUtility,alpha,beta,traverseLogFile,printFlag)


    return evaluationUtility,iNextPosition,jNextPosition

#----------------------------------------Input and Control--------------------------------------------------

#filename = sys.argv[-1]
filename = 'Sample inputs + outputs/1/input.txt'
countFile = open(filename)
decisionCount = 0
for line in countFile:
    decisionCount = decisionCount+1
countFile.close()

#1.Handling the Input

#Single move Games
if decisionCount == 13:
    #Initialisation of the variables
    gameTask = 0
    gamePlayer = 0
    gameEnemyPlayer = 0
    gameCutOff = 0

    boardValues = []
    boardState = []

    #Reading the input file
    inputFile = open(filename)

    #Reading the game task player and cutoff
    gameTask  = inputFile.readline().strip()
    gameTask = int(gameTask)
    gamePlayer = inputFile.readline().strip()
    gameCutOff = inputFile.readline().strip()
    gameCutOff = int(gameCutOff)
    gameEnemyPlayer = getEnemy(gamePlayer)

    #Reading the board grid values
    for i in range(0, 5):
        line = inputFile.readline()
        boardValues.append(line.split())

    #Reading the current board status
    for i in range(0, 5):
        l = list(inputFile.readline().strip())
        boardState.append(l)


    inputFile.close()

    #2.Control

    if gameTask == 1:
        #print 'Greedy Best First Search in execution...'

        nextStateFile = open('next_state.txt','w')

        result,iNext,jNext = GBFS(boardState,boardValues,gamePlayer)

        if iNext >= 0 and iNext <= 4 and jNext >= 0 and jNext <= 4:
            #print 'The position chosen is ',getBoardPosition(iNext,jNext),' with utility value of ',result,'.'
            if (isSneakable(boardState,gamePlayer,iNext,jNext)):
                performOperation(boardState, gamePlayer, iNext, jNext,'sneak')
            else:
                performOperation(boardState, gamePlayer, iNext, jNext,'raid')

        for i in range(0,5):
            nextStateFile.write(''.join(boardState[i]))
            nextStateFile.write('\n')

        nextStateFile.close()

        with open('next_state.txt', 'rb+') as finalStripFile:
            finalStripFile.seek(0,2)
            size=finalStripFile.tell()
            finalStripFile.truncate(size-1)
            finalStripFile.close()


    elif gameTask == 2:
        #print 'Minimax Search in execution...'

        traverseLogFile = open('traverse_log.txt','w')
        nextStateFile = open('next_state.txt','w')
        traverseLogFile.write("Node,Depth,Value\n")

        result,iNext,jNext = MINIMAX(boardState,boardValues,gamePlayer,gamePlayer,gameCutOff,0,-99,-99,traverseLogFile,True)

        if iNext >= 0 and iNext <= 4 and jNext >= 0 and jNext <= 4:
            #print 'The position chosen is ',getBoardPosition(iNext,jNext),' with utility value of ',result,'.'
            if (isSneakable(boardState,gamePlayer,iNext,jNext)):
                performOperation(boardState, gamePlayer, iNext, jNext,'sneak')
            else:
                performOperation(boardState, gamePlayer, iNext, jNext,'raid')

        for i in range(0,5):
            nextStateFile.write(''.join(boardState[i]))
            nextStateFile.write('\n')

        traverseLogFile.close()
        nextStateFile.close()

        with open('traverse_log.txt', 'rb+') as finalStripFile:
            finalStripFile.seek(0,2)
            size=finalStripFile.tell()
            finalStripFile.truncate(size-1)
            finalStripFile.close()

        with open('next_state.txt', 'rb+') as finalStripFile:
            finalStripFile.seek(0,2)
            size=finalStripFile.tell()
            finalStripFile.truncate(size-1)
            finalStripFile.close()

    elif gameTask == 3:
        #print 'Alpha-Beta Pruning Search in execution...'

        traverseLogFile = open('traverse_log.txt','w')
        nextStateFile = open('next_state.txt','w')
        traverseLogFile.write("Node,Depth,Value,Alpha,Beta\n")

        result,iNext,jNext = ABPrune(boardState,boardValues,gamePlayer,gamePlayer,gameCutOff,0,-99,-99,-float('inf'),float('inf'),traverseLogFile,True)

        if iNext >= 0 and iNext <= 4 and jNext >= 0 and jNext <= 4:
            #print 'The position chosen is ',getBoardPosition(iNext,jNext),' with utility value of ',result,'.'
            if (isSneakable(boardState,gamePlayer,iNext,jNext)):
                performOperation(boardState, gamePlayer, iNext, jNext,'sneak')
            else:
                performOperation(boardState, gamePlayer, iNext, jNext,'raid')

        for i in range(0,5):
            nextStateFile.write(''.join(boardState[i]))
            nextStateFile.write('\n')

        traverseLogFile.close()
        nextStateFile.close()

        with open('traverse_log.txt', 'rb+') as finalStripFile:
            finalStripFile.seek(0,2)
            size=finalStripFile.tell()
            finalStripFile.truncate(size-1)
            finalStripFile.close()

        with open('next_state.txt', 'rb+') as finalStripFile:
            finalStripFile.seek(0,2)
            size=finalStripFile.tell()
            finalStripFile.truncate(size-1)
            finalStripFile.close()

else:

    #1. Input

    #Initialisation of the variables
    gameTask = 0
    player1 = 0
    player2 = 0
    player1Algo = 0
    player2Algo = 0
    player1Cutoff = 0
    player2Cutoff = 0

    boardValues = []
    boardState = []

    #Reading the input file
    inputFile = open(filename)

    gameTask = inputFile.readline().strip()
    gameTask = int(gameTask)

    player1 = inputFile.readline().strip()
    player1Algo = inputFile.readline().strip()
    player1Algo = int(player1Algo)
    player1Cutoff = inputFile.readline().strip()
    player1Cutoff = int(player1Cutoff)

    player2 = inputFile.readline().strip()
    player2Algo = inputFile.readline().strip()
    player2Algo = int(player2Algo)
    player2Cutoff = inputFile.readline().strip()
    player2Cutoff = int(player2Cutoff)

    #Reading the board grid values
    for i in range(0, 5):
        line = inputFile.readline()
        boardValues.append(line.split())

    #Reading the current board status
    for i in range(0, 5):
        l = list(inputFile.readline().strip())
        boardState.append(l)

    inputFile.close()


    #2.Control

    traverseLogFile = open('traverse_log.txt','w')

    traceStateFile = open('trace_state.txt','w')
    traceStateFile.close()
    traceStateFile = open('trace_state.txt','a')
    player1Move = True

    while (not(isBoardFull(boardState))):
        if (player1Move == True):
            iNext,jNext = getNextMove(boardState,boardValues,player1,player1Algo,player1Cutoff,traverseLogFile)

            if iNext >= 0 and iNext <= 4 and jNext >= 0 and jNext <= 4:
                if (isSneakable(boardState,player1,iNext,jNext)):
                    performOperation(boardState, player1, iNext, jNext,'sneak')
                else:
                    performOperation(boardState, player1, iNext, jNext,'raid')

            player1Move = False

        else:
            iNext,jNext = getNextMove(boardState,boardValues,player2,player2Algo,player2Cutoff,traverseLogFile)

            if iNext >= 0 and iNext <= 4 and jNext >= 0 and jNext <= 4:
                if (isSneakable(boardState,player2,iNext,jNext)):
                    performOperation(boardState, player2, iNext, jNext,'sneak')
                else:
                    performOperation(boardState, player2, iNext, jNext,'raid')

            player1Move = True

        for i in range(0,5):
            traceStateFile.write(''.join(boardState[i]))
            traceStateFile.write('\n')


    traceStateFile.close()
    traverseLogFile.close()

    with open('trace_state.txt', 'rb+') as finalStripFile:
        finalStripFile.seek(0,2)
        size=finalStripFile.tell()
        finalStripFile.truncate(size-1)
        finalStripFile.close()

