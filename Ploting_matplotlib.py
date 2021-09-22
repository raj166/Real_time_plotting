import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('ggplot')
x_vals = []
y1_vals = []
y2_vals = []
index = count()

fig, ax = plt.subplots(2, 2)


def animate(i, self=None):
    # read data
    data = pd.read_csv('data.csv')
    x = data['x_value']
    y1 = data['total_1']
    y2 = data['total_2']

    if y1.values[-1] > 50:
        pass

    # append the data
    x_vals.append(x.values[-1])
    y1_vals.append(y1.values[-1])
    y2_vals.append(y2.values[-1])
    x_limit = x_vals[-20:]

    # plot the data
    ax[0].cla()
    if len(x_limit) > 3:
        ax[0].set_xlim([x_limit[0], x_limit[-1]])
    ax[0].plot(x_vals, y1_vals, label='Channel 1')
    ax[0].legend(loc='upper left')

    ax[1].cla()
    if len(x_limit) > 3:
        ax[1].set_xlim([x_limit[0], x_limit[-1]])
    ax[1].plot(x_vals, y2_vals, label='Channel 2')
    ax[1].legend(loc='upper left')

    fig.tight_layout()


ani = FuncAnimation(plt.gcf(), animate, interval=1000)

fig.tight_layout()
plt.show()
