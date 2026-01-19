import math
import pygame as pg
from bullet import Bullet


class Weapon:
    def __init__(self, game):
        self.game = game
        self.damage = 25
        self.normal_cooldown = 250
        self.rapid_cooldown = 50
        self.fire_cooldown = self.normal_cooldown
        self.last_fire_time = 0
        self.is_firing = False
        self.muzzle_flash_duration = 100
        self.rapid_fire = False
        self.rapid_fire_end_time = 0

    def fire(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_fire_time < self.fire_cooldown:
            return

        self.last_fire_time = current_time
        self.is_firing = True

        player = self.game.player

        spawn_distance = 0.5
        bullet_x = player.x + spawn_distance * math.cos(player.angle)
        bullet_y = player.y + spawn_distance * math.sin(player.angle)

        bullet = Bullet(self.game, bullet_x, bullet_y, player.angle, self.damage)
        if hasattr(self.game, 'bullets'):
            self.game.bullets.append(bullet)

    def toggle_rapid_fire(self):
        self.rapid_fire = True
        self.rapid_fire_end_time = pg.time.get_ticks() + 5000
        self.fire_cooldown = self.rapid_cooldown

    def update(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_fire_time > self.muzzle_flash_duration:
            self.is_firing = False

        if self.rapid_fire and current_time > self.rapid_fire_end_time:
            self.rapid_fire = False
            self.fire_cooldown = self.normal_cooldown

    def draw(self):
        if not self.is_firing:
            return

        player = self.game.player
        camera = self.game.camera
        screen_x, screen_y = camera.world_to_screen(player.x, player.y)

        flash_dist = 30
        flash_x = screen_x + flash_dist * math.cos(player.angle)
        flash_y = screen_y - 40 + flash_dist * math.sin(player.angle)

        sprite = self.game.sprite_manager.get_sprite('muzzle_flash')
        rect = sprite.get_rect(center=(int(flash_x), int(flash_y)))
        self.game.screen.blit(sprite, rect)
