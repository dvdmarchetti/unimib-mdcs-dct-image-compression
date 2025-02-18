import math


import numpy as np


def dct(V):
    """
    Implementation from pdf formula (Parte_2.pdf).
    """
    N = len(V)
    c = np.zeros(N)
    for k in range(N):
        s = 0

        for i in range(N):
            s += V[i] * np.cos(k * np.pi * ((2*i+1) / (2*N)))

        alpha = 1 / math.sqrt(N) if k == 0 else math.sqrt(2 / N)
        c[k] = alpha * s

    return c


def idct(C):
    N = len(C)
    f = np.zeros(N, dtype=np.float)
    for j in range(N):
        s = 0

        for k in range(N):
            alpha = 1 / math.sqrt(N) if k == 0 else math.sqrt(2 / N)
            s += C[k] * alpha * np.cos(k * np.pi * ((2*j+1) / (2*N)))

        f[j] = s

    return f


def dct2(Mat):
    N, M = Mat.shape

    C = np.zeros((N, M), dtype='float')
    for j in range(M):
        C[:, j] = dct(Mat[:, j])


    for i in range(N):
        C[i, :] = dct(C[i, :])

    return C


    # N, M = Mat.shape
    # C = np.zeros((N, M), dtype=float)
    # for k in range(N):
    #     for l in range(M):
    #         s = 0
    #         for i in range(N):
    #             for j in range(M):
    #                 # M(i+1,j+1) = sqrt(2/N)*cos(pi*k*(2*i+1)/(2*N))*cos(pi*l*(2*j+1)/(2*N));
    #                 # print(np.cos(np.dot(math.pi*k, (2*i-1)/(2*N))) * np.cos(np.dot(math.pi*l, (2*j-1)/(2*N)));)
    #                 s += Mat[i,j] * np.cos(k * np.pi * ((2*i+1) / (2*N))) * np.cos(l * np.pi * ((2*j+1) / (2*M)))

    #         if (k == 0 and l == 0):
    #             alpha = (1 / math.sqrt(N*M))
    #         elif (k >= 1 and l == 0) or (k == 0 and l >= 1):
    #             alpha = math.sqrt(2 / N)
    #         else:
    #             alpha = 2 / math.sqrt(N*M)

    #         C[k][l] = alpha * s

    # return C