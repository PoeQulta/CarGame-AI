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
