# Game settings
import math

RES = WIDTH, HEIGHT = 1600, 900
FPS = 60

# Player POSITION, ANGLE, SPEED, ROTATION SPEED
PLAYER_POS = (2, 10)  # Новая стартовая позиция для карты подземелья
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
PLAYER_ROT_SPEED = 0.002

# Camera settings
TILE_SIZE = 64  # Размер тайла в пикселях (вместо 30)
CAMERA_WIDTH = 25  # Сколько тайлов видно по ширине
CAMERA_HEIGHT = 14  # Сколько тайлов видно по высоте
CAMERA_OFFSET_X = WIDTH // 2  # Центр камеры по X
CAMERA_OFFSET_Y = HEIGHT // 2  # Центр камеры по Y

# RAYCASTING (больше не используется)
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20