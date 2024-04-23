import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def read_off(file):
    if 'OFF' != file.readline().strip():
        raise ValueError('Not an OFF file')
    n_verts, n_faces, _ = map(int, file.readline().strip().split())
    verts = [[float(s) for s in file.readline().strip().split()] for _ in range(n_verts)]
    faces = [[int(s) for s in file.readline().strip().split()][1:] for _ in range(n_faces)]
    return verts, faces


def plot_mesh(vertices, faces):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Create a Poly3DCollection from the faces and vertices
    poly3d = [[vertices[vert_id] for vert_id in face] for face in faces]
    mesh = Poly3DCollection(poly3d, edgecolor='k')
    ax.add_collection3d(mesh)

    # Auto scale to the mesh size
    scale = np.concatenate([np.array(vertices)]).flatten()
    ax.auto_scale_xyz(scale, scale, scale)

    plt.show()

