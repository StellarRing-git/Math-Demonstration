import numpy as np
import pygame
import pyglet



class Game():
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((900,600))
        pygame.display.set_caption("No.of Collisions Simulator")
        
        self.clock = pygame.time.Clock()
        self.fps = 100
        self.timestep = 0
        self.running = True
        self.n_collisions = 0
        self.collision = 0
        self.sound = pyglet.resource.media("clack_sound.mp3", streaming=False)
        self.font = pygame.font.Font("Minecraft.ttf",20)
        pygame.key.start_text_input()

        self.v1 = 0
        self.v2 = -100
        self.m1 = 1
        self.m2 = 100
        self.y = 300
        self.pos1 = np.array([300,self.y])
        self.pos2 = np.array([400,self.y])
        self.UI()
       
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

    def update(self):
        if self.pos1[0]+50 >= self.pos2[0]:
            self.cal_vel()
            if self.timestep < 0:
                self.n_collisions = self.n_collisions-1
            else:
                self.n_collisions = self.n_collisions+1

        if 205 >= self.pos1[0]:
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
        self.y = 300
        self.pos1 = np.array([300,self.y])
        self.pos2 = np.array([400,self.y])         

    def UI(self):
        #ui for mass count
        self.Str_Mass = str(self.m2)
        
        

    def UI_Render(self):
        #text for mass
        Text_Mass = 'Mass = ' 
        Text_Mass = str(Text_Mass + self.Str_Mass)
        self.Text_Mass = self.font.render(Text_Mass, True, (250,250,250))
        self.rect = self.Text_Mass.get_rect()
        pygame.draw.rect(self.Text_Mass, (30,30,30), self.rect, 1)
        self.window.blit(self.Text_Mass, (700, 100))

        #text for collisions
        self.Str_Collisions = str(self.n_collisions)
        Text_Collisions = 'Collsions = '
        Text_Collisions = str(Text_Collisions + self.Str_Collisions)
        self.Text_Collisions = self.font.render(str(Text_Collisions), True, (250,250,250))
        self.window.blit(self.Text_Collisions, (700, 20))
        
        #ui for change mass
        pos = (700+self.rect.topright[0],100+self.rect.topright[1])
        point = pygame.mouse.get_pos()
        if point[0]>690 and point[0]<(710+self.rect.width) and point [1]>90 and point[1]<(110+self.rect.height):
            cursor = pygame.Rect(pos, (7, self.rect.height))
            pygame.draw.rect(self.window, (250,250,250), cursor)
            self.cursor_touch = True
        else:
            self.cursor_touch = False
            
    def render(self):
        self.window.fill((40,40,40))
        #objects
        pygame.draw.rect(self.window,(241, 76, 76),pygame.Rect(self.pos1[0],300,50,50))
        pygame.draw.rect(self.window,(93, 102, 179),pygame.Rect(self.pos2[0],300,50,50))
        pygame.draw.rect(self.window,(161, 216, 187),pygame.Rect(200,100,5,250))
        pygame.draw.rect(self.window,(161, 216, 187),pygame.Rect(200,350,800,5))
        #UI
        self.UI_Render()
        #update display
        pygame.display.update()    

    def run(self):
        
        while self.running:
            for i in range(10):
                self.update()
            self.render()        
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
                    if event.key == pygame.K_RIGHT:
                        if self.timestep < 0:
                            self.timestep = 0
                        else:
                                self.timestep = 1/2000
                    elif event.key == pygame.K_LEFT:
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