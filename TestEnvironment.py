import pygame, neat, pickle, os
import sys
from Track import Track
from Car import Car
import math
def Draw(car,track):
    screen.fill(pygame.Color(0,0,0))
    screen.blit(trackSurface, (0,0))
    screen.blit(car.surf, car.rect)


def get_colorkey_hitmask(image,rect, key=None):
    """returns a hitmask using an image's colorkey.
       image->pygame Surface,
       rect->pygame Rect that fits image,
       key->an over-ride color, if not None will be used instead of the image's colorkey"""
    if key==None:colorkey=image.get_colorkey()
    else:colorkey=key
    mask=[]
    for x in range(1000):
        mask.append([])
        for y in range(800):
            mask[x].append(not image.get_at((x,y)) == colorkey)
    return mask
def get_alpha_hitmask(image, rect, alpha=1):
    """returns a hitmask using an image's alpha.
       image->pygame Surface,
       rect->pygame Rect that fits image,
       alpha->the alpha amount that is invisible in collisions"""
    mask=[]
    for x in range(rect.width):
        mask.append([])
        for y in range(rect.height):
            try:
                mask[x].append(not image.get_at((x,y))[3]==alpha)
            except:
                mask[x].append(False)
    return mask


def PixelPerfectCollision(obj1, obj2):
    """
    If the function finds a collision, it will return True;
    if not, it will return False. If one of the objects is
    not the intended type, the function instead returns None.
    """
    try:
        #create attributes
        rect1, mask1, blank1 = obj1.rect, obj1.hitmask, obj1.blank
        rect2, mask2, blank2 = obj2.rect, obj2.hitmask, obj2.blank
        if not rect1.colliderect(rect2):
            return False
    except AttributeError:
        return None

    #get the overlapping area
    clip = rect1.clip(rect2)
    #pygame.draw.rect(debugSurf, pygame.Color(255,0,0) ,clip)
    #find where clip's top-left point is in both rectangles
    x2 = clip.left - rect2.left
    y2 = clip.top  - rect2.top
    #print("the variables {} {} {} {}".format(x1,y1,x2,y2))
    #cycle through clip's area of the hitmasks
    for x in range(clip.width):
        for y in range(clip.height):
            #returns True if neither pixel is blank
            try:
                if mask1[x][y] is not True and mask2[x2+x][y2+y] is not True:
                    return True
            except Exception as e : print(e)
    #if there was neither collision nor error
    return False

def NewTrack():
    valtr = Track(20, screenSize)
    pygame.draw.polygon(trackSurface, WHITE, valtr.getOuterBound())
    pygame.draw.polygon(trackSurface, Black, valtr.getInnerBound())
    return valtr

screenSize = 1000, 800
clock = pygame.time.Clock()
trackSurface = pygame.Surface(screenSize)
debugSurf = pygame.Surface(screenSize)
debugSurf.set_colorkey(pygame.Color(0, 0, 0))
trackSurfaceRect = trackSurface.get_rect()
Black = pygame.Color(0,0,0)
WHITE = pygame.Color(255,255,255)
screen = pygame.display.set_mode(screenSize)
pygame.init()
def main():
    valtr = NewTrack()
    #print(valtr.edges)
    valtr.surf = trackSurface
    valtr.rect = trackSurfaceRect
    valtr.surf.set_colorkey(pygame.Color(0, 0, 0))
    valtr.hitmask = get_colorkey_hitmask(valtr.surf, valtr.rect)
    averageX = (valtr.getOuterBound()[0][0]+valtr.getInnerBound()[0][0])/2
    averageY = (valtr.getOuterBound()[0][1]+valtr.getInnerBound()[0][1])/2
    alignmentVec = (valtr.getInnerBound()[0][0]-valtr.getInnerBound()[1][0],valtr.getInnerBound()[0][1]-valtr.getInnerBound()[1][1])
    cordinates = (averageX, averageY)
    car = Car(cordinates, alignmentVec)

    car.hitmask = get_alpha_hitmask(car.surf,car.rect)
    screen.blit(trackSurface,(0,0))
    #print(valtr.hitmask)
    while 1:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            car.motion = 1
        elif keys[pygame.K_s]:
            car.motion = -1
        else:
            car.motion = 0

        if keys[pygame.K_a]:
            car.angleSpeed = 2
        elif keys[pygame.K_d]:
            car.angleSpeed = -2
        else:
            car.angleSpeed = 0

        car.move()
        car.hitmask = get_alpha_hitmask(car.surf, car.rect)
        #print(len(car.hitmask))
        #print(PixelPerfectCollision(car, valtr))
        directions = [car.acceleration.normalize(),car.acceleration.normalize().rotate(45),car.acceleration.normalize().rotate(90),car.acceleration.normalize().rotate(270)]
        car.points =list()
        car.collisions = list()
        car.distances = list()
        for i in range(len(directions)):
            point,distance = car.DetectEdges(valtr, directions[i])
            car.collisions.append(point)
            car.distances.append(distance)
        Draw(car,valtr)

        pygame.display.update()

main()
