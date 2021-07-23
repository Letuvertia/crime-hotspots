import imageio ## to convert to mp4, please also run "pip install imageio-ffmpeg"
import matplotlib.pyplot as plt
import numpy as np
import os
import datetime


class Plot2DArray(object):
    def __init__(self, output_dir="imgfiles"):
        super().__init__()
        # use current time as filename
        self.time = datetime.datetime.now().strftime('%m_%d_%H_%M')
        self.output_dir=output_dir

        self.max_digit = 4
        self.plotted_img_paths = []


    def plot_map(self, map, t, cmap="magma", figure_size=(9, 9)):
        """
        Param
        - map: np.array
            an 2d numpy array to plot
        - t: float
            current timestep t
        - cmap:
            the color set for meshcolor.
            you can choose the one you like at https://matplotlib.org/stable/tutorials/colors/colormaps.html
        """
        title = "t = {}".format(t)
        output_path = os.path.join(os.getcwd(), self.output_dir, self.time)
        filename = "simulation_{}_t_{}.png".format(self.time, t)
        plt.figure(figsize=figure_size, dpi=80)
        plt.title(title)
        plt.imshow(map, cmap=cmap)
        plt.colorbar(orientation='vertical')
        self.plotted_img_paths.append(self._save_fig(output_path, filename, t))
    

    def _save_fig(self, output_path, fn, t):
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        file_path = os.path.join(output_path, fn)
        plt.savefig(file_path)
        print("|t={}| figrue saved to {}".format((str(t)+' '*self.max_digit)[:self.max_digit], file_path))
        return file_path

    
    def save_gif(self, fps=30):
        filename = "simulation_{}.gif".format(self.time)
        file_path = os.path.join(os.getcwd(), self.output_dir, filename)
        images = [imageio.imread(img_path) for img_path in self.plotted_img_paths]
        imageio.mimsave(file_path, images, duration=1/fps)
        print("gif saved to {}".format(file_path))

    
    def save_mp4(self, fps=30):
        filename = "simulation_{}.mp4".format(self.time)
        file_path = os.path.join(os.getcwd(), self.output_dir, filename)
        writer = imageio.get_writer(file_path, fps=20)
        for img_path in self.plotted_img_paths:
            writer.append_data(imageio.imread(img_path))
        writer.close()
        print("mp4 saved to {}".format(file_path))




if __name__ == "__main__":
    # usage example
    t = 60
    lots_of_data = np.random.randint(256, size=(t, 128, 128))
    plotter = Plot2DArray()
    for i in range(t):
        plotter.plot_map(lots_of_data[i], i)
    plotter.save_gif()
    plotter.save_mp4()
