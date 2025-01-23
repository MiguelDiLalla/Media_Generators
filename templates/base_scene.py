from manim import *

class BaseScene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_image = None
        self.mask_circle = None

    def construct(self):
        # Setup layers
        self.setup_background_image("assets/images/default_background.jpg")
        self.setup_mask_circle()

        # Add animations
        self.play(self.animate_mask_circle())
        self.wait(2)

    def setup_background_image(self, image_path, saturation=1.0, opacity=1.0):
        """
        Adds a background image to the scene with adjustable saturation and opacity.
        """
        self.background_image = ImageMobject(image_path)
        self.background_image.set_opacity(opacity)
        self.background_image.set_saturation(saturation)
        self.background_image.set_z_index(0)  # Ensure it's the bottom layer
        self.add(self.background_image)

    def setup_mask_circle(self, radius=2, color=WHITE, opacity=0.7):
        """
        Creates a circular mask with customizable properties.
        """
        self.mask_circle = Circle(radius=radius, color=color, fill_opacity=opacity)
        self.mask_circle.set_z_index(1)  # Ensure it's above the background
        self.add(self.mask_circle)

    def animate_mask_circle(self, amplitude=0.5, frequency=1.0):
        """
        Creates an oscillating animation for the circular mask.
        """
        return self.mask_circle.animate.scale(1 + amplitude * np.sin(frequency * self.time))

# Example usage if executed directly
if __name__ == "__main__":
    from manim import *
    scene = BaseScene()
    scene.render()
