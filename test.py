import pygame

pygame.init()
x = 5
y = 10
window = pygame.display.set_mode((300,300))
rect2 = pygame.Rect(0, 0, x, y)
def create_obj():
    rect1 = pygame.Rect(*window.get_rect().center, 0, 0).inflate(75, 75)
    return rect1

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    rect=create_obj()
    rect2.center = pygame.mouse.get_pos()
   
    color = (255, 0, 0) 

    window.fill(0)
    pygame.draw.rect(window, color, rect)
    pygame.draw.rect(window, (0, 255, 0), rect2, 6, 1)
    pygame.display.flip()

pygame.quit()
exit()