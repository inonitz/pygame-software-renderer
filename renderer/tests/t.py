import pygame


width = 480
height = 480
window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
running = True

for i in range(0, 100):
    for j in range(0, 100):
        pygame.display.get_surface().set_at((i, j), [255, 255, 255])
pygame.display.update()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


