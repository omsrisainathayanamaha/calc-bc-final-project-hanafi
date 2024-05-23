#Everything recoded for tables!
#All documentation rules apply. If you see a mistake in the documentation, fix it! It really helps with debugging.
#CHANGE MADE: Made the graph interactive so the betting will now actually work!
from matplotlib import pyplot as plt
import numpy as np




class Table: #A class that represents a table of values.
    def __init__(self, xArr:list[float], yArr:list[float]):
        xArr.sort()
        yArr.sort()
        self.xValues:list[float] = xArr
       # print(xArr, self.xValues)
        self.yValues:list[float] = yArr
        #print(yArr, self.yValues)

        
  
    def getXValues(self): #returns the list of x values in the table
        return self.xValues
    def getFirstXValue(self): #returns the smallest x value in the table
        return self.xValues.min()
    def getLastXValue(self): #returns the biggest x value in the table
        return self.xValues.max()
    def getFirstYValue(self): #returns the smallest y value in the table
        return self.yValues.min()
    def getLastYValue(self): #returns the biggest y value in the table
        return self.yValues.max()
    def getYValues(self): #returns the list of y values in the table
        return self.yValues
    def plot(self): #creates a scatter plot of all the values. Must call plt.ion() after
         plt.scatter(self.xValues,self.yValues)
#TODO test tableLeftRienmannSum() (Sahanav)
#Parameters:
#t: a valid, instantiated table
#startIndex: the index of the x-value in the array to start the Rienmann Sum
#endIndex: the index of the x-value in the array to end the Rienmann Sum
def tableLeftRienmannSum(t:Table, startIndex:int, endIndex:int): #Returns a floating point number that is the left Rienmann Sum of the table t from the x-values x[startIndex] to x[endIndex]
    x = t.getXValues()[startIndex:endIndex]   # starts at 
    y = t.getYValues()[startIndex:endIndex]
    print(y)
    currentSum = 0
    index = 0
    for i in y:
        currentSum += (abs(x[index-1]-x[index]))*i #finds the difference between the two x values and multiplies it by the y
        index += 1
    return currentSum

def tableRightRienmannSum(t, startIndex, endIndex): #Returns a floating point number that is the right Rienmann Sum of the table t using the subintervals provided from the x-value x[startIndex] to x[endIndex]
    x = t.getXValues()[startIndex:endIndex+1]
    y = t.getYValues()[startIndex+1:endIndex+1]
    currentSum = 0
    index = 1
    for i in y:
        print("Current y value", i)
        print("Thing to be added to current sum between x values ", x[index], x[index-1], ":", (abs(x[index]-x[index-1])*i))
        currentSum += (x[index]-x[index-1])*i
        index += 1
    return currentSum
#Precondition: The table must have an intermediate value in between each set of two values.
#Example:
#In the table with xValues [1,3,4,5,6,7,8], the only section of the array tableMidpointRienmannSum() can use is [4,5,6,7,8].
#In this example, tableMidpointRienmannSum() will evaluate with n = 2 rectangles, using the y values for x = 5 and x = 7 to find it
#tableMidpointRienmannSum() will NOT validate arrays. All validation must be done before tableMidpointRienmannSum() is called.
def tableMidpointRienmannSum(t:Table, startIndex:int, endIndex:int):
    
    x = t.getXValues()[startIndex:endIndex+1]
    y = t.getYValues()[startIndex:endIndex+1]
    currentSum = 0
    index = 1
    while (index <= len(x)-2):
        currentSum += y[index]*(x[index+1]-x[index-1])
        print("length", len(x), x, "length y", len(y), y)
        print("Current y value", y[index])
        print(index)
        print("Thing to be added to current sum between x values ", x[index+1], x[index-1], ":", (abs(x[index]-x[index-1])*y[index]))
        index +=2
    return currentSum
def tableTrapezoidalRienmannSum(t:Table, startIndex:int, endIndex:int):
    x = t.getXValues()[startIndex:endIndex+1]
    y = t.getYValues()[startIndex:endIndex+1]
    currentSum = 0
    
    for i in range(len(y)-1):
        
        currentSum += (1/2)*(x[i+1]-x[i])*(y[i+1]+y[i])
        
    return currentSum
def tableLeftRectangle(t:Table, startIndex:int, endIndex:int):
    xs = t.getXValues()
    ys = t.getYValues()
    yVerLine = []
    xVerLine1 = []
    xHorLine1 = []
    yHorLine1 = []
    xVerLine2 = []
    index = startIndex
    for i in xs[startIndex:(endIndex)]:
        x = ys[index]
        yVerLine = [0, x]
        xVerLine1 = [i,i]
        xVerLine2 = [xs[index+1], xs[index+1]]
        
        xHorLine1 = [i, xs[index+1]]
        yHorLine1 = [x, x]
        plt.plot(xVerLine1, yVerLine)
        plt.plot(xVerLine2, yVerLine)
        plt.plot(xHorLine1, yHorLine1)
        index-=-1
    plt.title("Left Rienmann Sum of the Given Table: "+str(tableLeftRienmannSum(t,startIndex,endIndex)))
def tableRightRectangle(t:Table, startIndex:int, endIndex:int):
    xs = t.getXValues()
    ys = t.getYValues()
    yVerLine = []
    xVerLine1 = []
    xHorLine1 = []
    yHorLine1 = []
    xVerLine2 = []
    index = startIndex+1
    for i in xs[startIndex+1:(endIndex+1)]:
        x = ys[index]
        yVerLine = [0, x]
        xVerLine1 = [i,i]
        xVerLine2 = [xs[index-1], xs[index-1]]
        
        xHorLine1 = [i, xs[index-1]]
        yHorLine1 = [x, x]
        plt.plot(xVerLine1, yVerLine)
        plt.plot(xVerLine2, yVerLine)
        plt.plot(xHorLine1, yHorLine1)
        index-=-1
    plt.title("Right Rienmann Sum of the Given Table" + str(tableRightRienmannSum(t,startIndex,endIndex)))
#Precondition: The table must have an intermediate value in between each set of two values.
#Example:
#In the table with xValues [1,3,4,5,6,7,8], the only section of the array tableMidpointRectangle() can use is [4,5,6,7,8].
#In this example, tableMidpointRectangle() will evaluate with n = 2 rectangles, using the y values for x = 5 and x = 7 to find it
#tableMidpointRectangle() will NOT validate arrays. All validation must be done before tableMidpointRectangle() is called.
def tableMidpointRectangle(t:Table, startIndex:int, endIndex:int):
    xs = t.getXValues()
    ys = t.getYValues()
    yVerLine = []
    xVerLine1 = []
    xHorLine1 = []
    xVerLine2 = []
    #index = startIndex+1
    for index in range(startIndex+1, endIndex+1, 2):
        yVerLine = [0, ys[index]]
        xVerLine1 = [xs[index-1], xs[index-1]]
        xVerLine2 = [xs[index+1], xs[index+1]]

        xHorLine1 = [xs[index-1], xs[index+1]]
        yHorLine1 = [ys[index], ys[index]]
        
        plt.plot(xVerLine1, yVerLine)
        plt.plot(xVerLine2, yVerLine)
        plt.plot(xHorLine1, yHorLine1)
    plt.title("Middle Rienmann Sum of the Given Table" + str(tableMidpointRienmannSum(t,startIndex,endIndex)))
def tableTrapezoids(t, startIndex, endIndex):
    xs = t.getXValues()
    ys = t.getYValues()
    for index in range(startIndex, endIndex):
        yVerLine1 = [0, ys[index]]
        yVerLine2 = [0, ys[index+1]]
        xVerLine1 = [xs[index], xs[index]]
        xVerLine2 = [xs[index+1], xs[index+1]]

        xHorLine = [xs[index], xs[index+1]]
        yHorLine = [ys[index], ys[index+1]]

        plt.plot(xVerLine1, yVerLine1)
        plt.plot(xVerLine2, yVerLine2)
        plt.plot(xHorLine, yHorLine)
    plt.title("Trapezoidal Rienmann Sum of the Given Table " + str(tableTrapezoidalRienmannSum(t,startIndex,endIndex)))

        
#Tester
xArr = [1,2,3,4,5]
yArr = [0,4,16,36,64]
t = Table(xArr,yArr)
startIndex = 0
endIndex = len(xArr)-1
print("Left", tableLeftRienmannSum(t, startIndex, endIndex)) #works
print("Right", tableRightRienmannSum(t, startIndex, endIndex)) #works
print("Midpoint", tableMidpointRienmannSum(t, startIndex,endIndex)) #works
print("Trapezoidal", tableTrapezoidalRienmannSum(t, startIndex,endIndex)) #works
t.plot()
tableRightRectangle(t, startIndex, endIndex)
tableLeftRectangle(t, startIndex, endIndex) #RUNS BUT STOPS AT 4 IN THE GRAPH
tableMidpointRectangle(t, startIndex, endIndex)
tableTrapezoids(t, startIndex,endIndex)
plt.ion()
        
    


    
    
    

    
     