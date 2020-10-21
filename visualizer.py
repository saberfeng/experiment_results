import matplotlib.pyplot as plt


class Visualizer:

    def __init__(self):
        pass

    def run(self):
        # plot
        plt.plot( 'x', 'y', data=df, linestyle='-', marker='o')
        plt.show()
