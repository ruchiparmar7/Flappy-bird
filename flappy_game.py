import random # for generating random numbers
import sys #we will use sys.exit to exit the program
import pygame 
from pygame.locals import * #basic pygame imports

#global variable for the game

FPS=32 #frames per second
SCREENWIDTH = 289
SCREENHEIGHT = 511

SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY= SCREENHEIGHT*0.8
GAME_SPRITES={}
GAME_SOUNDS={}

PLAYER='gallery/spirits/bird.png'
BACKGROUND='gallery/spirits/background_img.png'
PIPE='gallery/spirits/pipe.png'
#show welcome images in this function
def welcomescreen(): 
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    welcomex = int((SCREENWIDTH - GAME_SPRITES['welcome'].get_width())/2)
    welcomey = int(SCREENHEIGHT *0.13)
    basex=0
    while True:
        for event in pygame.event.get():
            #if user click on cross button close game
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
                
                #if the user presses space or up key,start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
                SCREEN.blit(GAME_SPRITES['welcome'],(welcomex,welcomey))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

                
def maingame():
    score=0
    playerx=int(SCREENWIDTH/5)
    playery=int(SCREENWIDTH/2)
    basex=0
    
    #create 2 pipes for blint the screen
    
    newpipe1=getrandompipe()
    newpipe2=getrandompipe()
    
    #my list of upper pipes
    upperpipes=[{'x':SCREENWIDTH+200,'y':newpipe1[0]['y']},
                {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':newpipe2[0]['y']}
                ]
    #my list of lower pipes
    lowerpipes=[{'x':SCREENWIDTH+200,'y':newpipe1[1]['y']},
                {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':newpipe2[1]['y']}
                ]
    
    pipevelx=-4
    playervely=-9
    playermaxvely=10
    playerminvely=-8
    playeraccy=1
    playerflapaccv=-8 #velocity while flapping
    playerflapped=False #it is true only when the bird is flapped


    while True:
        for event in  pygame.event.get():
             if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
             if event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                if playery>0:
                    playervely=playerflapaccv
                    playerflapped=True
                    GAME_SOUNDS['wing'].play()
                    #this function will return true if the player is crashed
                    
        crashTest=isCollide(playerx,playery,upperpipes,lowerpipes)
        if crashTest:
            return
        #check for score
        playermidpos=playerx+GAME_SPRITES['player'].get_width()/2
        for pipe in upperpipes:
            pipemidpos=pipe['x']+GAME_SPRITES['pipe'][0].get_width()/2
            if pipemidpos<=playermidpos<pipemidpos+4:
                score+=1
                print(f"Your Score is {score}")
                GAME_SOUNDS['point'].play()
            
        if playervely <playermaxvely and not playerflapped:
            playervely+=playeraccy
        if playerflapped:
            playerflapped=False
        playerheight=GAME_SPRITES['player'].get_height()
        playery=playery+min(playervely,GROUNDY -playery-playerheight)
        
        #move pipes to the left
        
        for upperpipe,lowerpipe in zip(upperpipes,lowerpipes):
            upperpipe['x']+=pipevelx
            lowerpipe['x']+=pipevelx
        #adding a new pipe when the first pipe is  about to go left part of the screen
        if 0<upperpipes[0]['x']<5:
            newpipe=getrandompipe()
            upperpipes.append(newpipe[0])
            lowerpipes.append(newpipe[1])
            
            #if the pipe out of the screen remove it
        if upperpipes[0]['x']< -GAME_SPRITES['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)
            
            #let's blit  our sprites now
        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        for upperpipe,lowerpipe in zip(upperpipes,lowerpipes):
           SCREEN.blit(GAME_SPRITES['pipe'][0],(upperpipe['x'],upperpipe['y']))
           SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerpipe['x'],lowerpipe['y']))
           
        SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
        mydigits=[int (x) for x in list(str(score))]
        width=0
        for digit in mydigits:
            width+=GAME_SPRITES['numbers'][digit].get_width()
        xoffset=(SCREENWIDTH-width)/2
        
        for digit in mydigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(xoffset,SCREENHEIGHT*0.12))
            xoffset+=GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
def isCollide(playerx,playery,upperpipes,lowerpipes):
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperpipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True


    for pipe in lowerpipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    

             
    """
    generate positions of two pipes(one top pipe and bottom pipe) for blitting on the screen
    """
def getrandompipe():
    pipeHeight=GAME_SPRITES['pipe'][0].get_height()
    offset= SCREENHEIGHT/3
    y2=offset+random.randrange(0,int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()-1.2*offset))
    pipeX=SCREENWIDTH+10
    y1=pipeHeight-y2+offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upperpipe
        {'x': pipeX, 'y': y2} #lowerpipe
    ]
    return pipe        

if __name__ == "__main__":
    #this will be the mnain function were the game will start
    pygame.init()# intilize  all pygame modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy bird by ruchi parmar')
    GAME_SPRITES['numbers']=(
        pygame.image.load('gallery/spirits/0.png').convert_alpha(),
        pygame.image.load('gallery/spirits/1.png').convert_alpha(),
        pygame.image.load('gallery/spirits/2.png').convert_alpha(),
        pygame.image.load('gallery/spirits/3.png').convert_alpha(),
        pygame.image.load('gallery/spirits/4.png').convert_alpha(),
        pygame.image.load('gallery/spirits/5.png').convert_alpha(),
        pygame.image.load('gallery/spirits/6.png').convert_alpha(),
        pygame.image.load('gallery/spirits/7.png').convert_alpha(),
        pygame.image.load('gallery/spirits/8.png').convert_alpha(),
        pygame.image.load('gallery/spirits/9.png').convert_alpha(),
            )
    
    GAME_SPRITES['base']=pygame.image.load('gallery/spirits/base.png').convert_alpha()
    GAME_SPRITES['welcome']=pygame.image.load('gallery/spirits/welcome.png').convert_alpha()
    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180), 
    pygame.image.load(PIPE).convert_alpha()
    )
   
    #game sounds
    
    GAME_SOUNDS['die']=pygame.mixer.Sound('gallery/audio/sfx_die.wav')
    GAME_SOUNDS['hit']=pygame.mixer.Sound('gallery/audio/sfx_hit.wav')
    GAME_SOUNDS['swoosh']=pygame.mixer.Sound('gallery/audio/sfx_swooshing.wav')
    GAME_SOUNDS['point']=pygame.mixer.Sound('gallery/audio/sfx_point.wav')
    GAME_SOUNDS['wing']=pygame.mixer.Sound('gallery/audio/sfx_wing.wav')
    
    GAME_SPRITES['background']=pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player']=pygame.image.load(PLAYER).convert_alpha()
    
    while True:
        welcomescreen()  #show welcome screen until user presses the button
        maingame()    #this is the main function