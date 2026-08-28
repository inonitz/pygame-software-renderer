from Cube import Cube
from Vertex import Vertex
import math


def place(camera, cube, world):

    length = 0.2
    run = True

    is_place = False

    while run:

        check_vertex = Vertex(0, 0, length)

        check_vertex.rotate_x(camera.xangle).rotate_y(camera.yangle)

        check_vertex.x += camera.x
        check_vertex.y += camera.y
        check_vertex.z += camera.z

        if run:
            for block in world:
                if block.is_in_cube(check_vertex):
                    is_place = True
                    run = False

            print(Cube(0, 0, 0, 1, (0, 0, 0)).is_in_cube(check_vertex))

            length += 0.2

            if math.sqrt((camera.x - check_vertex.x)**2 + (camera.y - check_vertex.y)**2 + (camera.z - check_vertex.z)**2)\
                    > 5:
                run = False

    if is_place:
        d_x = int(round(camera.x - check_vertex.x))
        d_y = int(round(camera.y - check_vertex.y))
        d_z = int(round(camera.z - check_vertex.z))

        print(int(check_vertex.x + d_x)),
        print(int(check_vertex.y + d_y)),
        print(int(check_vertex.z + d_z))

        print(type(Cube(int(check_vertex.x + d_x), int(check_vertex.y + d_y), int(check_vertex.z + d_z), 1, cube.color)))
