import numpy as np

def getVertexArray(info):
    vertices = []
    for t in info:
        if t[0] == 'v' and t[1] == ' ':
            fl_string = t[2:].replace(" ", ",").replace("\n", "")
            fl_string = np.fromstring(fl_string, dtype=float, sep=",")
            vertices.append(fl_string)
        else:
            vertices.append(0)
    return np.array(vertices, dtype=object)  # archive fix (2026): modern numpy needs explicit object dtype for ragged lists


def getIndexArray(info):
    indices = []
    for t in info:
        if t[0] == 'f' and t[1] == ' ':
            fl_arr = np.fromstring(t[2:], dtype=float, sep=' ')
            fl_arr = np.subtract(fl_arr, 1).astype(np.int32)
            indices.append(fl_arr)
    return np.array(indices)

#  Rework it!!! (needs to work with other .obj files, even those with normals and shit).
def createTriangles(vertices, indices):
    tris = []
    for ind in indices:
        v = np.array([np.append(vertex, 1).reshape(vertex.shape[0]+1, 1) for vertex in vertices[ind] if type(vertex) != int])
        if v.size == 12:
            tris.append(v)
    return np.array(tris)
