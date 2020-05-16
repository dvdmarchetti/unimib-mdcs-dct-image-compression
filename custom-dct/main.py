import math
import time


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.fftpack import dctn
import seaborn as sns


from plot_utils import SnaptoCursor
import custom_jpg


# Plot style
sns.set()

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
# result = dctn(mat, type=2, norm='ortho')

# # Test that v -> DCT -> IDCT -> w  => v = w
# v = np.array([231, 32, 233, 161, 24, 71, 140, 245], dtype=float)
# dct_v = custom_jpg.dct(v)
# print(dct_v)
# idct_v = custom_jpg.idct(dct_v)
# print(idct_v)

# # Test that M -> DCT2 -> IDCT2 -> N  => M = N
# dct2_mat = custom_jpg.dct2(mat)
# print(dct2_mat)
# idct2_mat = custom_jpg.idct2(dct2_mat)
# print(idct2_mat)
# print(custom_jpg.dct2(mat))
# exit()

offset = 1
step = 1
how_many = 80
matrices = []

for index in range(0, how_many, step):
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

for matrix in matrices:
    print('Matrix ({0},{0}) took {1:.4f}ms to complete.'.format(matrix['size'], matrix['duration']))


df = pd.DataFrame.from_dict(matrices)

fig = plt.figure()
ax = plt.axes()

sns.lineplot(data=df, x='size', y='duration', hue='type', marker='o', ax=ax)
ax.set_xticks(df['size'])
ax.set_yscale('log')

snap_cursor = SnaptoCursor(ax, df['size'], df['duration'])
fig.canvas.mpl_connect('motion_notify_event', snap_cursor.mouse_move)

sns.despine()
plt.show()
