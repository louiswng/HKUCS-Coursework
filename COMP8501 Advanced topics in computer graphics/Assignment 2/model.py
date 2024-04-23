class Mesh:
    def __init__(self, vertices, faces):
        self.vertices = vertices
        self.faces = faces

        self.num_vertices = len(vertices)
        self.num_faces = len(faces)
        self.vertex_error = [0] * self.num_vertices

        self.compute_vertex_error()

    def compute_vertex_error(self):
        vertex_degree = [0] * self.num_vertices

        for face in self.faces:
            for vertex in face:
                vertex_degree[vertex] += 1

        self.vertex_error = [1.0 / degree if degree > 0 else float('inf') for degree in vertex_degree]

    def renumber_vertices_and_faces(self):
        old_to_new_indices = {old_idx: new_idx for new_idx, old_idx in enumerate(sorted(set(vertex for face in self.faces for vertex in face)))}
        self.faces = [[old_to_new_indices[vertex] for vertex in face] for face in self.faces]
        used_vertices = set(idx for face in self.faces for idx in face)
        self.vertices = [self.vertices[i] for i in sorted(used_vertices)]


    def print(self):
        print(f"Num of vertices: {len(self.vertices)}.")
        print(f"Num of faces: {len(self.faces)}.")


def remove_vertex(mesh, target_vertices):
    sorted_vertices = sorted(range(len(mesh.vertex_error)), key=lambda i: mesh.vertex_error[i], reverse=True)
    to_remove = set(sorted_vertices[:target_vertices])

    new_faces = []
    for face in mesh.faces:
        new_face = [v for v in face if v not in to_remove]
        if len(new_face) >= 3:  # Keep faces with at least 3 vertices
            new_faces.append(new_face)

    mesh.faces = new_faces
    mesh.renumber_vertices_and_faces()
    mesh.compute_vertex_error()  # Recompute errors after removal


def simplify_mesh(mesh, target_num_vertices):
    while len(mesh.vertices) > target_num_vertices:
        remove_count = len(mesh.vertices) - target_num_vertices
        remove_vertex(mesh, remove_count)
        if remove_count <= 0:
            break  # Stop if we cannot remove more vertices without breaking the mesh

    return mesh