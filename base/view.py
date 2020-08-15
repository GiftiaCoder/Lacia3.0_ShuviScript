import matplotlib.pyplot as plt
import numpy as np


class ShowView(object):

    def __init__(self, title, height, width):
        self.height = height
        self.width = width
        plt.figure(title, figsize=(10.24, 7.2))
        self.plts = [plt.subplot(height, width, i + 1) for i in range(height * width)]

    def set_data(self, y, x, data, is_colored=True):
        data = data if is_colored else np.concatenate((data, data, data), axis=-1)
        self.plts[x * self.width + y].imshow(data)

    def show(self, time):
        plt.ion()
        plt.pause(time)
