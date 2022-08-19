import pygame

def loadimage(name):
    img = pygame.image.load(name)
    return img

def scaleimage(name,width,height):
    scaledimg = pygame.transform.scale(name,(width,height))
    return scaledimg

def displayimage(display,name,x,y):
    display.blit(name,(x,y))

def displaytext(display,text,x,y,size,color,bold,italic):
    font = pygame.font.SysFont(None,size,bold,italic)
    text = font.render(text,True,color)
    display.blit(text,(x,y))

def playmusic(name):
    pygame.mixer.music.load(name)
    pygame.mixer.music.play()

def drawrect(display,color,x,y,sizex,sizey):
    pygame.draw.rect(display,color,(x,y,sizex,sizey))
