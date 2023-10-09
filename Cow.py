import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np



'''
class SphericalCow:
    def __init__(self, radius=1.0, structure='sphere'):
        self.radius = radius
        self.structure = structure

    def moo(self):
        print("Moo! I am a spherical cow with a radius of", self.radius)

    def plot(self):
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')

        # Create the cow
        if self.structure == 'sphere':
            # Create a sphere with the given radius
            u = np.linspace(0, 2 * np.pi, 100)
            v = np.linspace(0, np.pi, 100)
            x = self.radius * np.outer(np.cos(u), np.sin(v))
            y = self.radius * np.outer(np.sin(u), np.sin(v))
            z = self.radius * np.outer(np.ones(np.size(u)), np.cos(v))
            cow_color = 'pink'
        elif self.structure == 'cylinder':
            # Create a cylinder with the given radius and height
            radius = self.radius
            height = 2 * radius
            resolution = 100
            theta = np.linspace(0, 2*np.pi, resolution)
            z = np.linspace(-height/2, height/2, resolution)
            Z, T = np.meshgrid(z, theta)
            X = radius * np.cos(T)
            Y = radius * np.sin(T)
            cow_color = 'brown'
        else:
            raise ValueError('Invalid structure type')

        # Plot the cow
        if self.structure == 'sphere':
            ax.plot_surface(x, y, z, color=cow_color)
        elif self.structure == 'cylinder':
            ax.plot_surface(X, Y, Z, color=cow_color)
            ax.plot_surface(X, Y, -Z, color=cow_color)

        # Add eyes
        ax.scatter(self.radius/2, 0, 0, color='black')
        ax.scatter(-self.radius/2, 0, 0, color='black')

        # Label the axes
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # Set the aspect ratio to 1
        ax.set_box_aspect([1,1,1])

        plt.show()

# Create a cylindrical cow with a radius of 2
my_cow = SphericalCow(radius=2.0, structure='sphere')

# Plot the cow
my_cow.plot()

'''