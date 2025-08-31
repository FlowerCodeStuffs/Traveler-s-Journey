from pyray import *
from random import uniform

class CameraShake:
    def __init__(self, camera: Camera2D):
        self.camera = camera
        self.original_target = Vector2(camera.target.x, camera.target.y)
        self.shake_magnitude = 0.0
        self.shake_duration = 0.0
        self.shake_timer = 0.0

    def trigger(self, magnitude: float, duration: float):
        """Start a new camera shake."""
        self.shake_magnitude = magnitude
        self.shake_duration = duration
        self.shake_timer = duration
        self.original_target = Vector2(self.camera.target.x, self.camera.target.y)

    def update(self, delta: float):
        """Call every frame to apply shake."""
        if self.shake_timer > 0:
            self.shake_timer -= delta
            current_magnitude = self.shake_magnitude * (self.shake_timer / self.shake_duration)
            offset_x = uniform(-current_magnitude, current_magnitude)
            offset_y = uniform(-current_magnitude, current_magnitude)
            self.camera.target = Vector2(self.original_target.x + offset_x,
                                         self.original_target.y + offset_y)
        else:
            self.camera.target = Vector2(self.original_target.x, self.original_target.y)
