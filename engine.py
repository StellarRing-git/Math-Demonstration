import pygame
import pymunk
import pymunk.pygame_util
import playsound

pygame.init()


screen = pygame.display.set_mode((1200,800))
x=0
print("Collision Count:")
pygame.mixer.init(buffer=256)
pygame.mixer.music.load("clack_sound.mp3")
pygame.mixer.music.set_volume(1.5)




def draw(space, screen, draw_options):
	space.debug_draw(draw_options)

	pygame.display.update()

def create_floor(space):
	b0 = space.static_body
	segment = pymunk.Segment(b0, (100, 700), (1300, 700), 4)
	segment.elasticity = 0
	space.add(segment)

def create_wall(space,collision_type):
	b0 = space.static_body
	segment = pymunk.Segment(b0, (100, 700), (100, 100), 4)
	segment.elasticity = 1
	segment.collision_type = collision_type
	space.add(segment)


def create_obj1(space, collision_type):
	body = pymunk.Body(body_type=pymunk.Body.DYNAMIC,mass=1000,moment=100000)
	body.position =400,640 #previous_pos = 300,320
	vs=[(-50,-50),(50,-50),(50,50),(-50,50)]
	shape = pymunk.Poly(body, vs)
	shape.elasticity = 1
	shape.friction = 0
	shape.color = (150, 50, 0, 100)
	shape.collision_type = collision_type 
	

	#groove_joint_body = pymunk.Body(body_type = pymunk.Body.STATIC) # 1
	#groove_joint_body.position = (400,640)
	#groove_joint=pymunk.GrooveJoint(body, groove_joint_body, (100,640), (1300,640),(0, 0))

	body.apply_impulse_at_local_point((-50*body.mass,0),(0,0))

	space.add(body, shape,)
	return shape,body.position

def create_obj2(space, collision_type):
	body = pymunk.Body(body_type=pymunk.Body.DYNAMIC,mass=0.1,moment=1000000)
	body.position = 200,640 #previous_pos = 200,320
	vs=[(-50,-50),(50,-50),(50,50),(-50,50)]
	shape = pymunk.Poly(body, vs)
	shape.elasticity = 1
	shape.friction = 0
	shape.color = (150, 50, 0, 100)
	shape.collision_type = collision_type
	

	space.add(body, shape)
	return shape,body.position

def create_bounds(space):
	b0 = space.static_body
	segment = pymunk.Segment(b0, (100, 594), (1300, 594), 4)
	segment.color=(30, 30, 30, 0)
	segment.elasticity = 0
	space.add(segment)

def n_collision(arbiter,space,handler): 	
	global x
	x=x+1
	print(x)
	pygame.mixer.music.play()

def run(window):
	run = True
	clock = pygame.time.Clock()
	fps = 100
	dt=100

	space = pymunk.Space()
	space.gravity = (0, 100000)
	create_obj1(space,1)
	create_obj2(space,2)
	create_floor(space)
	create_wall(space,3)
	create_bounds(space)
	draw_options = pymunk.pygame_util.DrawOptions(window)
	

	col_handl1 = space.add_collision_handler(1,2)
	col_handl2 = space.add_collision_handler(2,3)
	col_handl1.post_solve = n_collision
	col_handl2.post_solve = n_collision
	space.use_spatial_hash(50,50)

	while run:
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				break

		draw(space, window, draw_options)
		clock.tick(fps)
		window.fill((30,30,30))
		space.step(1/dt)
		

	pygame.quit()

if __name__ == "__main__":
	run(screen)