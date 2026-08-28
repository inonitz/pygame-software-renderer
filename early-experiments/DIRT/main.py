from Cube import Cube
from player import place
from Camera import base_camera, get_dif
from minecraft_cube import get_dirt
import pygame

pygame.init()


def main():

    world = get_dirt()

    screen_res = (800, 800)
    screen_center = (screen_res[0]/2, screen_res[1]/2)
    speed = 0.1

    main_camera = base_camera

    screen = pygame.display.set_mode(screen_res)

    run = True

    pygame.mouse.set_pos(screen_center)

    while run:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            main_camera.move_forward(speed)

        if keys[pygame.K_s]:
            main_camera.move_backward(speed)

        if keys[pygame.K_d]:
            main_camera.move_right(speed)

        if keys[pygame.K_a]:
            main_camera.move_left(speed)

        if keys[pygame.K_SPACE]:
            main_camera.y -= speed

        if keys[pygame.K_LSHIFT]:
            main_camera.y += speed

        if keys[pygame.K_ESCAPE]:
            run = False

        if pygame.mouse.get_pressed()[0]:
            print(type(place(main_camera, Cube(0, 0, 0, 1, (0, 0, 0)), world)))

        world = sorted(world, key=lambda block: block.get_closest_vertex(main_camera).get_dist(main_camera),
                       reverse=True)

        screen.fill((255, 255, 255))

        main_camera.rotate(get_dif(screen_center, pygame.mouse.get_pos()))

        pygame.mouse.set_pos(screen_center)

        for cube in world:
            cube.draw_faces(main_camera, screen)

        pygame.display.update()


if __name__ == "__main__":

    main()

pygame.quit()
