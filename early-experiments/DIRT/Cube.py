import pygame
from Vertex import Vertex


class Cube:

    def __init__(self, x, y, z, edge, color):

        self.x = x
        self.y = y
        self.z = z
        self.color = color

        vertex_list = [Vertex(x + edge * i, y + edge * j, z + edge * k)
                       for i in range(2)
                       for j in range(2)
                       for k in range(2)]

        self.vertex_list = tuple(vertex_list)

        self.edge_list = (
            (self.vertex_list[0], self.vertex_list[1]), (self.vertex_list[2], self.vertex_list[3]),
            (self.vertex_list[4], self.vertex_list[5]), (self.vertex_list[6], self.vertex_list[7]),
            (self.vertex_list[0], self.vertex_list[2]), (self.vertex_list[1], self.vertex_list[3]),
            (self.vertex_list[4], self.vertex_list[6]), (self.vertex_list[5], self.vertex_list[7]),
            (self.vertex_list[0], self.vertex_list[4]), (self.vertex_list[1], self.vertex_list[5]),
            (self.vertex_list[2], self.vertex_list[6]), (self.vertex_list[3], self.vertex_list[7]))

        self.face_list = (
            (self.vertex_list[0], self.vertex_list[1], self.vertex_list[3], self.vertex_list[2]),
            (self.vertex_list[4], self.vertex_list[5], self.vertex_list[7], self.vertex_list[6]),
            (self.vertex_list[0], self.vertex_list[1], self.vertex_list[5], self.vertex_list[4]),
            (self.vertex_list[2], self.vertex_list[3], self.vertex_list[7], self.vertex_list[6]),
            (self.vertex_list[0], self.vertex_list[2], self.vertex_list[6], self.vertex_list[4]),
            (self.vertex_list[1], self.vertex_list[3], self.vertex_list[7], self.vertex_list[5])
        )

    def __str__(self):
        return "x: {0}, y: {1}, z: {2}, color: {3}, ".format(self.x, self.y, self.z, self.color)

    def draw_vertices(self, camera, screen):
        for vertex in self.vertex_list:
            if camera.isproject(vertex, screen):
                pygame.draw.circle(screen, self.color, camera.project(vertex, screen), 5)

    def draw_edges(self, camera, screen):
        for edge in self.edge_list:
            if camera.isproject(edge[0], screen) and camera.isproject(edge[1], screen):
                pygame.draw.line(screen, self.color, camera.project(edge[0], screen), camera.project((edge[1]), screen))

    def get_closest_vertex(self, camera):

        dist_list = [(v.x - camera.x) ** 2 + (v.y - camera.y) ** 2 + (v.z - camera.z) ** 2 for v in self.vertex_list]

        return self.vertex_list[dist_list.index(min(dist_list))]

    def draw_faces(self, camera, screen):

        face_list = [face for face in self.face_list if self.get_closest_vertex(camera) in face]

        for face in face_list:
            if sum([camera.isproject(face[i], screen) for i in range(4)]) == 4:
                pygame.draw.polygon(screen, self.color, [camera.project(face[i], screen) for i in range(4)], 0)

    def is_in_cube(self, vertex):
        return self.vertex_list[0].x <= vertex.x <= self.vertex_list[7].x and \
               self.vertex_list[0].y <= vertex.y <= self.vertex_list[7].y and \
               self.vertex_list[0].z <= vertex.z <= self.vertex_list[7].z
