#Project Procedures:
#1. Put preconditions where needed.
#2. If the method name doesn't tell you what the method does, add a post condition or change the method name
#3. If there's a feature that needs to be added or something that needs to be worked on, just add a TODO comment followed by a parenthetical of who needs to do it.
#4. Add a comment with what each function returns/does at the heading of the function.
#All documentation rules apply. If you see a mistake in the documentation, fix it! It really helps with debugging.


import matplotlib
from matplotlib import pyplot as plt
import numpy as np

#In the function, standard symbols and procedures:
#It gets parsed into an int[] in turn. This int[] is of the format:
#[highestDegCoef, highestDeg-1Coef,..., coefOfx,constant]
#For the example x^3 + 3x^2 - x/6 + 1,
#[1,3,-1/6,1] would be the int[].
class Function:
    def __init__(self,intarr, degree:int): # Function constructor
        self.expression = intarr
        self.degree = degree
    def evalAtPoint(self, x:float): # Evaluates the Function at point x and returns the value
        #sets the current degree equal to the highest degree
        currDegree = self.degree
        currY = 0
        for i in self.expression:
            currY += i*x**currDegree
            currDegree -= 1 
            #print(currY, currDegree) Debug line
            #The current degree goes down by one because we are headed to the next degree
        return currY
    def multipleEvalAtPoint(self,x): #Evaluates the Function at each element in the list x and returns the array of values
        listThing = [] #The list to append values to
        for i in x:
            listThing.append(self.evalAtPoint(i)) #Appends the y value that corresponds to the x value
        return listThing
    def plot(self, start:float, end:float): #Plots the function. You must use plt.ion() after this method has been run
        figure = plt.figure() #Creates a nonlinear figure
        x = np.linspace(start, end, 100*(abs(end-start))) #Creates an array of 100 times the width of the full function evenly spaced x values between start and end
        plt.plot(x,self.multipleEvalAtPoint(x), '-') #Plots the x array on the x axis and an array with all the values of the function according to the x values on the y axis
#Params:
#f: a valid instance of a function
#step: a float that represents the width of one rectangle
#start: the first number the Rienmann Sum should start to be evaluated at. In [a,b], a.
#end: the last number the Rienmann Sum should be evaluated at. In [a,b], b.
def rightRienmannSum(f:Function, step:float, start:int, end:int): #Certified As Working: Returns a floating point number which is the Right Rienmann Sum of f from start to end.
    currentSum = 0
    for i in np.arange(start+step,end+step,step):
        x = f.evalAtPoint((i))
        
        currentSum += x * step 
    return currentSum
def leftRienmannSum(f:Function, step:float, start:int, end:int): #Certified As Working: Returns a floating point number that is the left Rienmann sum of f from start to end.
    
    currentSum = 0
    for i in np.arange(start,end,step):
        x = f.evalAtPoint(i)
        currentSum += x * step 
    return currentSum
def midpointRienmannSum(f:Function, step:float, start:int, end:int): #Certified As Working: Returns a floating point number that is the midpoint Rienmann sum of f from start to end.
    
    currentSum = 0
    for i in np.arange((start+start+step)/2,(end+end+step)/2,step):
        x = f.evalAtPoint(i)
        currentSum += x*step
    return currentSum     
def trapezoidalRienmannSum(f:Function, step:float, start:int, end:int): #Certified As Working: Returns a floating point number that is the trapezoidal Rienmann sum of f from start to end.
    currentSum = 0
    x = 0
    for i in np.arange(start+step,end+step,step):
        x = (f.evalAtPoint((i))+f.evalAtPoint((i-step)))/2
        #print(x)

        currentSum += x * step 
    return currentSum
#Precondition: Must have a PyPlot created. Must not be shown. Call the plt.ion() method after this runs.
#TODO add the areas to the middle of each shape (We'll figure it out later)
#TODO make colors uniform in rectangle graphs (Andrew)
def leftRectangleCreator(f:Function, step:float, start:int, end:int):
    yVerLine = []
    xVerLine1 = []
    xHorLine1 = []
    yHorLine1 = []
    xVerLine2 = []
    
    for i in np.arange(start,end,step):
        x = f.evalAtPoint(i)
        yVerLine = np.arange(0, x+step, step)
        xVerLine1 = []
        xVerLine2 = []
        for j in yVerLine:
            xVerLine1.append(i)
            xVerLine2.append(i+step)
        xHorLine1 = [i, i+step]
        yHorLine1 = [x, x]
        plt.plot(xVerLine1, yVerLine)
        plt.plot(xVerLine2, yVerLine)
        plt.plot(xHorLine1, yHorLine1)
    plt.title("Left Rienmann Sum of the Given Table: "+str(leftRienmannSum(f,step,start,end)))
        #Now adding the area of each rectangle to its center
        #a = fig.add_subplot()
        #fig.text(i/2, x/2, str(step*x))
def rightRectangleCreator(f:Function, step:float, start:int, end:int):
    yVerLine = []
    xVerLine1 = []
    xHorLine1 = []
    yHorLine1 = []
    xVerLine2 = []
    
    for i in np.arange(start+step,end+step,step):
        x = f.evalAtPoint(i)
        yVerLine = np.arange(0, x+step, step)
        xVerLine1 = []
        xVerLine2 = []
        for j in yVerLine:
            xVerLine1.append(i)
            xVerLine2.append(i-step)
        xHorLine1 = [i, i-step]
        yHorLine1 = [x, x]
        plt.plot(xVerLine1, yVerLine)
        plt.plot(xVerLine2, yVerLine)
        plt.plot(xHorLine1, yHorLine1)
    plt.title("Right Rienmann Sum of the Given Table: "+str(rightRienmannSum(f,step,start,end)))

        #a = fig.add_subplot()
        #fig.text(i/2, x/2, str(step*x))
def midpointRectangleCreator(f:Function,step:float,start:int,end:int):
    yVerLine = []
    xVerLine1 = []
    xHorLine1 = []
    yHorLine1 = []
    xVerLine2 = []
    
    for i in np.arange(start,end,step):
        x = f.evalAtPoint((i+i+step)/2)
        yVerLine = np.arange(0, x+step, step)
        xVerLine1 = []
        xVerLine2 = []
        for j in yVerLine:
            xVerLine1.append(i)
            xVerLine2.append(i+step)
        xHorLine1 = [i, i+step]
        yHorLine1 = [x, x]
        plt.plot(xVerLine1, yVerLine)
        plt.plot(xVerLine2, yVerLine)
        plt.plot(xHorLine1, yHorLine1)
    plt.title("Midpoint Rienmann Sum of the Given Table: "+str(midpointRienmannSum(f,step,start,end)))

        #a = fig.add_subplot()
       # fig.text(i/2, x/2, str(step*x))
def trapezoidCreator(f:Function, step:float, start:int, end:int):
    yVerLine1 = []
    yVerLine2 = []
    xVerLine1 = []
    xVerLine2 = []
    xHorLine = []
    yHorLine = []
    for i in np.arange(start+step,end+step,step):
        y1 = (f.evalAtPoint((i-step)))
        y2 = f.evalAtPoint((i))
        xVerLine1 = []
        xVerLine2 = []
        yVerLine1 = np.arange(0, y1+step, step)
        yVerLine2 = np.arange(0, y2+step, step)
        for j in yVerLine1:
            xVerLine1.append(i-step)
        for h in yVerLine2:
            xVerLine2.append(i)
        xHorLine = [i-step, i]
        yHorLine = [y1, y2]
        plt.plot(xVerLine1, yVerLine1)
        plt.plot(xVerLine2, yVerLine2)
        plt.plot(xHorLine, yHorLine)
    plt.title("Trapezoidal Rienmann Sum of the Given Table: "+str(trapezoidalRienmannSum(f,step,start,end)))
        #a = fig.add_subplot()
        #fig.text(i/2, y1/2, str(step/2*(y1+y2)))

#Tester
a = int(input("How many degrees in the polynomial?"))
numArr = []
for i in range(a,-1,-1):
    numArr.append(int(input("Enter the "+str(i)+"th degree.")))
start = int(input("What is the starting value for the integral to be evaluated? "))
end = int(input("What is the ending value for the integral to be evaluated? "))
step = float(input("What is the step of the integral? "))
figure = plt.figure()
x = np.linspace(start, end, 100)
plt.plot(x,Function(numArr, len(numArr)-1).multipleEvalAtPoint(x), '-')
#leftRectangleCreator(Function(numArr, len(numArr)-1), step, start, end, figure)
#rightRectangleCreator(Function(numArr, len(numArr)-1), step, start, end, figure)
#midpointRectangleCreator(Function(numArr, len(numArr)-1), step, start, end, figure)
trapezoidCreator(Function(numArr, len(numArr)-1), step, start, end, figure)
plt.ion()
