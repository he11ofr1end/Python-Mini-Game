import math
import pygame as pg


class AnimatedSprite:
    def __init__(self, game, x, y, sprite_type):
        self.game = game
        self.x = x
        self.y = y
        self.sprite_type = sprite_type
        self.direction = 'down'
        self.frame = 0
        self.animation_speed = 200
        self.last_frame_time = 0

    def update_animation(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_frame_time > self.animation_speed:
            self.frame = (self.frame + 1) % 4
            self.last_frame_time = current_time

    def update_direction(self, angle):
        if -math.pi/4 < angle <= math.pi/4:
            self.direction = 'right'
        elif math.pi/4 < angle <= 3*math.pi/4:
            self.direction = 'down'
        elif -3*math.pi/4 < angle <= -math.pi/4:
            self.direction = 'up'
        else:
            self.direction = 'left'

    def draw(self):
        camera = self.game.camera
        screen_x, screen_y = camera.world_to_screen(self.x, self.y)

        sprite = self.game.sprite_manager.get_sprite(
            self.sprite_type, self.direction, self.frame
        )

        rect = sprite.get_rect(midbottom=(int(screen_x), int(screen_y)))
        self.game.screen.blit(sprite, rect)
