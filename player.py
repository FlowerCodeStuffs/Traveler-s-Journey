from pyray import *
from entity import Entity
from JsonReader import JsonReader
import math
from random import uniform

def GetSwingHitboxPosition(player_pos: Vector2, cursor_pos: list, offset_distance: float):
        dir_x = cursor_pos[0] - player_pos.x
        dir_y = cursor_pos[1] - player_pos.y
        
        length = math.sqrt(dir_x**2 + dir_y**2)
        if length == 0:
            length = 1
        
        dir_x /= length
        dir_y /= length

        hitbox_x = player_pos.x + dir_x * offset_distance
        hitbox_y = player_pos.y + dir_y * offset_distance

        return Vector2(hitbox_x, hitbox_y)

class Player(Entity):
    def __init__(self, radius: int):
        nit = JsonReader.LoadJson("data/player.json")
        super().__init__(Vector2(nit["position"]["x"], nit["position"]["y"]), nit)

        self.Data["hitbox"]["radius"] = radius
        self.Radius = self.Data["hitbox"]["radius"]
        self.Velocity = Vector2(self.Data["velocity"]["x"], self.Data["velocity"]["y"])

        self.CursorPosition = self.Data["player:cursor"]["position"]
        self.isDashing = False
        self.dashTime = 0.0
        self.dashDuration = 0.2
        self.dashStart = Vector2(0, 0)
        self.dashTarget = Vector2(0, 0)

        gst = JsonReader.LoadJson("data/game.json")
        self.SoundEffectsPaths = [gst["Game:Sfx"][5]] # * swing.wav
        self.soundPool = []
        self.poolSize = 4  
        self.nextSoundIndex = 0

    # ! Load audio AFTER audio device is initialized
    def LoadAudio(self):
        for path in self.SoundEffectsPaths:
            for _ in range(self.poolSize):
                self.soundPool.append(load_sound(path))

    def Draw(self):
        draw_circle_lines_v(self.Position, self.Radius, WHITE)
        draw_circle_lines_v(self.CursorPosition, self.Data["player:cursor"]["radius"], WHITE)

        hitbox_center = GetSwingHitboxPosition(self.Position, self.CursorPosition, 40)
        hitbox_radius = 15  # size of the swing
        draw_circle_lines_v(hitbox_center, hitbox_radius, RED)


    def Update(self, Delta):
        self.Data["position"]["x"] = self.Position.x
        self.Data["position"]["y"] = self.Position.y
        speed = self.Data["info"]["speed"]

        if is_key_down(KeyboardKey.KEY_LEFT_SHIFT):
            speed *= 1.7

        dx, dy = 0, 0
        if not self.isDashing:
            if is_key_down(KeyboardKey.KEY_A): dx -= 1
            if is_key_down(KeyboardKey.KEY_D): dx += 1
            if is_key_down(KeyboardKey.KEY_W): dy -= 1
            if is_key_down(KeyboardKey.KEY_S): dy += 1

        length = math.sqrt(dx*dx + dy*dy)
        if length != 0:
            dx /= length
            dy /= length

        self.Position.x += dx * speed * Delta
        self.Position.y += dy * speed * Delta

        self.UpdateCursor()

        if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
            self.StartDash()
            if self.soundPool:
                self.SwingSound()
        if self.isDashing:
            self.UpdateDash(Delta)

        if is_key_pressed(KeyboardKey.KEY_SPACE):
            if self.soundPool:
                self.SlashSound()

    def SwingSound(self):
        snd = self.soundPool[self.nextSoundIndex]
        set_sound_pitch(snd, uniform(0.7, 1.0))
        play_sound(snd)
        self.nextSoundIndex = (self.nextSoundIndex + 1) % self.poolSize
    
    def SlashSound(self):
        snd = self.soundPool[self.nextSoundIndex]
        set_sound_pitch(snd, uniform(1.0, 1.5))
        play_sound(snd)
        self.nextSoundIndex = (self.nextSoundIndex + 1) % self.poolSize

    def Save(self):
        self.Data["hitbox"]["radius"] = self.Radius
        self.Data["position"]["x"] = self.Position.x
        self.Data["position"]["y"] = self.Position.y
        self.Data["player:cursor"]["position"] = self.CursorPosition
        JsonReader.OverrideJson("data/player.json", self.Data)

    def Unload(self):
        for snd in self.soundPool:
            unload_sound(snd)

    def UpdateCursor(self):
        _mouse_pos = get_mouse_position()
        self.CursorPosition = [_mouse_pos.x, _mouse_pos.y]
        self.Data["player:cursor"]["position"] = self.CursorPosition

    def StartDash(self):
        self.isDashing = True
        self.dashTime = 0.0
        self.dashStart = Vector2(self.Position.x, self.Position.y)

        dir_x = self.CursorPosition[0] - self.Position.x
        dir_y = self.CursorPosition[1] - self.Position.y
        length = math.sqrt(dir_x*dir_x + dir_y*dir_y)
        if length != 0:
            dir_x /= length
            dir_y /= length

        dashDistance = 50
        self.dashTarget = Vector2(
            self.Position.x + dir_x * dashDistance,
            self.Position.y + dir_y * dashDistance
        )

    def UpdateDash(self, Delta):
        self.dashTime += Delta
        t = self.dashTime / self.dashDuration
        if t >= 1.0:
            t = 1.0
            self.isDashing = False

        ease_t = 1 - (1 - t) * (1 - t)
        self.Position.x = self.dashStart.x + (self.dashTarget.x - self.dashStart.x) * ease_t
        self.Position.y = self.dashStart.y + (self.dashTarget.y - self.dashStart.y) * ease_t
