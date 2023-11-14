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

        self.v1 = 0
        self.v2 = -100
        self.m1 = 1
        self.m2 = 1000000
        self.y = 300
        self.pos1 = np.array([300,self.y])
        self.pos2 = np.array([400,self.y])
       
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
            self.n_collisions = self.n_collisions+1
            print(self.n_collisions)

        if 205 >= self.pos1[0]:
            self.v1 = -self.v1
            self.n_collisions = self.n_collisions+1
            print(self.n_collisions)

        self.cal_pos(self.timestep)
        
    def render(self):
        self.window.fill((40,40,40))
        pygame.draw.rect(self.window,(241, 76, 76),pygame.Rect(self.pos1[0],300,50,50))
        pygame.draw.rect(self.window,(93, 102, 179),pygame.Rect(self.pos2[0],300,50,50))
        pygame.draw.rect(self.window,(161, 216, 187),pygame.Rect(200,100,5,250))
        pygame.draw.rect(self.window,(161, 216, 187),pygame.Rect(200,350,800,5))
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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.timestep = 1/2000
                    elif event.key == pygame.K_LEFT:
                        self.timestep = -1/2000
                    elif event.key == pygame.K_RSHIFT:
                        self.timestep = -1/700
                        print('speed)')
                    elif event.key == pygame.K_LSHIFT:
                        self.timestep = 1/700
                        print('speed)')
                else:
                    self.timestep = 0


game = Game()
game.run()