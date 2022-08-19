import pygame
from functions import displayimage,displaytext,loadimage,scaleimage,drawrect,playmusic

pygame.init()

# declaring the global variable

width = 850
height = 700
fps = 90

# loading all the images

building = loadimage("assets/building.png")
city = loadimage("assets/city.png")
city = scaleimage(city,width,300)
logo = loadimage("assets/logo.png")

# defining the colors
displaycolor = "#163646"
pathcolor = "#f2e7e6"


display = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

def gameloop():
    buildingarr = [{
        "name":city,
        "x":0,
        "y":370,
        "width":width,
        "height":300
    }]

    # two corners of the initial block
    targetx1 = city.get_width()/2-65
    targetx2 = city.get_width()/2+120
    targety = 530

    # buildinginhand or blockinhand is nothing but the block which is moving here there on the top
    buildinginhand = {
        "name":building,
        "x":width/2,
        "y":10,
        "width":targetx2-targetx1,
        "height":100,
        "speedx":7,
        "speedy":0
    }

    rotating = True
    performdowning = False
    score = 0
    falling = {
        "name":building,
        "x":0,
        "y":0,
        "falling":False,
        "sizex":0,
        "sizey":100
    }

    count = 0

    # every block will be of 100px  left the initial building
    while True:

        if not pygame.mixer.music.get_busy():
            playmusic("assets/music.mp3")
            pygame.mixer.music.set_pos(30)

        # getting the events
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit()
            
            if e.type == pygame.KEYDOWN:
                if e.key ==pygame.K_SPACE:
                    if rotating:
                        rotating=False
                        buildinginhand.update({
                            "speedy":6
                        })
                        playmusic("assets/click.wav")

        display.fill(displaycolor)

        drawrect(display,pathcolor,0,10,width,100)

        if rotating:
            drawrect(display,pathcolor,buildinginhand["x"],buildinginhand["y"],buildinginhand["width"],height)
        
        for index,data in enumerate(buildingarr):
            displayimage(display,scaleimage(data["name"],data["width"],data["height"]),data["x"],data["y"])
        

        # displaying the block in the hand
        if rotating:
            if buildinginhand["x"]<0:
                buildinginhand.update({"speedx":6})
            if buildinginhand["x"]>(width-buildinginhand["width"]):
                buildinginhand.update({"speedx":-6})
                
            
        # update the position of the building in the hand
        buildinginhand.update({
            "x":buildinginhand["x"]+buildinginhand["speedx"] if rotating else buildinginhand["x"],
            "y":buildinginhand["y"]+buildinginhand["speedy"] if buildinginhand["y"]+buildinginhand["height"]-10<targety else buildinginhand["y"]
        })

        # removing the extra part of the block
        if buildinginhand["y"]+buildinginhand["height"]-10>targety:
            playmusic("assets/poof.mp3")
            decrement = 0
            if buildinginhand["x"]+buildinginhand["width"]<targetx1 or buildinginhand["x"]>targetx2:
                playmusic("assets/gameover.mp3")
                scorescreen(score)

            elif buildinginhand["x"]<targetx1:
                score+=1    
                decrement = targetx1-buildinginhand["x"]
                inix = buildinginhand["x"]
                buildinginhand.update({
                    "x":abs(buildinginhand["x"]+decrement),
                    "width":buildinginhand["width"]-decrement
                })
                falling.update({
                    "x":inix,
                    "y":buildinginhand["y"],
                    "falling":True,
                    "sizex":decrement
                })
            elif buildinginhand["x"]>targetx1:
                score+=1
                decrement = buildinginhand["x"]+buildinginhand["width"]-targetx2
                inix = buildinginhand["x"]+buildinginhand["width"]-decrement
                buildinginhand.update({
                    "width":buildinginhand["width"]-decrement,
                })
                falling.update({
                    "x":inix,
                    "y":buildinginhand["y"],
                    "falling":True,
                    "sizex":decrement
                })
            else:
                score+=1    
                performdowning=True
            targetx1 = buildinginhand["x"]
            targetx2 = buildinginhand["x"]+buildinginhand["width"]
            buildingarr.append(buildinginhand)
            buildinginhand = {
                "name":building,
                "x":width/2,
                "y":10,
                "width":targetx2-targetx1,
                "height":100,
                "speedx":7,
                "speedy":0,
            }
        
        if falling["falling"]:
            displayimage(display,scaleimage(falling["name"],falling["sizex"],falling["sizey"]),falling["x"],falling["y"])
            falling.update({
                "y":falling["y"]+8
            })
            if falling["y"]>height:
                performdowning=True
                falling.update({"falling":False})

        # to move all the blocks down
        if performdowning:
            for index,data in enumerate(buildingarr):
                data.update({
                    "y":data["y"]+5
                })
            count +=5
            if count==100 or count>100:
                count=0
                performdowning = False
                rotating = True
            

        # checking whether the width of the building has become smaller than zero or not
        if buildinginhand["width"]<0:
            playmusic("assets/gameover.mp3")
            scorescreen(score)


        # displaying the block in hand
        displayimage(display,scaleimage(buildinginhand["name"],buildinginhand["width"],buildinginhand["height"]),buildinginhand["x"],buildinginhand["y"])

        # displaying the score
        displaytext(display,f"Score :- {score}",10,10,30,"black",True,True)
        

        # some other stuffs
        pygame.display.update()
        clock.tick(fps)

def homescreen():
    speed = 7
    x = 10
    y = 10
    targetx1 = city.get_width()/2-65
    targetx2 = city.get_width()/2+120
    scaledbuilding = pygame.transform.scale(building,(targetx2-targetx1,100))
    while True:
        if not pygame.mixer.music.get_busy():
            playmusic("assets/music.mp3")
            pygame.mixer.music.set_pos(22)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    gameloop()
        
        display.fill(displaycolor)
        drawrect(display,pathcolor,x,y,scaledbuilding.get_width(),height)
        drawrect(display,pathcolor,0,10,width,100)
        displayimage(display,scaledbuilding,x,y)
        if x<0:
            speed = 7
        if x+scaledbuilding.get_width()>width:
            speed = -7
        x+=speed

        displayimage(display,scaleimage(city,width,300),0,370)

        displaytext(display,"Press Space Bar To Start The Game",width/2-250,height/2-39,40,"black",True,True)
        displayimage(display,scaleimage(logo,400,140),width/2-200,height/2-240)

        pygame.display.update()

def scorescreen(score):
    try:
        data  = open("data.txt","r+")
        if len(data.readline())<=0:
            print("entered")
            data.write("0")
        data.seek(0)
        showhighscore = False

        if int(data.readline())<score:
            showhighscore=True
            data = open("data.txt","w")
            data.write(f"{score}")
        
        while True:
            if not pygame.mixer.music.get_busy():
                playmusic("assets/music.mp3")
                pygame.mixer.music.set_pos(22)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    quit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE:
                        gameloop()
                    if e.key == pygame.K_h:
                        homescreen()

            display.fill(displaycolor)
            displayimage(display,scaleimage(city,width,300),0,370)

            displaytext(display,"Congrats Hight score" if showhighscore else "Well Played",300 if not showhighscore else 200,50,60,"white",True,True)
            displaytext(display,f"Score:-{score}",width/2-100,height/2-200,60,"blue",False,True)
            displaytext(display,"Press Space Bar To Restart",width/2-170,height/2-100,40,"black",False,True)
            displaytext(display,"OR",width/2-20,height/2-46,40,"black",False,True)
            displaytext(display,"Press H To Move Back To Home Screen",width/2-240,height/2+10,40,"black",False,True)
            pygame.display.update()
    except Exception as e:
        data = open("data.txt")
        data.write("0")
            





homescreen()