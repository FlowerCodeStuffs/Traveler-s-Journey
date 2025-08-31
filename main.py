from pyray import *
from JsonReader import JsonReader
from player import Player
from CameraShake import CameraShake

init_window(1000, 800, "Title")
init_audio_device()
set_target_fps(250)

PLAYER = Player(10)
PLAYER.LoadAudio()

GAME_DATA = JsonReader.LoadJson("data/game.json")
CAMERA = Camera2D(Vector2(0,0), Vector2(0,0))
CAMERA.rotation = GAME_DATA["Game:Priority"][0]["rotation"]
CAMERA.zoom = GAME_DATA["Game:Priority"][0]["zoom"]

Camera_Shake = CameraShake(CAMERA)

while not window_should_close():
    begin_drawing()
    clear_background(BLACK)
    begin_mode_2d(CAMERA)

    PLAYER.Draw()
    PLAYER.Update(get_frame_time())

    if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
        Camera_Shake.trigger(5, 0.1)
    
    Camera_Shake.update(get_frame_time())

    end_mode_2d()
    end_drawing()

PLAYER.Unload()
GAME_DATA["Game:Priority"][0]["zoom"] = CAMERA.zoom
GAME_DATA["Game:Priority"][0]["rotation"] = CAMERA.rotation
PLAYER.Save()

close_audio_device()
close_window()
