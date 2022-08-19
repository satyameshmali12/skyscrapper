import pygame
from functions import displayimage,displaytext,loadimage,scaleimage,drawrect,playmusic

pygame.init()

# declaring the global variable

width = 850
height = 700
fps = 60

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
            pygame.mixer.music.set_pos(20)
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
            drawrect(display,"blue",buildinginhand["x"],buildinginhand["y"],buildinginhand["width"],height)
        
        for index,data in enumerate(buildingarr):
            displayimage(display,scaleimage(data["name"],data["width"],data["height"]),data["x"],data["y"])
        

        # displaying the block in the hand
        if rotating:
            if buildinginhand["x"]<0:
                buildinginhand.update({"speedx":7})
            if buildinginhand["x"]>(width-buildinginhand["width"]):
                buildinginhand.update({"speedx":-7})
                
            
        # update the position of the building in the hand
        buildinginhand.update({
            "x":buildinginhand["x"]+buildinginhand["speedx"] if rotating else buildinginhand["x"],
            "y":buildinginhand["y"]+buildinginhand["speedy"] if buildinginhand["y"]+buildinginhand["height"]-10<targety else buildinginhand["y"]
        })

        # removing the extra part of the block
        if buildinginhand["y"]+buildinginhand["height"]-10>targety:
            playmusic("assets/poof.mp3")
            score+=1
            decrement = 0
            if buildinginhand["x"]+buildinginhand["width"]<targetx1:
                playmusic("assets/gameover.mp3")
                quit()
            if buildinginhand["x"]<targetx1:
                print("left")
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
                print("right")
                decrement = buildinginhand["x"]+buildinginhand["width"]-targetx2
                inix = buildinginhand["x"]+buildinginhand["width"]-decrement
                print(decrement)
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
            # performdowning = True
        
        if falling["falling"]:
            displayimage(display,scaleimage(falling["name"],falling["sizex"],falling["sizey"]),falling["x"],falling["y"])
            falling.update({
                "y":falling["y"]+8
            })
            if falling["y"]>height:
                performdowning=True
                falling.update({"falling":False})

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
            quit()


        displayimage(display,scaleimage(buildinginhand["name"],buildinginhand["width"],buildinginhand["height"]),buildinginhand["x"],buildinginhand["y"])

        # displaying the score
        displaytext(display,f"Score :- {score}",10,10,30,"black",True,True)
        


        pygame.display.update()
        clock.tick(fps)


gameloop()