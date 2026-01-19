import pygame as pg

from maps_collection import choose_random_map, map_collection_
from src.settings import TILE_SIZE, CAMERA_WIDTH, CAMERA_HEIGHT, WIDTH, HEIGHT

_ = False

# Карта подземелья 40x25
mini_map = choose_random_map(map_collection_)


class Map:
    def __init__(self, game):
        self.game = game
        self.mini_map = mini_map
        self.world_map = {}
        self.get_map()
        self.load_textures()

    def get_map(self):
        for y, row in enumerate(mini_map):
            for x, value in enumerate(row):
                if value:
                    self.world_map[(x, y)] = value

    def load_textures(self):
        import os
        tileset_path = 'map/0x72_DungeonTilesetII_v1.7'

        # Попробовать загрузить текстуры из DungeonTilesetII
        if os.path.exists(tileset_path):
            try:
                # Загрузить атлас стен
                walls_atlas = pg.image.load(f'{tileset_path}/atlas_walls_low-16x16.png').convert_alpha()
                # Вырезать одну текстуру стены (кирпичная стена - позиция 0,0)
                wall_tile = pg.Surface((16, 16), pg.SRCALPHA)
                wall_tile.blit(walls_atlas, (0, 0), (0, 0, 16, 16))
                # Масштабировать до TILE_SIZE
                self.wall_sprite = pg.transform.scale(wall_tile, (TILE_SIZE, TILE_SIZE))

                # Загрузить атлас пола
                floor_atlas = pg.image.load(f'{tileset_path}/atlas_floor-16x16.png').convert_alpha()
                # Вырезать текстуру пола (темный пол - позиция 16, 0)
                floor_tile = pg.Surface((16, 16), pg.SRCALPHA)
                floor_tile.blit(floor_atlas, (0, 0), (16, 0, 16, 16))
                # Масштабировать до TILE_SIZE
                self.floor_sprite = pg.transform.scale(floor_tile, (TILE_SIZE, TILE_SIZE))

                print("Текстуры DungeonTilesetII загружены!")
                return
            except Exception as e:
                print(f"Ошибка загрузки текстур: {e}")

        # Fallback - процедурные текстуры
        # Создать спрайт стены (64x64)
        self.wall_sprite = pg.Surface((TILE_SIZE, TILE_SIZE))
        # Кирпичная текстура
        for y in range(0, TILE_SIZE, 16):
            for x in range(0, TILE_SIZE, 16):
                color = (80, 80, 80) if (x + y) % 32 == 0 else (100, 100, 100)
                pg.draw.rect(self.wall_sprite, color, (x, y, 16, 16))
        # Добавить границу
        pg.draw.rect(self.wall_sprite, (60, 60, 60), (0, 0, TILE_SIZE, TILE_SIZE), 2)

        # Пол
        self.floor_sprite = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.floor_sprite.fill((40, 40, 40))
        # Линии сетки
        pg.draw.line(self.floor_sprite, (50, 50, 50), (0, 0), (TILE_SIZE, 0))
        pg.draw.line(self.floor_sprite, (50, 50, 50), (0, 0), (0, TILE_SIZE))

    def draw(self):
        camera = self.game.camera

        # Определить видимую область
        start_x = max(0, int(camera.x // TILE_SIZE) - 1)
        start_y = max(0, int(camera.y // TILE_SIZE) - 1)
        end_x = min(40, start_x + CAMERA_WIDTH + 2)  # Новая карта 40x25
        end_y = min(25, start_y + CAMERA_HEIGHT + 2)

        # Сначала рисовать пол везде
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                screen_x, screen_y = camera.apply(x, y)
                if -TILE_SIZE < screen_x < WIDTH and -TILE_SIZE < screen_y < HEIGHT:
                    self.game.screen.blit(self.floor_sprite, (screen_x, screen_y))

        # Потом стены
        for (x, y), value in self.world_map.items():
            if start_x <= x < end_x and start_y <= y < end_y:
                screen_x, screen_y = camera.apply(x, y)
                if -TILE_SIZE < screen_x < WIDTH and -TILE_SIZE < screen_y < HEIGHT:
                    self.game.screen.blit(self.wall_sprite, (screen_x, screen_y))
