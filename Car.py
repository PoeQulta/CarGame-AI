import pygame
from pygame.math import Vector2 as vec
import math
from PointInPoly import *
import numpy as np
RED = pygame.Color(255,0,0)
class Car(pygame.sprite.Sprite):
    def __init__(self,cordinates,alignment=0):
        #pygame stuff
        pygame.sprite.Sprite.__init__(self)
        intialVec = vec(0,1)
        self.surf = pygame.image.load("Sprites/CarSprite.png")
        self.__origisurf = self.surf
        self.rect = self.surf.get_rect()
        self.rect.center = cordinates
        self.position = vec(cordinates)
        #Physics stuff
        self.velocity = vec(0,0)
        self.acceleration = vec(0,-0.1)
        self.angleSpeed = 0
        self.angle = -intialVec.angle_to(vec(alignment))
        self.surf = pygame.transform.rotozoom(self.__origisurf, self.angle, 1)
        self.velocity = self.velocity.rotate(self.angle*-1)
        self.acceleration = self.acceleration.rotate(self.angle*-1)
        self.motion = 0
        #collision detection and Colllision prediction
        self.hitmask = None
        self.blank = False
        self.points = list()
        self.collisions = list()
        self.distances = list()

    def move(self):
        #if no throttle coast to a stop
        if self.motion == 0:
            self.velocity = 0.8* self.velocity
        else:
            self.velocity += self.acceleration*self.motion
        #velocity peaks at 10
        if self.velocity.length()>10:
            self.velocity.scale_to_length(10)
        self.Rotate()
        #pygame stuff
        self.position += self.velocity
        self.rect = self.surf.get_rect(center = self.position)



    def Rotate(self):
        #sprite cannot rotate while car is stationary
        if (not self.angleSpeed ==0) and self.velocity.magnitude() > 0.5:
            #scale omega with respect to velocity
            self.angleSpeed = self.angleSpeed * 0.2*self.velocity.magnitude()*self.motion
            self.angle += self.angleSpeed
            #rotate velocity & acceleration vectors so they remain stationary relative to sprite
            self.velocity = self.velocity.rotate(self.angleSpeed*-1)
            self.acceleration = self.acceleration.rotate(self.angleSpeed*-1)
            self.surf = pygame.transform.rotozoom(self.__origisurf, self.angle , 1)
    def Accelerate(self, acc):
        self.acceleration.scale_to_length(acc)


    def DetectEdges(self,track,direction): #get point and distance of nearest collision with vector direction
        x1 = self.rect.center[0]
        y1 = self.rect.center[1]
        vx1 = direction.x
        vy1 = direction.y
        lamdas = list()
        #get points of collision of inner edges
        for line in track.edges[1]:
            x3 = line[0][0]
            y3 = line[0][1]
            vx2 = line[1].x
            vy2 = line[1].y
            try:lamdas.append(((x3*vy2)-(x1*vy2)+(y1*vx2)-(y3*vx2))/((vx1*vy2)-(vy1*vx2)))
            except: lamdas.append(math.inf)
        #filter negative values and sort ascendingly
        lamdas = [lamda for lamda in lamdas if lamda>0]
        lamdas.sort()
        allOutside = True
        #check if any of the detect points are on the inner polygons if not then check outer edge
        for lamda in lamdas:
            query = tuple(self.rect.center + (lamda+0.1) * direction)
            if not wn_PnPoly(query,track.getInnerBound()) == 0:
                allOutside = False
                smallest = lamda
                break
        if allOutside:
            lamdas = list()
            for line in track.edges[0]:
                x3 = line[0][0]
                y3 = line[0][1]
                vx2 = line[1].x
                vy2 = line[1].y
                try:lamdas.append(((x3*vy2)-(x1*vy2)+(y1*vx2)-(y3*vx2))/((vx1*vy2)-(vy1*vx2)))
                except: lamdas.append(math.inf)

            smallest = min(lamda for lamda in lamdas if lamda>0)
        return(tuple(self.rect.center + smallest * direction),smallest)
