from settings import *

from chunk import Chunk

def debug_tooltip(x, y, texts, font, font_size=16, spacing=1, padding=3):
    text_sizes = [measure_text_ex(font, text, font_size, spacing) for text in texts]
    max_width = max(size.x for size in text_sizes)
    total_height = sum(size.y for size in text_sizes)

    # Draw text rectangle
    draw_rectangle(int(x), int(y), int(max_width + padding * 2), int(total_height + padding * 2), (0, 0, 0, 150))

    # Draw texts
    offset_y = y + padding
    for text, size in zip(texts, text_sizes):
        draw_text_ex(font, text, Vector2(x + padding, offset_y), font_size, spacing, WHITE)
        offset_y += size.y

class World:
    def __init__(self, main):
        self.chunk_width, self.chunk_height = CHUNK_WIDTH, CHUNK_HEIGHT
        self.active_chunk_range_y = None
        self.active_chunk_range_x = None

        self.chunks = {}

    def _create_chunk(self, chunk_x, chunk_y) -> Chunk:
        chunk_pos = (chunk_x, chunk_y)
        if chunk_pos not in self.chunks:
            grid = Chunk(self.chunk_width, self.chunk_height, chunk_pos, self)
            self.chunks[chunk_pos] = grid
        return self.chunks[chunk_pos]

    def _get_active_chunks_range(self, camera, chunk_range=1):
        chunk_size = self.get_chunk_pixel_size()
        cam_center_x = camera.target.x
        cam_center_y = camera.target.y

        center_chunk_x = int(cam_center_x // chunk_size[0])
        center_chunk_y = int(cam_center_y // chunk_size[1])

        chunks_on_screen_x = math.ceil(WINDOW_WIDTH / (self.chunk_width * TILE_SIZE))
        chunks_on_screen_y = math.ceil(WINDOW_HEIGHT / (self.chunk_height * TILE_SIZE))

        self.active_chunk_range_x = range(center_chunk_x - chunks_on_screen_x // 2 - chunk_range,
                                          center_chunk_x + chunks_on_screen_x // 2 + chunk_range + 1)
        self.active_chunk_range_y = range(center_chunk_y - chunks_on_screen_y // 2 - chunk_range,
                                          center_chunk_y + chunks_on_screen_y // 2 + chunk_range + 1)

    def _set_tile(self, world_x, world_y, value):
        (chunk_x, chunk_y), (tile_x, tile_y) = self.world_to_tile(world_x, world_y)
        chunk = self.try_get_chunk(chunk_x, chunk_y)
        if chunk is None: return

        chunk.tiles[tile_x, tile_y] = value
        chunk.set_dirty()

    def world_to_world_tile(self, world_x, world_y):
        return world_x // TILE_SIZE, world_y // TILE_SIZE

    def world_to_tile(self, world_x, world_y) -> tuple[tuple[int, int], tuple[int, int]]:
        global_tile_x = world_x // TILE_SIZE
        global_tile_y = world_y // TILE_SIZE

        chunk_x = global_tile_x // self.chunk_width
        chunk_y = global_tile_y // self.chunk_height

        local_tile_x = global_tile_x % self.chunk_width
        local_tile_y = global_tile_y % self.chunk_height

        return (int(chunk_x), int(chunk_y)), (int(local_tile_x), int(local_tile_y))

    # This one is faster but more complicated and works only when values are pow of 2
    def world_to_tile_bit(self, world_x, world_y):
        tile_shift = 4  # 16 -> 2^4
        chunk_shift = 5  # 32 -> 2^5 -> 100000
        chunk_bitmask = self.chunk_width - 1  # 32 = 100000, 31 = 11111, so we take 5 bits because otherwise you would go over chunksize

        global_tile_x = int(world_x) >> tile_shift
        global_tile_y = int(world_y) >> tile_shift

        chunk_x = global_tile_x >> chunk_shift
        chunk_y = global_tile_y >> chunk_shift

        # Bitmask works like modulo
        local_tile_x = global_tile_x & chunk_bitmask
        local_tile_y = global_tile_y & chunk_bitmask

        return (chunk_x, chunk_y), (local_tile_x, local_tile_y)

    def get_chunk_pixel_size(self):
        return self.chunk_width * TILE_SIZE, self.chunk_height * TILE_SIZE

    def get_chunk_pixel_pos(self, chunk_x, chunk_y):
        world_pos = self.get_chunk_world_pos(chunk_x, chunk_y)
        return world_pos[0] * TILE_SIZE, world_pos[1] * TILE_SIZE

    def get_chunk_world_pos(self, chunk_x, chunk_y):
        return int(chunk_x * self.chunk_width), int(chunk_y * self.chunk_height)

    def try_get_chunk(self, chunk_x, chunk_y) -> Chunk | None:
        return self.chunks.get((chunk_x, chunk_y))

    def destroy_tile(self, world_x, world_y):
        self._set_tile(world_x, world_y, TileType.EMPTY)

    def create_tile(self, world_x, world_y):
        self._set_tile(world_x, world_y, TileType.WALL)

    def update(self, camera, delta_time):
        self._get_active_chunks_range(camera)

        for chunk_x in self.active_chunk_range_x:
            for chunk_y in self.active_chunk_range_y:
                self._create_chunk(chunk_x, chunk_y)

        for chunk_pos in list(self.chunks):
            if chunk_pos[0] not in self.active_chunk_range_x or chunk_pos[1] not in self.active_chunk_range_y:
                unload_render_texture(self.chunks[chunk_pos].chunk_texture)
                del self.chunks[chunk_pos]

        for chunk in self.chunks.values():
            chunk.draw_texture()

    def debug(self, camera, font):
        for x in self.active_chunk_range_x:
            for y in self.active_chunk_range_y:
                pixel_x, pixel_y = self.get_chunk_pixel_pos(x, y)
                pixel_width, pixel_height = self.get_chunk_pixel_size()
                chunk_rect = Rectangle(pixel_x, pixel_y, pixel_width, pixel_height)
                draw_rectangle_lines_ex(chunk_rect, 1, RED)
                draw_text(f'{x, y}', int(pixel_x + 25), int(pixel_y + 25), 32, RED)

        mouse_world = get_screen_to_world_2d(get_mouse_position(), camera.camera)
        (chunk_x, chunk_y), (tile_x, tile_y) = self.world_to_tile(mouse_world.x, mouse_world.y)
        chunk = self.try_get_chunk(chunk_x, chunk_y)
        world_tile_x, world_tile_y = self.world_to_world_tile(mouse_world.x, mouse_world.y)
        tile_type = TileType(chunk.tiles[tile_x, tile_y]).name if chunk else ''

        texts = [
            f'Pos: {mouse_world.x:.0f}, {mouse_world.y:.0f}',
            f'Chunk: {chunk_x}, {chunk_y}',
            f'Tile: {tile_x}, {tile_y}',
            f'World Tile: {world_tile_x:.0f}, {world_tile_y:.0f}',
            f'Type: {tile_type}',
            f'Neighbours: {chunk.tile_neighbours_count(tile_x, tile_y) if chunk else ''}',
        ]
        debug_tooltip(mouse_world.x + 12, mouse_world.y + 12, texts, font)

        # Draw indicator
        world_tile_x, world_tile_y = self.world_to_world_tile(mouse_world.x, mouse_world.y)
        pixel_tile_x, pixel_tile_y = world_tile_x * TILE_SIZE, world_tile_y * TILE_SIZE
        draw_rectangle_lines_ex(Rectangle(pixel_tile_x, pixel_tile_y, TILE_SIZE, TILE_SIZE), 2, RED)

    def draw(self, debug, camera, font):
        for chunk in self.chunks.values():
            chunk.draw()

        if not debug: return
        self.debug(camera, font)