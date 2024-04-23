import argparse

from model import Mesh, simplify_mesh
from utils import read_off, plot_mesh


def main(args):
    with open(args.data, 'r') as file:
        vertices, faces = read_off(file)

    mesh = Mesh(vertices, faces)
    mesh.print()

    plot_mesh(mesh.vertices, mesh.faces)

    simplified_mesh = simplify_mesh(mesh, int(args.keep_proportion * mesh.num_vertices))
    simplified_mesh.print()

    plot_mesh(simplified_mesh.vertices, simplified_mesh.faces)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Params')
    parser.add_argument('--data', default='ModelNet10', type=str, help='dataset name')
    parser.add_argument('--keep_proportion', default=0.90, type=float, help='keep proportion of vertices')
    args = parser.parse_args()

    main(args)