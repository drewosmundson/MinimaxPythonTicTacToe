import random 

def checkWin(board):
    for i in range(1, 3):  # 1 is computer and 2 is human
        for j in range(3):
            if board[j][0] == board[j][1] == board[j][2] == i:  #checks all rows and columns for a 1 or 2 win
                return True, i
            if board[0][j] == board[1][j] == board[2][j] == i:
                return True, i
        if board[0][0] == board[1][1] == board[2][2] == i:   #checks both diagonals for a 1 or 2 win
            return True, i
        if board[0][2] == board[1][1] == board[2][0] == i:
            return True, i
    return False, 0

def checkTie(board):
    for i in range(3):  #check if board is full
        for j in range(3):
            if board[i][j] == 0:
                return False
    return True

def checkFirstMove(board):
    for i in range(3):  #check if board is all 0
        for j in range(3):
            if board[i][j] != 0:
                return False
    return True

def miniMax(board, depth, isMaxing, alpha, beta):
    #https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
    # check if someone has already won
    won, player = checkWin(board)
    if won:
        if player == 1:  # if computer wins
            return [-1, -1], 1
        else:            # if human wins
            return [-1, -1], -1
    # check if tie (no spaces left and no winner)
    if checkTie(board):
        return [-1, -1], 0

    if isMaxing:
        # computer is trying to maximize score
        bestScore = -float("inf")   # start at lowest possible value
        bestMove = [-1, -1]
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:   # check each possible move
                    board[i][j] = 1    # computer plays here
                    _, score = miniMax(board, depth + 1, False, alpha, beta)  # simulate human move
                    board[i][j] = 0    # undo move (backtrack)
                    if score > bestScore:   # keep move if it’s the best so far
                        bestScore = score
                        bestMove = [i, j]
                    alpha = max(alpha, bestScore)   # update alpha (best guaranteed score for maximizer)
                    if beta <= alpha:  # pruning condition no need to check further
                        break
        return bestMove, bestScore
    else:
        # human is trying to minimize computer's score
        bestScore = float("inf")   # start at highest possible value
        bestMove = [-1, -1]
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0: # check each possible move
                    board[i][j] = 2  # human plays here
                    _, score = miniMax(board, depth + 1, True, alpha, beta)  # simulate computer move
                    board[i][j] = 0    # backtrack
                    if score < bestScore:   # keep move if it’s the best
                        bestScore = score
                        bestMove = [i, j]
                    beta = min(beta, bestScore)   # update beta best guaranteed score for minimizer
                    if beta <= alpha:  # pruning condition: no need to check further
                        break
        return bestMove, bestScore


def convertCoordinateToLocation(coordinate):
    for i in range(3):
        for j in range(3):
            if (coordinate == [i,j]):
                return i*3+j+1             #returns 1 - 9 for location related to board


def getNextMoveRandom(board):
    empty = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                empty.append((i*3)+j+1)
    randLocation = random.choice(empty) #get random empty space
    return randLocation  #this is what we 1will send to the robot for its arm to move to


def getNextMove(board):
    if (checkWin(board)[0] or checkTie(board)):
        return 0 #send message to baxter to stop it does not matter who wins baxter just needs to stop
    if(checkFirstMove(board)):
        return 5 # always plays the middle square if baxter has the first move. my algorithm gets stuck in a loop of comparison if all 0 and returns none
    score = 0
    next_move = miniMax(board, score, True) #returns best move for current board
    location = convertCoordinateToLocation(next_move[0]) #converts coordinate to location
    if location == None:            #edge case in case no best location is found such as if a board looks like 000020000
        location = getNextMoveRandom(board)
    return location #send message to baxter to move to location


def testing():
    inputString = input("Enter a board in 9 digit format 000000000. upperleft of board is first digit. 1 is computer 2 is player piece ")
    while len(inputString) != 9:
        inputString = input("Invalid enter 9 digits ") #make sure is valid move
    tempBoard = []
    board = []
    for i in range(9):
        tempBoard.append(int(inputString[i]))
        if (i % 3 == 2):
            board.append(tempBoard)
            tempBoard = []
    next_move = getNextMove(board)
    print(next_move)
    return next_move
testing()
