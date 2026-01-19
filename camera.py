from src.settings import TILE_SIZE, CAMERA_OFFSET_X, CAMERA_OFFSET_Y


class Camera:
    def __init__(self, game):
        self.game = game
        self.x = 0
        self.y = 0

    def update(self):
        # Центрировать камеру на игроке
        player = self.game.player
        self.x = player.x * TILE_SIZE - CAMERA_OFFSET_X
        self.y = player.y * TILE_SIZE - CAMERA_OFFSET_Y

    def apply(self, x, y):
        # Преобразовать мировые координаты (тайлы) в экранные
        screen_x = x * TILE_SIZE - self.x
        screen_y = y * TILE_SIZE - self.y
        return screen_x, screen_y

    def world_to_screen(self, world_x, world_y):
        # Для объектов с float координатами
        screen_x = world_x * TILE_SIZE - self.x
        screen_y = world_y * TILE_SIZE - self.y
        return screen_x, screen_y
