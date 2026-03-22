from settings import *
from os.path import join


from camera import Camera
from world import World

class Main:
    def __init__(self):
        init_window(WINDOW_WIDTH, WINDOW_HEIGHT, 'Cellular Automata Caves')
        self.font = load_font_ex(join('fonts', 'Pixellari.ttf'), 32, ffi.NULL, 0)

        self.world = World(self)
        self.camera = Camera()

        self.debug = False

    def input(self):
        mouse_screen = get_mouse_position()
        mouse_world = get_screen_to_world_2d(mouse_screen, self.camera.camera)
        if is_key_pressed(KEY_F1): self.debug = not self.debug
        if is_mouse_button_down(0):
            self.world.create_tile(mouse_world.x, mouse_world.y)
        if is_mouse_button_down(1):
            self.world.destroy_tile(mouse_world.x, mouse_world.y)


    def update(self):
        delta_time = get_frame_time()

        self.input()

        self.world.update(self.camera, delta_time)
        self.camera.update(delta_time)

    def draw(self):
        begin_drawing()
        clear_background(LIGHT_GRAY)
        begin_mode_2d(self.camera.camera)

        self.camera.draw(self.debug)
        self.world.draw(self.debug, self.camera, self.font)
        end_mode_2d()

        draw_fps(5, get_screen_height() - 20)
        end_drawing()

    def run(self):
        while not window_should_close():
            self.update()
            self.draw()
        close_window()

if __name__ == '__main__':
    game = Main()
    game.run()