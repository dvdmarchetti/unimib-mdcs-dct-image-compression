import numpy as np


class SnaptoCursor(object):
    """
    Like Cursor but the crosshair snaps to the nearest x, y point.
    For simplicity, this assumes that *x* is sorted.
    """

    def __init__(self, ax, x, y):
        self.ax = ax
        self.lx = ax.axhline(color='0.3', linestyle='-')
        self.ly = ax.axvline(color='0.3', linestyle='-')
        self.xvalues = x
        self.yvalues = y
        self.text = ax.text(0.01, 1, '', transform=ax.transAxes, size=15)

    def mouse_move(self, event):
        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata
        indx = min(np.searchsorted(self.xvalues, x), len(self.xvalues) - 1)

        x = self.xvalues[indx]
        y = self.yvalues[indx]

        self.ly.set_xdata(x)
        self.lx.set_ydata(y)

        self.text.set_text('x={:1d}, y={:1.5f}'.format(x, y))
        self.ax.figure.canvas.draw()