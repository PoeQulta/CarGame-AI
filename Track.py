from ValtrAlgorithm import ValtrAlgorithm as VA
import pygame
from pygame.math import Vector2
class Track(VA):
    def __init__(self, size, screenSize):
        super().__init__(size,screenSize)
        self.GenerateTrack()
        self.surf = None
        self.rect = None
        self.hitmask = None
        self.blank = False
        self.edges = [self.__VectorEdges(self.__outerBound),self.__VectorEdges(self.__innerBound)]

    def BezierCurve(self,xshift=5):
        self.bezier = []
        for i,point in enumerate(self.__outerBound):
            gradients = [0,0]
            try:

                gradients[0] = (point[1]-self.__outerBound[i-1][1])/(point[0]-self.__outerBound[i-1][0])

            except:
                print("error")
                gradients[0] = 0
            try:
                gradients[1] = (point[1]-self.__outerBound[(i+1)%len(self.__outerBound)][1])/(point[0]-self.__outerBound[(i+1)%len(self.__outerBound)][0])
            except:
                print("error")
                gradients[1] = 0
            print(gradients)
            controlpoints = [(point[0]-xshift,point[1]-(xshift*gradients[0])),(point[0]+xshift,point[1]+(xshift*gradients[1]))]
            t = 0
            for count in range(50):
                x = ((1-t)**2)*controlpoints[0][0] + 2*(1-t)*t*point[0] + (t**2)*controlpoints[1][0]
                y = ((1-t)**2)*controlpoints[0][1] + 2*(1-t)*t*point[1] + (t**2)*controlpoints[1][1]
                self.bezier.append((x,y))
                t +=0.02
        print(self.bezier)

    def scale(self,tup):
        return (tup[0] * 0.7, tup[1] * 0.7)

    def ShiftPoints(self,points, xEndPos, xStartPos, yEndPos, yStartPos):
        # shift from origin
        xShift = (xEndPos - xStartPos)
        yShift = (yEndPos - yStartPos)
        for i in range(len(points)):
            points[i] = (points[i][0] + xShift, points[i][1] + yShift)
        return points
    def CenterPoly(self,centeroid,center,points):
        centered = self.ShiftPoints(points,center[0],centeroid[0],center[1],centeroid[1])
        return centered
    def GenerateTrack(self):
        self.__outerBound = self.getPoly()
        scaledPoly = list(map(self.scale,self.getPoly()))
        scaledPolyCentroid = VA.CalculateCentroid(scaledPoly)
        self.__innerBound = self.CenterPoly(scaledPolyCentroid,self.getPolyCentroid(),scaledPoly)

    def getOuterBound(self):
        return self.__outerBound
    def getInnerBound(self):
        return self.__innerBound
    def __VectorEdges(self,poly):
        lines = list()
        length = len(poly)
        for i,point in enumerate(poly):
            vector = Vector2(poly[(i+1)%length][0]-point[0],poly[(i+1)%length][1]-point[1])
            #vector = vector.normalize()
            line = [point,vector]
            lines.append(line)
        return lines