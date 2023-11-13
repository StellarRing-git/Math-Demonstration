import numpy as np
import pygame



class Game():
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((900,600))
        pygame.display.set_caption("No.of Collisions Simulator")
        
        self.clock = pygame.time.Clock()
        self.fps = 10
        self.running = True

        self.u1 = 0
        self.u2 = -100
        self.m1 = 1
        self.m2 = 100
        self.y = 300
        self.pos1 = np.array([300,self.y])
        self.pos2 = np.array([600,self.y])
        self.obj1 =self.create_obj((self.pos1), self.m1, self.u1)
        self.obj2 = self.create_obj((self.pos2), self.m2, self.u2)
        self.wall = pygame.Rect((200,300),(5,100))

        print(self.wall)

    def create_obj(self, pos, m, v):
        self.pos = pos
        self.mass_obj = m
        self.vel_obj = v
        self.obj = pygame.Rect((self.pos),(50,50))
        return self.obj
    
    
    def cal_pos(self):
        self.delta_pos1 = np.array([self.u1*1/1000,0])
        self.delta_pos2 = np.array([self.u2*1/1000,0])
        print(self.delta_pos2)
        self.pos1 = self.delta_pos1 + self.pos1
        self.pos2 = self.delta_pos2 + self.pos2

    def update_obj(self):
        pygame.Rect.move_ip(self.obj1,1.5,self.delta_pos1[1])
        pygame.Rect.move_ip(self.obj2,self.delta_pos2[0],self.delta_pos2[1])
        print(self.delta_pos2[0])

    def cal_vel(self):
        m1 = self.m1 
        m2 = self.m2 
        u1 = self.u1 
        u2 = self.u2 
        a=2* m1* u1
        b=(m2 - m1) * u2
        c=m1 + m2
        self.u2 = (a + b) / c
        self.u1 = self.u2 + u2 - u1
        print('v1 =', self.u1, 'v2 =', self.u2)

    def cal_vel_wall(self):
        self.u1= -self.u1

    def update(self):
        if self.obj1.colliderect(self.obj2):
            self.cal_vel()
        if self.obj1.colliderect(self.wall):
            self.cal_vel_wall()
        self.cal_pos()
        self.update_obj()
        
        

    def render(self):
        self.window.fill((30,30,30))
        pygame.draw.rect(self.window,(241, 76, 76),self.obj1)
        pygame.draw.rect(self.window,(93, 102, 179),self.obj2)
        pygame.draw.rect(self.window,(161, 216, 187),self.wall)
        pygame.display.update()    

    def run(self):
        while self.running:
            self.update()
            self.render()        
            self.clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    break

game = Game()
game.run()