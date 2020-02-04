import sys

global N
global bk
global bkls
global solcnt
N = 8#the dimensions of the board
bk=0#statistic counts
bkls=[]
solcnt=1


#gets input from user
def inputuser():
    coldict={'A':7,'B':6,'C':5,'D':4,'E':3,'F':2,'G':1,'H':0}
    rowcol=input("Please enter in position of the first queen.")
    rowcol=rowcol.replace(" ","")#gets rid of spaces
    col=int(rowcol[0])-1
    row=rowcol[1]
    row=row.upper()
    row=coldict[row]
    output=[row,col]
    return output
    
#function used for debugging would print board for visualization to check if correct
#and to help visualizes the process
def printboard(board):
    for i in range(N):
        for j in range(N):
            print (board[i][j]," ", end= "")
        print("")
    print("")
#prints rows in desired format
def printrows(board):
    rowdict={7:'A',6:'B',5:'C',4:'D',3:'E',2:'F',1:'G',0:'H'}
    row=1;
    for i in range(N):
        for j in range(N):
            if board[j][i] == 1:
                print("Row ",row,": ",row,rowdict[j])
                row+=1
                break;

# Checks the diagonals if there are any other queens on that diagonals which are marked by the 1 so checks if there is a 1 on the upper diagonal
#and the lower diagonal but it only needs to check the left side  since it is assigning queens col by col left to right so nothing will be assigned on the right yet
#also checks if there are any queens on the same row marked by the 1
def checkconsit(board, row, col):
    board[row][col]=0
    #row check
    for i in range(col):
        if board[row][i] == 1:
            board[row][col]=1
            return False

    #up diagonal check
    for i,j in zip(range(row,-1,-1), range(col,-1,-1)):
        if board[i][j] == 1:
            board[row][col]=1
            return False

    #lower diagonal check
    for i,j in zip(range(row,N,1), range(col,-1,-1)):
        if board[i][j] == 1:
            board[row][col]=1
            return False

    board[row][col]=1
    return True

def backtrack(board, col):
    #checks if all queens are placed than solution is found and print it
    global N
    global bk
    global bkls
    global solcnt
    if col >= N:
        print("Solution ",solcnt)#print solution
        solcnt+=1
        #printboard(board)#print board
        printrows(board)
        bkls.append(bk)
        print("Number of backtracks for chronological backtracking: ",bk)#print back tracks
        bk=0
        return True


    for i in range(N):#loop through columns

        
            # Place this queen in board[i][col]
            board[i][col] = 1

            if checkconsit(board, i, col): 
                backtrack(board, col+1)#recursive call to check the next availaile squares
            
            board[i][col] = 0#does the backtrack
            bk+=1

    return False  #not valid for this iteration than return false


def main():#init board
    board = [ [0, 0, 0, 0,0,0,0,0],
            [0, 0, 0, 0,0,0,0,0],
            [0, 0, 0, 0,0,0,0,0],
            [0, 0, 0, 0,0,0,0,0],
            [0, 0, 0, 0,0,0,0,0],
            [0, 0, 0, 0,0,0,0,0],
            [0, 0, 0, 0,0,0,0,0],
            [0, 0, 0, 0,0,0,0,0],
            ]
    #gets user input
    vals=inputuser()
    board[vals[0]][vals[1]]=1
    if backtrack(board, 1) == True:
        print ("Solution does not exist")
        return False
    
    #Display tota stats
    #print(bkls)
    #print(bk)
    totalbk=sum(bkls)+bk
    print("Total number of backtracks:",totalbk)
    
    return True





main()

