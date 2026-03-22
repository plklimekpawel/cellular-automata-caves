from settings import *

class Camera:
    def __init__(self):
        self.speed = 1000

        self.target = Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.camera = Camera2D()
        self.camera.zoom = 1
        self.camera.offset = Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.camera.rotation = 0
        self.camera.target = self.target

    def grid_overlay(self):
        top_left = get_screen_to_world_2d(Vector2(0, 0), self.camera)
        bottom_right = get_screen_to_world_2d(Vector2(WINDOW_WIDTH, WINDOW_HEIGHT), self.camera)

        start_x = int(top_left.x // TILE_SIZE)
        end_x = int(bottom_right.x // TILE_SIZE) + 1

        start_y = int(top_left.y // TILE_SIZE)
        end_y = int(bottom_right.y // TILE_SIZE) + 1
        for x in range(start_x, end_x):
            world_x = x * TILE_SIZE
            draw_line(int(world_x), int(top_left.y), int(world_x), int(bottom_right.y), (50, 50, 50, 100))
        for y in range(start_y, end_y):
            world_y = y * TILE_SIZE
            draw_line(int(top_left.x), int(world_y), int(bottom_right.x), int(world_y), (50, 50, 50, 100))

    def update(self, delta_time):
        direction = Vector2()
        direction.x = int(is_key_down(KEY_RIGHT)) - int(is_key_down(KEY_LEFT))
        direction.y = int(is_key_down(KEY_DOWN)) - int(is_key_down(KEY_UP))
        direction = vector2_normalize(direction)

        self.target.x += direction.x * self.speed * delta_time
        self.target.y += direction.y * self.speed * delta_time
        self.camera.target = self.target

    def draw(self, debug):
        if not debug: return
        self.grid_overlay()