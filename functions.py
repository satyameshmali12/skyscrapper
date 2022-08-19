import pygame
import os
import webbrowser

def openurl(url):
    webbrowser.open_new_tab(url)  

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

def listallthefiles(name):
    dir = os.listdir(name)
    images = []
    for i in range(len(dir)):
        images.append(pygame.image.load(f"{name}/{dir[i]}"))        
    return images

def playmusic(name):
    pygame.mixer.music.load(name)
    pygame.mixer.music.play()

def drawrect(display,color,x,y,sizex,sizey):
    pygame.draw.rect(display,color,(x,y,sizex,sizey))

# this function is to check whether the button is pressed or not
def checkwhetherbuttonpressed(button,buttonx,buttony,mousex,mousey,iftrue,iffalse):
    if mousex>buttonx and mousex<buttonx+button.get_width() and mousey>buttony and mousey<buttony+button.get_height():
        return iftrue
    else:
        iffalse