import random
import math
import numpy as np
class ValtrAlgorithm:
    def __init__(self, size, screenSize):
        self.__points = []
        self.GenerateRandConvPoly(size, screenSize)


    def GenerateRandConvPoly(self, size, screenSize):
        # Create list of random x and y values
        xPool = []
        yPool = []
        for i in range(size):
            xPool.append(random.randint(50,screenSize[0]-50))
            yPool.append(random.randint(50,screenSize[1]-50))
        #sort the lists
        xPool.sort()
        yPool.sort()
        # seperate extreme points
        xMax = xPool[-1]
        xMin = xPool[0]
        yMax = yPool[-1]
        yMin = yPool[0]
        # seperate into two chains (directions) and extract vector translations
        xVec = []
        yVec = []
        lastTop = xMin
        lastBot = xMin
        for i in range(size -2):
            i+=1
            x = xPool[i]
            if bool(random.getrandbits(1)):
                xVec.append(x - lastTop)
                lastTop = x
            else:
                xVec.append(lastBot - x)
                lastBot = x
        xVec.append(xMax - lastTop)
        xVec.append(lastBot - xMax)
        lastleft = yMin
        lastRight = yMin
        for i in range(size - 2):
            i += 1
            y = yPool[i]
            if bool(random.getrandbits(1)):
                yVec.append(y - lastleft)
                lastleft = y
            else:
                yVec.append(lastRight - y)
                lastRight = y
        yVec.append(yMax - lastleft)
        yVec.append(lastRight - yMax)

        random.shuffle(yVec)
        vectors = []
        for i in range(size):
            vectors.append((xVec[i],yVec[i]))
        # sort according to angle
        vectors = sorted(vectors, key= lambda t:math.atan2(t[1],t[0]))
        # lay vectors end to end
        x = 0
        y = 0
        minPolyX = 0
        minPolyY = 0
        for i in range(size):
            self.__points.append((x,y))
            x += vectors[i][0]
            y += vectors[i][1]
            minPolyX = min(minPolyX,x)
            minPolyY = min(minPolyY,y)

        # scale

        self.__ShiftPoints(xMin,minPolyX,yMin,minPolyY)


    def getPolyCentroid(self):
        arr = np.array(self.__points)

        length = arr.shape[0]
        xSum = np.sum(arr[:,0])
        ySum = np.sum(arr[:,1])
        return (xSum/length,ySum/length)


    def __ShiftPoints(self,xMin,minPolyX,yMin,minPolyY):
        # shift from origin
        xShift = (xMin - minPolyX)
        yShift = (yMin - minPolyY)
        for i in range(len(self.__points)):
            self.__points[i] = (self.__points[i][0] + xShift, self.__points[i][1] + yShift)

    def getPoly(self):
        return self.__points
    @staticmethod
    def CalculateCentroid(poly):
        arr = np.array(poly)

        length = arr.shape[0]
        xSum = np.sum(arr[:,0])
        ySum = np.sum(arr[:,1])
        return (xSum/length,ySum/length)