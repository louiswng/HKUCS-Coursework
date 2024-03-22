import cv2
import numpy as np
from scipy.sparse import lil_matrix, linalg


def spsolve(target, mask, lap):
    indices = np.nonzero(mask)
    num_pixels = indices[0].shape[0] 

    A = lil_matrix((num_pixels, num_pixels), dtype=np.float64)
    b = np.ndarray((num_pixels, ), dtype=np.float64)
    
    index_map = {(x, y): i for i, (x, y) in enumerate(zip(indices[0], indices[1]))}
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    for i, (x, y) in enumerate(zip(indices[0], indices[1])):
        A[i, i] = -4
        b[i] = lap[x, y]
        p = [(x + dx[j], y + dy[j]) for j in range(4)]
        for j in range(4):
            if p[j] in index_map:
                A[i, index_map[p[j]]] = 1
            else:
                b[i] -= target[p[j]]
                
    A = A.tocsc()
    X = linalg.splu(A).solve(b)

    result = np.copy(target)
    for i, (x, y) in enumerate(zip(indices[0],indices[1])):
        if X[i] < 0:
            X[i] = 0
        if X[i] > 255:
            X[i] = 255
        result[x, y] = X[i]

    return result


def poisson_edit(source, target, mask, center):
    laplacian = cv2.Laplacian(np.float64(source), ddepth=-1, ksize=1)

    indices = np.nonzero(mask)
    x_begin, x_end, y_begin, y_end = np.min(indices[0]) - 1, np.max(indices[0]) + 1, np.min(indices[1]) - 1, np.max(indices[1]) + 1

    mask = mask[x_begin: x_end, y_begin: y_end]
    source = source[x_begin: x_end, y_begin: y_end]
    laplacian = laplacian[x_begin: x_end, y_begin: y_end]

    final_mask = np.zeros((target.shape[0], target.shape[1]))
    final_source = np.zeros_like(target)
    final_laplacian = np.zeros_like(target, dtype=np.float64)

    x_mid = (np.max(indices[0]) - np.min(indices[0])) // 2 + 1
    x_begin = center[0] - x_mid
    x_end = center[0] + mask.shape[0] - x_mid
    y_mid = (np.max(indices[1]) - np.min(indices[1])) // 2 + 1
    y_begin = center[1] - y_mid
    y_end = center[1] + mask.shape[1] - y_mid

    final_mask[x_begin: x_end, y_begin: y_end] = mask
    final_source[x_begin: x_end, y_begin: y_end] = source
    final_laplacian[x_begin: x_end, y_begin: y_end] = laplacian

    result = [spsolve(a, final_mask, b) for a, b in zip(cv2.split(target), cv2.split(final_laplacian))]
    
    final = cv2.merge(result)
    return final

