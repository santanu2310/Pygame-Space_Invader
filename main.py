#from cgitb import reset
import pygame
import random
import sys
from pygame import mixer
from pygame import*
import pickle

FPS=120
FPSCLOCK = pygame.time.Clock()
high_score=0
#level_up=True
enimy_speed=2
score_value=0
num_of_enimys_to_load= 10
num_of_enimys=3
# exitgame=False

def manue():    
    #initialze pygame
    pygame.init()

    global high_score

    #create the screen
    screen= pygame.display.set_mode((800,600))
    background = pygame.image.load("data/Sprites/background.png")

    #title and icon
    pygame.display.set_caption("Space Invaders.......🛸🛸")
    icon = pygame.image.load('data/Sprites/ufo.png')
    pygame.display.set_icon(icon)

    #player
    playerimg = pygame.image.load('data/Sprites/player.png')
    playerX=370
    playerY=480

    color = (255,255,255)
  
    # dark shade of the button
    color_dark = (255,136,44)
       
    data=open('data/score','rb')
    high_score=pickle.load(data)
    font = pygame.font.Font('freesansbold.ttf',32)
    font2 = pygame.font.Font('freesansbold.ttf',24)
    data.close()
    text = font.render('START' , True , color)
    text1 = font.render('HELP' , True , color)
    text2= font.render('EXIT' , True , color)
    text3= font2.render('MENUE' , True , (255, 200, 1))
    textX=275
    texty=240

    def show(x,y):
        score=font.render("HIGH SCORE:"+str(high_score) , True , (255,255,255))
        screen.blit(score ,(x,y))
    
    def help():
       pygame.init()
       screen= pygame.display.set_mode((800,600))
       background = pygame.image.load("data/Sprites/help.jpg")
       button=pygame.image.load("data/Sprites/back.png")
       screen.blit(background,(0,0))
       screen.blit(button,(10,5))
       while True:      
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type ==KEYDOWN and (event.key==K_SPACE):
                # print("True")
                return
            if event.type==pygame.MOUSEBUTTONDOWN:
                mouse=pygame.mouse.get_pos()
                # print(mouse[1])
                if 10<=mouse[0]<=42 and 5<=mouse[1]<=37:
                    # print("True")
                    return
        FPSCLOCK.tick(FPS)
        pygame.display.update()        

    while True:        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type ==KEYDOWN and (event.key==K_SPACE):
                return
            if event.type==pygame.MOUSEBUTTONDOWN:
                # print(mouse[1])
                if 330<=mouse[0]<=470 and 400<=mouse[1]<=440:
                    return
                elif 330<= mouse[0] <= 470 and 480 <= mouse[1] <=520:
                    pygame.quit()
                    sys.exit()
                elif 330<= mouse[0] <= 470 and 440 <= mouse[1] <=480:
                    help()
            else:
                mouse=pygame.mouse.get_pos()
                #print(mouse[0])
                screen.blit(background,(0,0))
                if 330<= mouse[0] <= 470 and 400 <= mouse[1] <=440:
                    pygame.draw.rect(screen,color_dark,[275,400,250,40])
                elif 330<= mouse[0] <= 470 and 440 <= mouse[1] <=480:
                    pygame.draw.rect(screen,color_dark,[275,440,250,40])
                elif 330<= mouse[0] <= 470 and 480 <= mouse[1] <=520:
                    pygame.draw.rect(screen,color_dark,[275,480,250,40],0,0,0,0,11,11) #surface, color, rect, width=0, border_radius=0, border_top_left_radius=-1, border_top_right_radius=-1, border_bottom_left_radius=-1, border_bottom_right_radius=-1
                
            pygame.draw.rect(screen,color_dark,[275,400,250,120],2,0,0,0,11,11)
            pygame.draw.rect(screen,color_dark,[275,372,250,30],2,0,11,11,0,0)
            screen.blit(text ,(350,406))
            screen.blit(text1 ,(358,446))
            screen.blit(text2 ,(358,486))
            screen.blit(text3 ,(358,377))
            FPSCLOCK.tick(FPS)
            show(textX,texty)
            pygame.display.update()
               
def gameover():
    global level_up
    global score_value
    global num_of_enimys
    global exitgame
    # print(exitgame)
    if exitgame:
        return

    screen= pygame.display.set_mode((800,600))
    over_font=pygame.font.Font('freesansbold.ttf',64)
    background = pygame.image.load("data/Sprites/background.jpg")
    def game_over_text():
        over_text=over_font.render('GAME OVER',True,(255,255,255))
        screen.blit(over_text,(200,250))
    for i in range(0,150):
        if i==150:
            return
        else:
            level_up=False
            score_value=0
            num_of_enimys= 3
            screen.blit(background,(0,0))
            FPSCLOCK.tick(70)
            game_over_text()
            pygame.display.update()
#                                                                             -------- main game function
def main_game():
    import math
    import time
    #initialze pygame
    global high_score
    global level_up
    global enimy_speed
    global score_value
    global num_of_enimys
    global exitgame
    pose=False
    level_up=True
    frame_delay_exp=0
    exp_frame=-1
    explotion=False
    start_animation=False
    
    pygame.init()
    pausebtn=pygame.image.load("data/Sprites/pause.png")

    #create the screen
    screen= pygame.display.set_mode((800,600))
    background = pygame.image.load("data/Sprites/background.jpg")

    #title and icon
    pygame.display.set_caption("Space Invaders")
    icon = pygame.image.load('data/Sprites/ufo.png')
    pygame.display.set_icon(icon)

    #player
    playerimg = pygame.image.load('data/Sprites/player.png')
    playerX=370
    playerY=480
    playerX_change=0

    #explotion
    images_exp=[]
    for i in range(1,6):
        img = pygame.image.load(f"data/Sprites/images/img{i}.png")
        img = pygame.transform.scale(img, (100, 100))
        images_exp.append(img)

    #Enimy
    enimyimg =[]
    enimyX=[]
    enimyY=[]
    enimy_collision=[]
    enimyX_change=[]
    enimyY_change=[]
    error_frame=[]
    
    for i in range(num_of_enimys_to_load):
        enimyimg.append(pygame.image.load('data/Sprites/enimy.png'))
        enimyX.append(random.randint(0,800))
        enimyY.append(30)
        enimyX_change.append(enimy_speed)
        enimyY_change.append(30)
        enimy_collision.append(1)
        error_frame.append(1)

    #bullet
    bulletimg=pygame.image.load('data/Sprites/bullet.png')
    bulletX=0
    bulletY=480
    bulletX_change=0
    bulletY_change=5
    bullet_state="ready"

    #Score
    font = pygame.font.Font('freesansbold.ttf',32)

    textX=10
    texty=10

    #background sound
    mixer.music.load("data/Sounds/background.wav")
    mixer.music.play(-1)             #-1 will run the music in loop

    #game over
    def show(x,y):
        score=font.render("score :"+str(score_value) , True , (255,255,255))
        screen.blit(score ,(x,y))
        
    def player(x,y):
        screen.blit(playerimg,(x,y))

    def enimy(x,y,i):
        screen.blit(enimyimg[i],(x,y))

    def fire(x,y):
        global bullet_state       
        screen.blit(bulletimg,(x+16,y+10))
               
    #colition
    def iscollition(enimyX,enimyY,bulletX,bulletY):
        
        distance=math.sqrt(math.pow(enimyX-bulletX,2) + (math.sqrt(math.pow(enimyY-bulletY,2))))
        if distance < 7:
            return True
    
    level_up_font=pygame.font.Font('freesansbold.ttf',64)

    def level_up_text():
        up_text=level_up_font.render('LEVEL UP',True,(255,255,255))
        screen.blit(up_text,(200,250))
    
    #  pause function
    def pause():
        global exitgame
        color_dark = (255,136,44)
        pygame.init()
        screen= pygame.display.set_mode((800,600))
        font = pygame.font.Font('freesansbold.ttf',32)
        text = font.render('RESUME' , True , (255,255,255))
        text1=font.render('EXIT',True,(255,255,255))
        background = pygame.image.load("data\Sprites/background.jpg")
        screen.blit(background,(0,0))
        while True:
            mouse=pygame.mouse.get_pos() 
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type ==KEYDOWN and (event.key==K_SPACE):
                    #print("True")
                    return
                if event.type==pygame.MOUSEBUTTONDOWN:
                    # mouse=pygame.mouse.get_pos()
                    # print(mouse[1])
                    if 300<=mouse[0]<=500 and 250<=mouse[1]<=300:
                        return
                    if 300<=mouse[0]<=500 and 320<=mouse[1]<=370:
                        exitgame=True
                        return exitgame
                else:
                    screen.blit(background,(0,0))                   
                    if 300<=mouse[0]<=500 and 250<=mouse[1]<=300:
                        pygame.draw.rect(screen,color_dark,[300,250,200,50],0,11)
                    if 300<=mouse[0]<=500 and 320<=mouse[1]<=370:
                        pygame.draw.rect(screen,color_dark,[300,320,200,50],0,11)
            
                # print(mouse)
                pygame.draw.rect(screen,(255,255,255),[300,250,200,50],2,11)
                pygame.draw.rect(screen,(255,255,255),[300,320,200,50],2,11)
                screen.blit(text,(330,260))
                screen.blit(text1,(360,330))
                FPSCLOCK.tick(FPS)
                pygame.display.update()

    #game loop
    running = True
    while running:
        screen.fill((0,0,0))
        screen.blit(background,(0,0))
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
        
            # if ky is pressed check whether it is right or light
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    playerX_change =-4

                if event.key==pygame.K_RIGHT:
                    playerX_change=4
                
                if event.key==pygame.K_SPACE:
                    if bullet_state == "ready":
                        bullet_state="fire"
                        bulletsound=mixer.Sound('data/Sounds\laser.wav')
                        bulletsound.play()
                        bulletX=playerX
                        fire(bulletX,playerY)

            if event.type==pygame.KEYUP:
                if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                    playerX_change=0
            
            if event.type==pygame.MOUSEBUTTONDOWN:
                mouse=pygame.mouse.get_pos()
                if 384<=mouse[0]<=416 and 5<=mouse[1]<=37:
                    pygame.mixer.music.pause()
                    exitgame=pause()
                    pygame.mixer.music.unpause()
                    if exitgame:
                        pygame.mixer.music.pause()
                        return
        
        playerX += playerX_change

        if playerX<=0:
            playerX=0
        elif playerX>=736:
            playerX=736

        for i in range(num_of_enimys):            
            collision = iscollition(enimyX[i],enimyY[i],bulletX,bulletY)

            #----------bullet collision----------
            if collision:
                collisionsound=mixer.Sound('data/Sounds\explosion.wav')
                collisionsound.play()
                bulletY=480
                bullet_state="ready"
                score_value+=1
                expX=enimyX[i]
                expY=enimyY[i]
                start_animation=True
                enimyX[i]=random.randint(0,800)
                enimyY[i]=random.randint(0,50)
                #enimyX_change[i]=enimyX_change*-1
            enimyX[i]+= enimyX_change[i]

            #------------------colition with wall-------------------
            error_frame[i]+=1
            enimy_collision[i]=1
            if error_frame[i]<15:
                enimy_collision[i]=0
            if error_frame[i]==15:
                error_frame[i]=1
            if enimyX[i]<0 and enimy_collision[i]==1:
                enimyX_change[i]=enimy_speed
                enimyY[i]+=enimyY_change[i]
            elif enimyX[i]>736 and enimy_collision[i]==1:
                enimyX_change[i]=-enimy_speed
                enimyY[i]+=enimyY_change[i]
            
            #game over
            if enimyY[i]>430:
                if score_value>high_score:
                    high_score=score_value
                # for j in range(num_of_enimys):
                #     enimyY[j]=2000
                enimy_speed=2
                data=open('data/score','wb')
                pickle.dump(high_score,data)
                data.close()
                exitgame=False
                pygame.mixer.music.pause()
                return exitgame
            
            enimy(enimyX[i],enimyY[i],i)
        
        #bulet
        if bulletY<=0:
            bulletY=480
            bullet_state="ready"
        if bullet_state=="fire":
            fire(bulletX,bulletY)
            bulletY-=bulletY_change
        
        #explition animation
        if start_animation:
            frame_delay_exp+=1
            try:
                if frame_delay_exp%12==0:
                    exp_frame+=1
                    explotion=True
                    exp_img=images_exp[exp_frame]
            except:
                exp_frame=0
                frame_delay_exp=0
                explotion=False
                start_animation=False

        if explotion:
            screen.blit(exp_img,(expX,expY))
        
        #level up                                                            ---------
        if score_value==10:
            num_of_enimys=5
            enimy_speed=2
            if level_up:
                level_up_text()
                pose=True
                level_up=False

        if score_value==11:
            level_up=True
        if score_value==20 and level_up:
            level_up=True
            num_of_enimys=7
            enimy_speed=3
            level_up_text()
            pose=True
            level_up=False

        if score_value==21:
            level_up=True
        if score_value==30 and level_up:
            level_up=True
            num_of_enimys=10
            enimy_speed=4
            pose=False
            level_up_text()
            pose=True
            level_up=False
            
        show(textX,texty)
        screen.blit(pausebtn,(384,5))
        player(playerX,playerY)
        FPSCLOCK.tick(FPS)
        pygame.display.update()
        if pose:
            time.sleep(1)
            pose=False
        
print("ENJOY THE GAME 😀")

while True:
    manue()
    main_game()
    gameover()