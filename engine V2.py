import numpy as np
import pygame
import pyglet
import math



class Game():
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((1366,768))
        self.background = pygame.image.load('background.jpg').convert()
        self.background = pygame.transform.smoothscale(self.background, self.window.get_size())

        pygame.display.set_caption("No.of Collisions Simulator")
        
        self.clock = pygame.time.Clock()
        self.fps = 100
        self.timestep = 0
        self.running = True
        self.n_collisions = 0
        self.collision = 0
        self.sound = pyglet.resource.media("clack.wav", streaming=False)
        self.font = pygame.font.Font("Minecraft.ttf",20)
        pygame.key.start_text_input()

        self.v1 = 0
        self.v2 = -100
        self.m1 = 1
        self.m2 = 100
        self.y = 575
        self.size1 = 50
        self.size2 = 50 + (math.log(self.m2,10) * 70)
        self.pos1 = np.array([225,self.y])
        self.pos2 = np.array([370,self.y])
        self.Str_Mass = str(self.m2)
       
    def cal_pos(self,timestep):
        self.delta_pos1 = np.array([self.v1*timestep,0])
        self.delta_pos2 = np.array([self.v2*timestep,0])
        self.pos1 = self.delta_pos1 + self.pos1
        self.pos2 = self.delta_pos2 + self.pos2

    def cal_vel(self):
        m1 = self.m1 
        m2 = self.m2 
        v1 = self.v1 
        v2 = self.v2 
        a=2* m1* v1
        b=(m2 - m1) * v2
        c=m1 + m2
        self.v2 = (a + b) / c
        self.v1 = self.v2 + v2 - v1

    def cycle_sim(self):
        if self.pos2[0] > 900:
            self.restart() 
    def update(self):
        if self.pos1[0]+50 >= self.pos2[0]:
            self.cal_vel()
            if self.timestep < 0:
                self.n_collisions = self.n_collisions-1
            else:
                self.n_collisions = self.n_collisions+1

        if 112 >= self.pos1[0]:
            self.v1 = -self.v1
            if self.timestep < 0:
                self.n_collisions = self.n_collisions-1
            else:
                self.n_collisions = self.n_collisions+1

        self.cal_pos(self.timestep)

    def restart(self):
        self.n_collisions = 0
        self.collision = 0
        self.v1 = 0
        self.v2 = -100
        self.m1 = 1
        self.y = 575
        self.size1 = 50
        self.size2 = 50 + (math.log(self.m2,10) * 70)
        self.pos1 = np.array([225,self.y])
        self.pos2 = np.array([370,self.y])     
        self.timestep = 1/2000    

    def UI_Render(self):
        #text for mass
        Text_Mass = 'Mass = ' 
        Text_Mass = str(Text_Mass + self.Str_Mass)
        self.Text_Mass = self.font.render(Text_Mass, False, (250,250,250))
        self.rect = self.Text_Mass.get_rect()
        pygame.draw.rect(self.Text_Mass, (30,30,30), self.rect, 1)
        self.window.blit(self.Text_Mass, (1190, 100))

        #text for collisions
        self.Str_Collisions = str(self.n_collisions)
        Text_Collisions = 'Collsions = '
        Text_Collisions = str(Text_Collisions + self.Str_Collisions)
        self.Text_Collisions = self.font.render(str(Text_Collisions), False, (250,250,250))
        self.window.blit(self.Text_Collisions, (1190, 70))
        
        #title text
        self.Text_Title = self.font.render('Py Collision Simulator', False, (250,250,250))
        rect1 = self.Text_Title.get_rect()
        pygame.draw.rect(self.Text_Mass, (30,30,30), self.rect, 1)
        pos_x = 683 - (rect1.width/2)
        self.window.blit(self.Text_Title, (pos_x, 70))

        #ui for change mass
        pos = (1190+self.rect.topright[0],100+self.rect.topright[1])
        point = pygame.mouse.get_pos()
        if point[0]>1185 and point[0]<(1195+self.rect.width) and point [1]>95 and point[1]<(105+self.rect.height):
            cursor = pygame.Rect(pos, (7, self.rect.height))
            pygame.draw.rect(self.window, (250,250,250), cursor)
            self.cursor_touch = True
        else:
            self.cursor_touch = False
            
    def render(self):
        self.window.blit(self.background, (0, 0))
        if self.slide ==1:
            self.window.blit('1.png', (0, 0))
        #objects
        pygame.draw.rect(self.window,(39, 40, 34),pygame.Rect(self.pos1[0],self.y,self.size1,self.size1))
        pygame.draw.rect(self.window,(93, 102, 179),pygame.Rect(self.pos2[0],625-self.size2,self.size2,self.size2))
        pygame.draw.rect(self.window,(200, 200, 200),pygame.Rect(105,110,7,522),0,10)
        pygame.draw.rect(self.window,(200, 200, 200),pygame.Rect(105,625,1154,7),0,10)
        #UI
        self.UI_Render()
        #update display
        pygame.display.update()    

    def run(self):
        
        while self.running:
            for i in range(10):
                self.update()
            self.cycle_sim()
            #self.render()        
            self.clock.tick(self.fps)
            if self.n_collisions != self.collision:
                self.sound.play()
                self.collision = self.n_collisions

            #input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    break
                elif event.type == pygame.KEYDOWN:
                    #timestep controls
                    if event.key == pygame.K_LEFT:
                        if self.timestep < 0:
                            self.timestep = 0
                        else:
                                self.timestep = 1/2000
                    elif event.key == pygame.K_RIGHT:
                        if self.timestep > 0:
                            self.timestep = 0
                        else:
                            self.timestep = -1/2000
                    elif event.key == pygame.K_RSHIFT:
                        self.timestep = -1/200
                    elif event.key == pygame.K_LSHIFT:
                        self.timestep = 1/200
                    #mass selection
                    elif self.cursor_touch == True:
                        if event.key == pygame.K_BACKSPACE:
                            if len(self.Str_Mass)>0:
                                self.Str_Mass = self.Str_Mass[:-1]
                        elif event.key == pygame.K_RETURN:
                            if self.Str_Mass != str(self.m2):
                                self.m2 = int(self.Str_Mass)
                                self.restart()
                        elif event.key != pygame.K_BACKSPACE or pygame.K_RETURN:
                            self.Str_Mass += event.unicode
                


game = Game()
game.run()