from display.colors import COLORS
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

class Viewer:
    def __init__(self, cube):
        self.cube = cube
        self.n = cube.n
        self.fig, self.ax = plt.subplots(
            3, 4,
            figsize=(8, 6),
            facecolor="#bbbbbb",
            gridspec_kw={"wspace": 0, "hspace": 0}
        )
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
        for a in self.ax.flat:
            a.set_visible(False)
        self.layout = {
            0: (0, 1),
            4: (1, 0),
            1: (1, 1),
            2: (1, 2),
            3: (1, 3),
            5: (2, 1),
        }

    def draw_face(self, ax, face_idx):
        face = self.cube.faces[face_idx]
        ax.cla()
        ax.set_xlim(0, self.n)
        ax.set_ylim(0, self.n)
        ax.set_box_aspect(1)
        ax.axis("off")
        ax.set_facecolor("white")
        for i in range(self.n):
            for j in range(self.n):
                rect = Rectangle((j, self.n - 1 - i), 1, 1, facecolor=COLORS[face[i, j]], edgecolor='black', linewidth=1)
                ax.add_patch(rect)

    def update(self):
        for a in self.ax.flat:
            a.set_visible(False)
        for face_idx, (row, col) in self.layout.items():
            ax = self.ax[row, col]
            ax.set_visible(True)
            self.draw_face(ax, face_idx)
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()

    def show(self):
        plt.show(block=False)
        self.fig.canvas.mpl_connect("resize_event", self._fix_aspect)

    def _fix_aspect(self, event):
        w, h = self.fig.get_size_inches()
        target_ratio = 4/3
        if w/h > target_ratio:
            new_w = h * target_ratio
            left = (w - new_w)/2/w
            self.fig.subplots_adjust(left=left, right=left + new_w/w, bottom=0, top=1)
        else:
            new_h = w / target_ratio
            bottom = (h - new_h)/2/h
            self.fig.subplots_adjust(left=0, right=1, bottom=bottom, top=bottom + new_h/h)

    def close(self):
        plt.close(self.fig)
