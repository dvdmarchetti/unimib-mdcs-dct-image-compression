import math
import time


# import matplotlib
# matplotlib.use('WebAgg')


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.fftpack import dctn, dct
import seaborn as sns


import custom_dct


def test_dctn():
    """
    Verify that dcnt is correct
    """
    mat = np.array([
        [231, 32, 233, 161, 24, 71, 140, 245],
        [247, 40, 248, 245, 124, 204, 36, 107],
        [234, 202, 245, 167, 9, 217, 239, 173],
        [193, 190, 100, 167, 43, 180, 8, 70],
        [11, 24, 210, 177, 81, 243, 8, 112],
        [97, 195, 203, 47, 125, 114, 165, 181],
        [193, 70, 174, 167, 41, 30, 127, 245],
        [87, 149, 57, 192, 65, 129, 178, 228],
    ])
    print(dctn(mat, norm='ortho'))


def test_custom_dct_idct(v):
    """
    Test that v -> DCT -> IDCT -> w  =>  v = w
    """
    dct_v = custom_dct.dct(v)
    print(dct_v)
    idct_v = custom_dct.idct(dct_v)
    print(idct_v)


def test_custom_dct2_idct2(mat):
    """
    Test that M -> DCT2 -> IDCT2 -> N  =>  M = N
    """
    dct2_mat = custom_dct.dct2(mat)
    print(dct2_mat)
    exit()
    idct2_mat = custom_dct.idct2(dct2_mat)
    print(idct2_mat)
    print(custom_dct.dct2(mat))


# v = np.array([231, 32, 233, 161, 24, 71, 140, 245], dtype=float)
# test_custom_dct_idct(v)

# mat = np.array([
#     [231, 32, 233, 161, 24, 71, 140, 245],
#     [247, 40, 248, 245, 124, 204, 36, 107],
#     [234, 202, 245, 167, 9, 217, 239, 173],
#     [193, 190, 100, 167, 43, 180, 8, 70],
#     [11, 24, 210, 177, 81, 243, 8, 112],
#     [97, 195, 203, 47, 125, 114, 165, 181],
#     [193, 70, 174, 167, 41, 30, 127, 245],
#     [87, 149, 57, 192, 65, 129, 178, 228],
# ])
# r = test_custom_dct2_idct2(mat)
# np.savetxt('out.csv', r, fmt='%.3f')

def performance_test(offset, how_many, step=1):
    matrices = []

    for index in range(0, how_many*step, step):
        size = index + offset
        problem = np.random.randint(0, 255, size=(size, size))

        tic = time.perf_counter()
        dctn(problem, type=2, norm='ortho')
        toc = time.perf_counter()

        matrices.append({
            'size': size,
            'duration': float(toc - tic),
            'type': 'scipy'
        })

        print('[FFT] Matrix ({0},{0}) took {1:.4f}ms to complete.'.format(size, float(toc-tic)))

        tic = time.perf_counter()
        custom_dct.dct2(problem)
        toc = time.perf_counter()

        matrices.append({
            'size': size,
            'duration': float(toc - tic),
            'type': 'implemented'
        })

        print('[DCT] Matrix ({0},{0}) took {1:.4f}ms to complete.'.format(size, float(toc-tic)))

    return matrices



def plot_results(results):
    df = pd.DataFrame.from_dict(results)

    ax = plt.axes()

    sns.lineplot(data=df, x='size', y='duration', hue='type', marker='o', ax=ax)
    ax.set_yscale('log')

    plt.show()


# Plot style
sns.set_style('darkgrid')

offset = 10
step = 10
how_many = 15
results = performance_test(offset, how_many, step)
plot_results(results)
