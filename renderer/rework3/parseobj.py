import numpy as np
import os.path

def create_Filtered_file(file_name):
    new_filename = file_name[0:len(file_name)-4] + "_filtered.obj"
    if os.path.isfile(new_filename): return new_filename
    file = open(file_name, "r")
    lines = file.readlines()
    with open(new_filename, "w+") as file_filtered:
        for line in lines:
            if len(line) > 2:
                if line[0] == "v" and line[1] == " ":
                    file_filtered.write(line)
                elif line[0] == "f" and line[1] == " ":
                    file_filtered.write(line)
    file_filtered.close()
    return new_filename

def get_vertices(lines):
    vertices = []
    for line in lines:
        if line[0] == "v":
            fl_string = line[2:].replace(" ", ",").replace("\n", "")
            fl_string = np.fromstring(fl_string, dtype=float, sep=",")
            vertices.append(fl_string)
    return vertices


def get_indices(lines):
    indices = []
    for line in lines:
        if line[0] == "f":
            fl_arr = np.fromstring(line[2:], dtype=float, sep=' ')
            fl_arr = np.subtract(fl_arr, 1).astype(np.int32)
            indices.append(fl_arr)
    return indices


def create_primitive_array(vertices, indices):
    primitive_arr = []
    for ind in indices:
        v = np.array([np.append(vertices[index], 0).reshape(4, 1) for index in ind])
        primitive_arr.append(v)
    return primitive_arr
