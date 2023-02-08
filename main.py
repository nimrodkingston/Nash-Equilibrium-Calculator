#Matrix A represents the payoff values for player 1
#Matrix B represents the payoff values for player 2
import numpy as np

def powerSet(size): # This function finds the power set of the numbers 0,1,2,3...,size
    tempSets = [] 
    sets = [] 
    subSet = [] # This is a placeholder for a subset

    for i in range(0,size): 
        subSet.append([i]) # This adds each item as a list to the subset
    tempSets.append(subSet) # This adds the subset to the solutions found so far

    for subSize in range(2,size + 1): # This iterates through all of the sizes of subset possible
        previousSet = tempSets[-1] # This holds all of the subsets from the previous subset size
        newSet = [] # This holds the all subsets of a given size
  
        for subSet in previousSet: 
            for j in range(subSet[-1] + 1, size): # This iterates through all of the indexes which are larger than the subset being checked
                newSet.append(subSet + [j]) # This adds the element to the subset
        tempSets.append(newSet) # This adds the new set of subsets to the list

    for subSize in tempSets: # This iterates through all of the sets in the tempset
        for subSet in subSize: # This iterates through all of the subsets within each size of subset
            sets.append(subSet) # This adds the completed subset to the final set
    return(sets) # The final set is returned

def LES(eq1,eq2): # (Linear Equation Simplifier) This takes two linear equations represented by two lists and simplifies the resulting equation
    newEq = [] 
    for i in range(0,len(eq1)): # This iterates through all of the items in equation 1 (it is assumed that both equations have the same variables, if not a coefficent of 0 is used)
        newEq.append(eq1[i] - eq2[i]) 
    return(newEq) # This returns the simplified equation

def convertSupport(support,length): # This turns a support into a simple vector with 1 or 0 
    vector = [] 

    for i in range(0,length): # This adds 0 to match the height/width of the matrix 
        vector.append(0) 

    for i in support: 
        vector[i] = 1 
    return(vector) # The final vector is returned

def matrixToVector(A): # This takes a 1XN matrix produced by numpy and turns it into a vector
    for i in range(0,len(A)):
        A[i] = A[i][0]
    return(A)

def vectorToMatrix(A): # This takes a simple list which represents a vector and turns it into a matrix which numpy can use for matrix multiplications
    for i in range(0,len(A)):
        A[i] = [A[i]]
    return(A)

def maximalityCheck(supportBinary,payoff): # This function takes the payoff function and the support being used and checks to see if the output is maximal
    maximum = round(max(payoff),14)  #This finds the largest value within the whole payoff matrix
  
    for i in range(0,len(supportBinary)):
        if supportBinary[i] == 1 and round(payoff[i],14) != maximum: # This checks if the support has been seleceted and that the value at this point is maximal
            return(False) # This returns false as the matrix is not maximal
    return(True) # This returns true as the payoff is maximal for the given support

def printMatrix(matrixA,matrixB,rows,columns):  # This outputs the inputted matrix to the user
    print("________________________________\n")
    print("Here is the matrix to be worked on: ")

    for m in range(0,rows):
        row = ""
        divider = ""

        for n in range(0,columns):
            row += "|" + str(matrixA[m][n]) + ", " + str(matrixB[m][n]) # All of the components of the print are added to a single string
        row += "|"
        print(row)

def textParser(): # This reads though a text file and reads the text into 2 matrices which the program can use
    fileName = input("Enter the name of the text file to be used with the extension .txt: ")
    try:
        file = open(fileName,"r")

    except:
        print("The filename given could not be found in the local folder")
        return(None)

    data = file.readlines()
    file.close()
    newData = []
    matrixA = []
    matrixB = []
    for line in data:
        number = ""
        for char in line:
            if char != "\n":
                number += char
            else:
                break
        newData.append(number)
    try: 
        rows = int(newData[0])
        columns = int(newData[1])

        counter = 2
        for m in range(0,rows):
            rowA = []
            rowB = []
            for n in range(0,columns):
                newCell = list(map(float, newData[counter].split(",")))
                rowA.append(newCell[0])
                rowB.append(newCell[1])
                counter += 1
            matrixA.append(rowA)
            matrixB.append(rowB)
    except:
        print("The data in the textfile is not of the correct format")
        return(None)
    return([matrixA,matrixB])


def matrixInput(rows,columns):
    matrixA = []
    matrixB = []
    print("\nAll cells must be entered in the form a,b where a is the payoff for player 1 and b is the payoff for player 2\n")
    #This is the code which generates the matrices for both the row and the column player
    for m in range(0,rows):
        rowA = []
        rowB = []
        for n in range(0,columns):
            errorFlag = True
            while errorFlag == True:
                inputCell = input("Enter the values for cell " + str(m + 1) + "," + str(n + 1) + ": ")
                try:
                    newCell = list(map(float, inputCell.split(",")))
                except:
                    print("The entered cell contains a non allowed character")
                if len(newCell) == 2:
                    rowA.append(newCell[0])
                    rowB.append(newCell[1])
                    errorFlag = False
                else:
                    print("The entered cell is not in the correct format, try again")
                
                    

        matrixA.append(rowA)
        matrixB.append(rowB)

    return([matrixA,matrixB])
# As a pure strategy is simply a special case of a mixed strategy, I ony have to write code to solve a mixed strategy 

def printEquation(variable,equation,output,singleSupport):
    outputString = ""

    if singleSupport:
        for i in range(0,len(equation)):
            print(variable + str(i + 1) + " = " + str(equation[i]))
    else:
        for i in range(0,len(equation)):
            if equation[i] >= 0 and i != 0:
                outputString += "+ "
            outputString += str(equation[i]) + "*" + variable + str(i + 1) + " "

        outputString += "= " + str(output)
        print(outputString)

def systemGenerator(payoff,supportBinary,altSupportBinary,variable): # This creates the system of equations to be solved
 
    equationInput = []
    equationOutput = []
    redundancyFlag = False
    equationInput.append([1.0]*len(payoff[0]))
    equationOutput.append([1])
    newSupportBinary = altSupportBinary

    for i in range(0,len(payoff)): # This block pairs equations within the payoff with each other 
        if altSupportBinary[i] == 1:
            for j in range(i + 1,len(altSupportBinary)):
                if altSupportBinary[j] == 1:
                    equationLine = LES(payoff[i],payoff[j])

                    if equationLine != [0]*len(equationLine): # This checks whether the equations are the same
                        equationInput.append(equationLine) # This adds the simplifed equations to the final system of equations
                        equationOutput.append([0])
                        break
                    else:
                        redundancyFlag = True # This states that two redundant equations have been found
    
    for i in range(0,len(supportBinary)): # This block adds the additional "X = 0" variable if there is a difference in dimensions
        if len(equationInput[0]) != len(equationInput) and supportBinary[i] == 0:
            equationLine = [0] * len(equationInput[0])
            equationLine[i] = 1
            equationInput.append(equationLine)
            equationOutput.append([0])

        if len(equationInput[0])==len(equationInput):
            break

   
    for i in range(0,len(equationInput)): # Ordering of prints needs to be changed at some point
        printEquation(variable,equationInput[i],equationOutput[i][0],False)

    if len(equationInput[0]) != len(equationInput):
        if redundancyFlag ==True:
            print("There is not enough unique information in this system")
        return(None)

    return([equationInput,equationOutput])

def solutionCalculator(support,supportBinary,altSupportBinary,A,variable):

    if len(support) == 1:
        printEquation(variable,supportBinary,0,True)
       
        ans = np.array(vectorToMatrix(supportBinary)) # This part is because values are passed by reference in python
        matrixToVector(supportBinary)
        return(ans)

    payoff = []
    
    for i in range(0,len(A)): # This multiplies the payoff with the strategy to get a linear equation
        newEq = [] 
        for j in range(0,len(A[0])): 
            newEq.append(A[i][j]*supportBinary[j]) 
            
        payoff.append(newEq)
        
    data = systemGenerator(payoff,supportBinary,altSupportBinary,variable)
    
    if data == None:
        print("The System from these supports is over/underconstrained")
        return(None)

    equationInput = data[0]
    equationOutput = data[1]

    if np.linalg.det(equationInput) == 0:
        print("A valid strategy could not be found")
        return(None)

    solutions = np.linalg.solve(np.array(equationInput),np.array(equationOutput))

    for element in solutions:
        if element < 0:
            print("Negative probability found")
            return(None)
    
    return(solutions)   

def nashEquilibriumCalculator(A,B,rows,columns,):
    supportA = powerSet(columns) # This is all of the possible supports which player 1 can have
    supportB = powerSet(rows) # This is all of the possible supports player 2 can have 
    supports = [] # This holds the supports which are currently being used

    for i in supportA: # This finds every possible combination of player 1's actions and player 2's actions
        for j in supportB:
            supports.append([i, j])

    for pair in supports: # This works out which actions are being considered and which ones aren't by each user
        if (len(pair[0]) == 1 and len(pair[1]) == 1) or (len(pair[0]) != 1 and len(pair[1]) != 1): # This checks whether both the supports are 1 or neither are 1 - can be replaced with an XOR at some point
            supportBinary1 = convertSupport(pair[0], columns) # Each element is a 1 or a 0 and this represents whether a variable is being taken into account or not
            supportBinary2 = convertSupport(pair[1],rows)

            print("\nSupports " + str(pair[0]) + " and " + str(pair[1]) + " are being checked" ) # Replace indexes with the item values
            print("Here is the system of equations to solve")
            print("column player's system: ")
            solution1 = solutionCalculator(pair[0],supportBinary1,supportBinary2,A,"Y") # This holds the solutions to the variables y1,y2... and is represented as a list of floats
            
            if solution1 is None: # If solutions are found to be a None value, an equilibrium couldn't be found
                print("An equilibrium could not be found with these supports")
                continue

            print("row player's system: ")
            solution1 = matrixToVector(solution1.tolist())
            solution2 = solutionCalculator(pair[1],supportBinary2,supportBinary1,np.transpose(B).tolist(),"X") # This holds the solutions to the variables x1,x2... and is represented as a list of floats
            
            if solution2 is None: #If solutions are found to be a None value, an equilibrium couldn't be found
                print("An equilibrium could not be found with these supports")
                continue

            solution2 = matrixToVector(solution2.tolist())
            payoff1 = np.matmul(A,solution1) # These represent the actual payoff values which will be gotten from the game
            payoff2 = np.matmul(np.transpose(B),solution2)
            outputStringY = ""
            outputStringX = ""

            for i in range(0,len(solution1)): # This outputs the systyem of equations for both players to the user
                    outputStringY += "y" + str(i + 1) + " = " + str(round(solution1[i], 3)) + " "
            for i in range(0,len(solution2)):
                    outputStringX += "x" + str(i + 1) + " = " + str(round(solution2[i], 3)) + " "

            print("column player's strategy profile: ")
            print(outputStringY)
            print("row player's strategy profile: ")
            print(outputStringX)

            if maximalityCheck(supportBinary2, payoff1) and maximalityCheck(supportBinary1,payoff2): # This checks whether the given strategy is truly maximal across all 
                print("An equilibrium has been found with this distribution!")
                   
                if len(pair[0]) == 1 and len(pair[1]) == 1: # This checks whether both supports are of size 1
                    print("This is also a pure nash equilibrium")
                
            else:
                print("This strategy is valid but is non maximal")
                print("An equilibrium could not be found with these supports")

def approximateCalculator(A,B,rows,columns,choice): # This calculates the approximate equilirbium of a matrix given an epsilon value
    x = [0] * columns
    y = [0] * rows

    if choice == 1: # Choice 1 represents a 3/4 epsilon - better naming can be used later
        maxListA = []
        maxListB = []
        aFlag = False
        bFlag = False
        aCell = []

        for i in range(0,rows):
            maxListA.append(max(A[i]))
            maxListB.append(max(B[i]))
        maxA = max(maxListA)
        maxB = max(maxListB)

        for i in range(0,rows):
            for j in range(0,columns):
                if A[i][j] == maxA and aFlag == False:
                    aCell = [i,j]
                    aFlag = True
                if B[i][j] == maxB and bFlag == False:
                    bCell = [i,j]
                    bFlag = True
            if aFlag and bFlag:
                break


        x[aCell[0]] += 0.5
        x[bCell[0]] += 0.5
        y[aCell[1]] += 0.5
        y[bCell[1]] += 0.5

    if choice == 2: #Choice 2 represents a 1/2 epsilon - I should change the naming of the variables at some point
        colMax = max(B[0])
        rowIndex = B[0].index(colMax)
        rowList = []

        for i in range(0,rows): # This creates a list which represents the chosen column
            rowList.append(A[i][rowIndex])

        rowMax = max(rowList)
        columnIndex = rowList.index(rowMax)
        x[0] += 0.5
        y[rowIndex] += 1.0
        x[columnIndex] += 0.5

    outputStringY = ""
    outputStringX = ""
    
    print("Here are the strategy profiles for the selected epsilon")
    
    for i in range(0,rows):
            outputStringY += "y" + str(i + 1) + " = " + str(y[i]) + " "
    for i in range(0,columns):
            outputStringX += "x" + str(i + 1) + " = " + str(x[i]) + " "

    print("Column player's strategy profile: ")
    print(outputStringY)
    print("Row player's strategy profile: ")
    print(outputStringX)

#This is the main of the code-should clean it up later
def main():
    typeResponse = input("Press any key to start or type exit to stop: ")
    inputResponse = ""
    
    while typeResponse != "exit" or inputResponse != "exit":
        print("_______________________________________________________")
        print("If you would like to calculate the Nash eqilibriums of a game press n")
        print("If you would like to find an approximate equilibrium of a game press a")
        print("If you would like to exit simply type exit")
        typeResponse = input("Enter your choice: ")

        if typeResponse != "n" and typeResponse!= "a" and typeResponse != "exit":
            print("Input is not a valid menu choice")
            continue
        print()

        if typeResponse == "exit":
            break

        print("If you would like to manually input a matrix press m")
        print("If you would like to use a matrix from a text file press t")
        print("If you would like to exit simply type exit")
        inputResponse = input("Enter your choice here: ")

        if inputResponse != "m" and inputResponse!= "t" and inputResponse != "exit":
            print("Input is not a valid menu choice")
            continue

        if inputResponse == "m":
            rows = int(input("Enter the number of rows in the payoff matrix: ")) # This sets the rows of the input matrix
            columns = int(input("Enter the number of columns in the payoff matrix: ")) # This sets the columns of the input matrix
            data = matrixInput(rows,columns) # This makes a matrix with all of the inputted matrix data

            if data == None:
                continue
            A =  (data[0]) # This is player 1's payoff matrix
            B =  (data[1]) # This is player 2's payoff matrix

        if inputResponse == "t":
            data = textParser()

            if data == None:
                continue

            A = (data[0])
            B = (data[1])
            rows = len(A)
            columns = len(A[0])

        if inputResponse == "exit":
            break

        printMatrix(A,B,rows,columns)
        
        if typeResponse == "n":
            nashEquilibriumCalculator(A,B,rows,columns)

        if typeResponse == "a":
            print("If you would like to use an epsilon of 3/4 enter 1")
            print("If you would like to use an epsilon of 1/2 enter 2")
            approxResponse = input("Enter your choice: ")
            approximateCalculator(A,B,rows,columns,int(approxResponse))
        

if __name__ == "__main__":
    main()
    print("END OF PROGRAM")
     # All matrix stuff has been done, just need to check if they are maximal now

    
    


