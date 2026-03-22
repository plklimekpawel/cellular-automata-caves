from settings import *
from scipy.ndimage import convolve

def noise_wall(x, y, threshold=0.45):
    # 0xFFFFFFFF -> 32 bit mask
    # * and + is always vectorized in numpy
    h = (x * 374761393 + y * 668265263 + SEED) & 0xFFFFFFFF
    h = (h ^ (h >> 13)) * 1274126177
    h = h & 0xFFFFFFFF
    return (h / 2**32) < threshold

class Chunk:
    def __init__(self, width, height, chunk_pos, world):
        self.world = world

        self.width = width
        self.height = height
        self.chunk_pos = chunk_pos

        self._padded_tiles = None
        self.tiles = None
        self.dirty_flag = True

        self.chunk_texture = load_render_texture(self.width * TILE_SIZE, self.height * TILE_SIZE)
        self._generate_chunk()

    def _generate_chunk(self):
        padding = CHUNK_PADDING

        xs = np.arange(-padding, self.width + padding)[:, None] + self.chunk_pos[0] * self.width
        ys = np.arange(-padding, self.height + padding)[None, :] + self.chunk_pos[1] * self.height
        tiles = noise_wall(xs, ys, WALL_THRESHOLD).astype(np.uint8)

        for _ in range(SMOOTHING_AMOUNT):
            tiles = self._smooth_step(tiles.astype(np.uint8))

        self._padded_tiles = tiles
        self.tiles = tiles[padding:-padding, padding:-padding]
        self.draw_texture()

    def _smooth_step(self, tiles):
        neighbors_count, solid_mask = self._neighbours_count_array(tiles)
                 # where(condition, value_if_true, value_if_false)
        new_tiles = np.where(solid_mask, neighbors_count >= 4, neighbors_count >= 5)
        result = np.where(new_tiles, TileType.WALL, TileType.EMPTY)
        return result

    def _neighbours_count_array(self, tiles):
        solid_mask = np.where(tiles >= TileType.WALL, TileType.WALL, TileType.EMPTY).astype(np.uint8)
        neighbors_count = convolve(solid_mask, NEIGHBOUR_KERNEL, mode='constant', cval=0)
        return neighbors_count, solid_mask

    def tile_neighbours_count(self, tile_x, tile_y):
        padded = self._padded_tiles
        x = tile_x + CHUNK_PADDING  # Offseting padding
        y = tile_y + CHUNK_PADDING

        neighbourhood = padded[x - 1:x + 2, y - 1:y + 2]

        center_tile = padded[x, y] >= TileType.WALL
        count = np.count_nonzero(neighbourhood)
        return count - center_tile

    def set_dirty(self):
        self.dirty_flag = True

    def draw_texture(self):
        if not self.dirty_flag:
            return
        walls = np.argwhere(self.tiles != TileType.EMPTY)

        begin_texture_mode(self.chunk_texture)
        clear_background(BLANK)
        for x, y in walls:
            pixel_x, pixel_y = int(x * TILE_SIZE), int(y * TILE_SIZE)
            draw_rectangle(pixel_x, pixel_y, TILE_SIZE, TILE_SIZE, DARK_GRAY)
        end_texture_mode()
        self.dirty_flag = False

    def draw(self):
        pixel_x = self.chunk_pos[0] * self.width * TILE_SIZE
        pixel_y = self.chunk_pos[1] * self.height * TILE_SIZE
        draw_texture_rec(self.chunk_texture.texture, Rectangle(0, 0, self.chunk_texture.texture.width, -self.chunk_texture.texture.height), Vector2(pixel_x, pixel_y), WHITE)