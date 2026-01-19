import math
import pygame as pg
from animated_sprite import AnimatedSprite
from src.settings import PLAYER_POS, PLAYER_ANGLE, PLAYER_SPEED, PLAYER_ROT_SPEED


class Player(AnimatedSprite):
    def __init__(self, game):
        super().__init__(game, *PLAYER_POS, 'player')
        self.angle = PLAYER_ANGLE
        self.health = 100
        self.max_health = 100
        self.is_alive = True

    def movement(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        camera = self.game.camera
        screen_x, screen_y = camera.world_to_screen(self.x, self.y)
        dx_to_mouse = mouse_x - screen_x
        dy_to_mouse = mouse_y - screen_y
        self.angle = math.atan2(dy_to_mouse, dx_to_mouse)

        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time

        keys = pg.key.get_pressed()

        if keys[pg.K_w]:
            dy -= speed
        if keys[pg.K_s]:
            dy += speed
        if keys[pg.K_a]:
            dx -= speed
        if keys[pg.K_d]:
            dx += speed

        self.check_wall_collision(dx, dy)
        self.update_direction(self.angle)

        if dx != 0 or dy != 0:
            self.update_animation()

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        margin = 0.4

        next_x = self.x + dx
        can_move_x = True
        if not self.check_wall(int(next_x + margin), int(self.y)):
            can_move_x = False
        if not self.check_wall(int(next_x - margin), int(self.y)):
            can_move_x = False
        if not self.check_wall(int(next_x + margin), int(self.y + margin)):
            can_move_x = False
        if not self.check_wall(int(next_x + margin), int(self.y - margin)):
            can_move_x = False
        if not self.check_wall(int(next_x - margin), int(self.y + margin)):
            can_move_x = False
        if not self.check_wall(int(next_x - margin), int(self.y - margin)):
            can_move_x = False

        next_y = self.y + dy
        can_move_y = True
        if not self.check_wall(int(self.x), int(next_y + margin)):
            can_move_y = False
        if not self.check_wall(int(self.x), int(next_y - margin)):
            can_move_y = False
        if not self.check_wall(int(self.x + margin), int(next_y + margin)):
            can_move_y = False
        if not self.check_wall(int(self.x + margin), int(next_y - margin)):
            can_move_y = False
        if not self.check_wall(int(self.x - margin), int(next_y + margin)):
            can_move_y = False
        if not self.check_wall(int(self.x - margin), int(next_y - margin)):
            can_move_y = False

        if can_move_x:
            self.x = next_x
        if can_move_y:
            self.y = next_y

    def take_damage(self, damage):
        if not self.is_alive:
            return

        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
            if hasattr(self.game, 'game_over'):
                self.game.game_over()

    def update(self):
        if self.is_alive:
            self.movement()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
