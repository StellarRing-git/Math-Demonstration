import pygame,sys,pymunk




screen=pygame.display.set_mode((600,400))

def draw(space, screen, draw_options):
	space.debug_draw(draw_options)

	pygame.display.update()

def create_block(space):
    body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
    body.position = 300,100
    shape = pymunk.Circle(body, 30)
    shape.mass = 40
    shape.elasticity = 0.9
    shape.friction = 0.4
    shape.color = (255, 0, 0, 100)
    space.add(body, shape)
    return shape

     
pygame.init()
fps=120

clock=pygame.time.Clock()
space=pymunk.Space()
space.gravity = (0,1)
draw_options = pymunk.pygame_util.DrawOptions(screen)



def run(screen):
    run = True
    create_block(space)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw(space, screen, draw_options)
        screen.fill((30,30,30))
        space.step(1/fps)
        clock.tick(fps)
        



if __name__ == "__main__":
	run(screen)
