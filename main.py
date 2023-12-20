import pygame,sys,random
from pygame.locals import *

pygame.init()

#Open Pygame window 
screen = pygame.display.set_mode((640, 480),) #add RESIZABLE or FULLSCREEN
#Title
pygame.display.set_caption("dark tetris")
color=pygame.color.THECOLORS["black"]

pygame.draw.rect(screen, (0,0,255), [220, 40, 200, 400], 2)
font=pygame.font.SysFont('Arial', 30)

score=0
lines=0
pause=0
level=1
hi_score=(200*level)+score
shadow=1
hard_drop=0
game_over=0
congratulation=0
display_type=0
result=0
time=0
time_limit=30-(level*5)
double_time_limit=time_limit*2
start_pos=[280,-40]

following_pos=[280,-40]

piece=[]
next_piece=[]
piece_pos=[]
next_piece_pos=[]
shadow_pos=[]

table=[]

pieces_list=[ [[0,0,0,0, 0,0,0,0, 0,1,0,0, 1,1,1,0],[0,0,0,0, 1,0,0,0, 1,1,0,0, 1,0,0,0],
               [0,0,0,0, 0,0,0,0, 1,1,1,0, 0,1,0,0],[0,0,0,0, 0,1,0,0, 1,1,0,0, 0,1,0,0]],
              [[0,0,0,0, 1,0,0,0, 1,0,0,0, 1,1,0,0],[0,0,0,0, 0,0,0,0, 1,1,1,0, 1,0,0,0],
               [0,0,0,0, 1,1,0,0, 0,1,0,0, 0,1,0,0],[0,0,0,0, 0,0,0,0, 0,0,1,0, 1,1,1,0]],
              [[0,0,0,0, 0,1,0,0, 0,1,0,0, 1,1,0,0],[0,0,0,0, 0,0,0,0, 1,0,0,0, 1,1,1,0],
               [0,0,0,0, 1,1,0,0, 1,0,0,0, 1,0,0,0],[0,0,0,0, 0,0,0,0, 1,1,1,0, 0,0,1,0]],
              [[0,0,0,0, 0,1,0,0, 1,1,0,0, 1,0,0,0],[0,0,0,0, 0,0,0,0, 1,1,0,0, 0,1,1,0]],
              [[0,0,0,0, 1,0,0,0, 1,1,0,0, 0,1,0,0],[0,0,0,0, 0,0,0,0, 0,1,1,0, 1,1,0,0]],              
              [[0,0,0,0, 0,0,0,0, 0,0,0,0, 1,1,1,1],[1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0]],
              [[0,0,0,0, 0,0,0,0, 1,1,0,0, 1,1,0,0]] ]

selected_piece=pieces_list[random.randint(0,len(pieces_list)-1)]
piece=selected_piece[0]

next_piece=pieces_list[random.randint(0,len(pieces_list)-1)]

selected_piece_index=0
record_selected_piece_index=selected_piece_index

def init_piece(piece,piece_pos,start_pos):
    x=start_pos[0]
    y=start_pos[1]
    for i in piece:
        if i==1:piece_pos.append([x,y])
        x+=20
        if x==start_pos[0]+(20*4):x=start_pos[0];y+=20
        
init_piece(piece,piece_pos,start_pos)
init_piece(piece,shadow_pos,following_pos)
init_piece(next_piece[0],next_piece_pos,[460,80])             

def draw_screen():
    screen.fill(color)
    pygame.draw.rect(screen, (0,0,255), [220, 40, 200, 400], 2)
    for i in piece_pos:
        if i[1]>=40:
           pygame.draw.rect(screen, (0,255,0), [i[0],i[1], 20, 20],2)
           pygame.draw.rect(screen, (0,255,0), [i[0]+6,i[1]+6, 15, 15])
           
    for i in next_piece_pos:
        pygame.draw.rect(screen, (0,255,0), [i[0],i[1], 20, 20],2)
        pygame.draw.rect(screen, (0,255,0), [i[0]+6,i[1]+6, 15, 15])
        
    for i in table:
        if i[1]>=40:
           pygame.draw.rect(screen, (255,0,0), [i[0],i[1], 20, 20],2)
           pygame.draw.rect(screen, (255,0,0), [i[0]+6,i[1]+6, 15, 15])
    if shadow:
       for i in shadow_pos:
           if i[1]>=40:
              pygame.draw.rect(screen, (0,255,0), [i[0],i[1], 20, 20],2)

    text=font.render(("score: "+str(score)), True, (250,250,250));screen.blit(text,(460,320))
    text=font.render(("level: "+str(level)), True, (250,250,250));screen.blit(text,(460,280))
    text=font.render(("lines: "+str(lines)), True, (250,250,250));screen.blit(text,(460,360))
    text=font.render(("next level:"+str(hi_score)), True, (250,250,250));screen.blit(text,(430,40))
    
    if game_over:
       text=font.render(("game over "), True, (250,250,250));screen.blit(text,(250,200))
    if congratulation:
       text=font.render(("congratulation "), True, (250,250,250));screen.blit(text,(228,200))

    pygame.display.flip()

def at_limit(piece_pos,table,axe,axe2,limit,move):
    its_limit=0
    for i in range(len(piece_pos)):
        if piece_pos[i][axe]+move==limit:its_limit=1
        for j in range(len(table)):
            if move==20 and axe==0:
               if piece_pos[i][axe]+move==table[j][axe] and piece_pos[i][axe2]==table[j][axe2]:its_limit=1
            elif move==0 and axe==0:
               if piece_pos[i][axe]+move==table[j][axe]+20 and piece_pos[i][axe2]==table[j][axe2]:its_limit=1
            elif move==20 and axe==1:
               if piece_pos[i][axe]==table[j][axe] and piece_pos[i][axe2]==table[j][axe2]:its_limit=1
    return its_limit


def bounce(piece_pos,axe,move):
     for i in range(len(piece_pos)):
         piece_pos[i][axe]+=move

         
def cast_shadow(shadow_pos):
    limit=0
    if len(shadow_pos)>0:
       while not limit:
             for i in range(len(shadow_pos)):
                 shadow_pos[i][1]+=20
             if at_limit(shadow_pos,table,1,0,460,20):
                bounce(shadow_pos,1,-20)
                limit=1
             
cast_shadow(shadow_pos)
         
def intersect(piece_pos,table):
    intersecting=0
    for i in piece_pos:
        if i[0]>=420:intersecting=1
        for j in table:
            if i==j:intersecting=1
    return intersecting
        
def valide_piece(piece):
    valide=0
    for i in piece:
        if i==1:valide=1
    return valide
    
def lose(table,limit_pos):
    its_lose=0
    for i in table:
        if i[1]<=limit_pos[1]:its_lose=1
    return its_lose

def break_line(table):
    x=220
    y=40#+(20*4)
    segement=0
    line=[]
    broken_line=0
    for i in range(20):  #(400-(4*20))/20=16
        x=220;y+=20;segement=0;line=[]
        for j in range(10):
            for square in table:
                if square==[x,y]:
                   segement+=1;line.append(square)
            x+=20
        if segement==10:
           broken_line+=1
           for square in line:table.remove(square)
           for j in range(len(table)):
               if table[j][1]<y:table[j][1]+=20
    return  broken_line

def fill_table(table):
    x=220;y=40+(20*4)
    for i in range(16):
        x=220
        for j in range(9):
            table.append([x,y])
            x+=20
        y+=20
    

pygame.key.set_repeat(400, 30)

while True:
    
    #loop speed limitation
    #30 frames per second is enought
    pygame.time.Clock().tick(30)
    
    for event in pygame.event.get():    #wait for events
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
                       
        if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
           if game_over or congratulation:
              table=[];score=0;lines=0
              following_pos=[280,-40]
              selected_piece=pieces_list[random.randint(0,len(pieces_list)-1)]
              piece=selected_piece[0];piece_pos=[];init_piece(piece,piece_pos,start_pos)
              next_piece=pieces_list[random.randint(0,len(pieces_list)-1)]
              next_piece_pos=[];init_piece(next_piece[0],next_piece_pos,[460,80])
              shadow_pos=[];init_piece(piece,shadow_pos,following_pos);cast_shadow(shadow_pos)
              game_over=0;hard_drop=0
              congratulation=0
              level=1;hi_score=(200*level)+score
              time_limit=30-(level*5);double_time_limit=time_limit*2
              
        if event.type == KEYUP:
           if event.key == K_SPACE:
              time_limit=time_limit/2
              
        if event.type == KEYDOWN:
           if event.key == K_c:
              if level<5:
                 level+=1
              time_limit=30-(level*5)
              double_time_limit=time_limit*2
              hi_score=(200*level)+score
              
           elif event.key == K_v:
              if level>1:
                 level-=1
              time_limit=30-(level*5)
              double_time_limit=time_limit*2
              hi_score=(200*level)+score
              
           elif event.key == K_s:
              if shadow:shadow=0
              elif not shadow:shadow=1
              
           elif event.key == K_p:
              text=font.render(("pause "), True, (250,250,250))
              screen.blit(text,(280,200))
              pygame.display.flip()
              pause=1
              if pause:
                 while pause:
                       pygame.time.Clock().tick(30)
                       for event in pygame.event.get():
                           if event.type == QUIT:
                              pygame.quit()
                              sys.exit()
                           if event.type == KEYDOWN and event.key == K_p:
                              pause=0

           elif event.type == KEYDOWN and event.key == K_f:
              if display_type==0:display_type=FULLSCREEN
              elif display_type==FULLSCREEN:display_type=0
              screen = pygame.display.set_mode((640,480),display_type)

                        
        if event.type == KEYDOWN and event.key == K_RIGHT or event.type == MOUSEBUTTONDOWN and event.button==5:
              if not at_limit(piece_pos,table,0,1,420,20):
                 for i in range(len(piece_pos)):piece_pos[i][0]+=20
                 following_pos[0]+=20
              if shadow:
                 shadow_pos=[]
                 init_piece(piece,shadow_pos,following_pos)
                 cast_shadow(shadow_pos)
    
        if event.type == KEYDOWN and event.key == K_LEFT or event.type == MOUSEBUTTONDOWN and event.button==4:         
              if not at_limit(piece_pos,table,0,1,220,0):
                 for i in range(len(piece_pos)):piece_pos[i][0]-=20
                 following_pos[0]-=20
              if shadow:
                 shadow_pos=[]
                 init_piece(piece,shadow_pos,following_pos)
                 cast_shadow(shadow_pos)

        if event.type == KEYDOWN and event.key == K_DOWN:         
              if not at_limit(piece_pos,table,1,0,460,20):
                 time=0
                 for i in range(len(piece_pos)):piece_pos[i][1]+=20
                 following_pos[1]+=20
                 
        if event.type == MOUSEBUTTONDOWN and event.button==1:hard_drop=1
        elif event.type == MOUSEBUTTONUP and event.button==1:hard_drop=0

        if event.type == KEYDOWN and event.key == K_SPACE:
              time_limit=double_time_limit
              
        if event.type == KEYDOWN and event.key == K_UP or event.type == MOUSEBUTTONDOWN and event.button==3:     
              record_selected_piece_index=selected_piece_index
              if selected_piece_index<len(selected_piece):
                 selected_piece_index+=1
              if selected_piece_index==len(selected_piece):selected_piece_index=0
              piece=selected_piece[selected_piece_index];piece_pos=[]
              init_piece(piece,piece_pos,following_pos)
              if intersect(piece_pos,table):
                 selected_piece_index=record_selected_piece_index
                 piece=selected_piece[selected_piece_index];piece_pos=[]
                 init_piece(piece,piece_pos,following_pos)
              if shadow:
                 shadow_pos=[]
                 init_piece(piece,shadow_pos,following_pos)
                 cast_shadow(shadow_pos)
           
    if valide_piece(piece):
        
       if hard_drop:
          if not at_limit(piece_pos,table,1,0,460,20):
             time=0
             for i in range(len(piece_pos)):piece_pos[i][1]+=20
             following_pos[1]+=20
              
       if not at_limit(piece_pos,table,1,0,460,20):
          time+=1
          if time>=time_limit:
             for i in range(len(piece_pos)):piece_pos[i][1]+=20
             following_pos[1]+=20
             time=0
       
       if at_limit(piece_pos,table,1,0,460,20):
          bounce(piece_pos,1,-20)
          for i in piece_pos:table.append(i)
          result=break_line(table)
          lines+=result
          score+=result*10*level
          following_pos=[280,-40]
          selected_piece=[[0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]]
          piece=selected_piece[0]
          shadow_pos=[]
          hard_drop=0
          if score>=hi_score:
             if level!=5:
                level+=1;hi_score=(200*level)+score
                time_limit=30-(level*5);double_time_limit=time_limit*2
             else:congratulation=1
          
       if not lose(table,[220,40]) and not congratulation:
          if not valide_piece(piece):
              selected_piece=next_piece
              piece=selected_piece[0]
              next_piece=pieces_list[random.randint(0,len(pieces_list)-1)]
              next_piece_pos=[];init_piece(next_piece[0],next_piece_pos,[460,80])
              piece_pos=[];init_piece(piece,piece_pos,start_pos)
              selected_piece_index=0
              record_selected_piece_index=selected_piece_index
              if shadow:
                 shadow_pos=[]
                 init_piece(piece,shadow_pos,following_pos)
                 cast_shadow(shadow_pos)
       elif lose(table,[220,40]):game_over=1


    draw_screen()
