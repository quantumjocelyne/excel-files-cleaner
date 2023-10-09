import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

class SphericalCow:
    def __init__(self, radius=1.0):
        self.radius = radius

    def moo(self):
        print("Moo! I am a spherical cow with a radius of", self.radius)

    def plot(self):
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')

        # Create the cow
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)

        # Create the head
        x_head = self.radius * np.outer(np.cos(u), np.sin(v)) + self.radius
        y_head = self.radius * np.outer(np.sin(u), np.sin(v))
        z_head = self.radius * np.outer(np.ones(np.size(u)), np.cos(v))
        head_color = 'pink'
        ax.plot_surface(x_head, y_head, z_head, color=head_color)

        # Create the ears
        x_ear1, y_ear1, z_ear1 = np.array([[self.radius + 1.5, 0, 0], [self.radius + 1.5, 0.5, 0], [self.radius + 2, 0.5, 0]])
        x_ear2, y_ear2, z_ear2 = np.array([[self.radius + 1.5, 0, 0], [self.radius + 1.5, -0.5, 0], [self.radius + 2, -0.5, 0]])
        ear_color = 'pink'
        ax.plot(x_ear1, y_ear1, z_ear1, color=ear_color)
        ax.plot(x_ear2, y_ear2, z_ear2, color=ear_color)


        # Create the eyes
        x_eye1, y_eye1, z_eye1 = np.array([[self.radius + 0.7, 0.3, 0], [self.radius + 0.9, 0.5, 0], [self.radius + 0.8, 0.6, 0]])
        x_eye2, y_eye2, z_eye2 = np.array([[self.radius + 0.7, -0.3, 0], [self.radius + 0.9, -0.5, 0], [self.radius + 0.8, -0.6, 0]])
        eye_color = 'black'
        ax.plot(x_eye1, y_eye1, z_eye1, color=eye_color)
        ax.plot(x_eye2, y_eye2, z_eye2, color=eye_color)

        # Create the nose
        x_nose, y_nose, z_nose = np.array([[self.radius + 0.5, 0, 0], [self.radius + 0.7, -0.3, 0], [self.radius + 0.7, 0.3, 0]])
        nose_color = 'black'
        ax.plot(x_nose, y_nose, z_nose, color=nose_color)

        # Create the body
        x_body = np.linspace(self.radius, -self.radius, 100)
        y_body = np.zeros(100)
        z_body = self.radius * np.sin(np.linspace(0, np.pi, 100))
        body_color = 'brown'
        ax.plot(x_body, y_body, z_body, color=body_color)

        # Create the legs
        x_leg1, y_leg1, z_leg1 = np.array([[self.radius - 0.3, -0.3, 0], [self.radius - 0.3, -0.6, 0], [self.radius - 0.2, -0.6, 0]])
        x_leg2, y_leg2, z_leg2 = np.array([[self.radius - 0.3, 0.3, 0], [self.radius - 0.3, 0.6, 0], [self.radius - 0.2, 0.6, 0]])
        leg_color = 'black'
        ax.plot(x_leg1, y_leg1, z_leg1, color=leg_color)
        ax.plot(x_leg2, y_leg2, z_leg2, color=leg_color)

        # Label the axes
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # Set the aspect ratio to 'equal' and show the plot
        ax.set_box_aspect([1, 1, 1])
        plt.show()


#To create an instance of the `SphericalCow` class and plot the cow, you can use the following code:

cow_radius = 10.0
my_cow = SphericalCow(cow_radius)
my_cow.moo()
my_cow.plot()

