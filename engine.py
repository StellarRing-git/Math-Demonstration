import pygame
import pymunk
import pymunk.pygame_util
import math

pygame.init()


screen = pygame.display.set_mode((600,400))



def draw(space, screen, draw_options):
	space.debug_draw(draw_options)

	pygame.display.update()

def create_floor(space):
	b0 = space.static_body
	segment = pymunk.Segment(b0, (50, 350), (550, 350), 4)
	segment.elasticity = 0
	space.add(segment)

def create_wall(space):
	b0 = space.static_body
	segment = pymunk.Segment(b0, (50, 350), (50, 50), 4)
	segment.elasticity = 1
	space.add(segment)


def create_obj1(space):
	body = pymunk.Body(body_type=pymunk.Body.DYNAMIC,mass=10,moment=100)
	body.position = 300,320
	vs=[(-25,-25),(25,-25),(25,25),(-25,25)]
	shape = pymunk.Poly(body, vs)
	shape.elasticity = 1
	shape.friction = 0
	shape.color = (150, 50, 0, 100)
	

	#rotation_limit_body = pymunk.Body(body_type = pymunk.Body.STATIC) # 1
	#rotation_limit_body.position = (300,320)
	#rotation_limit_joint=pymunk.SlideJoint(body, rotation_limit_body, (-0,0), (0,0),0, 0)

	body.apply_impulse_at_local_point((-1000,0),(0,0))

	space.add(body, shape,)
	return shape,body.position

def create_obj2(space):
	body = pymunk.Body(body_type=pymunk.Body.DYNAMIC,mass=10,moment=100)
	body.position = 200,327
	vs=[(-25,-25),(25,-25),(25,25),(-25,25)]
	shape = pymunk.Poly(body, vs)
	shape.elasticity = 1
	shape.friction = 0
	shape.color = (150, 50, 0, 100)
	space.add(body, shape)
	return shape,body.position

def run(window):
	run = True
	clock = pygame.time.Clock()
	fps = 60

	space = pymunk.Space()
	space.gravity = (0, 100)
	create_obj1(space)
	create_obj2(space)
	create_floor(space)
	create_wall(space)
	draw_options = pymunk.pygame_util.DrawOptions(window)

	b0 = space.static_body
	segment = pymunk.Segment(b0, (0, 0), (640, 0), 4)
	segment.elasticity = 1

	while run:
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				break

		draw(space, window, draw_options)
		space.step(1/fps)
		clock.tick(fps)
		window.fill((30,30,30))
		

	pygame.quit()

if __name__ == "__main__":
	run(screen)