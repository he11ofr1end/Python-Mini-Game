import math
import pygame as pg


class Bullet:
    def __init__(self, game, x, y, angle, damage=25):
        self.game = game
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 0.020
        self.damage = damage
        self.alive = True
        self.lifetime = 2000
        self.spawn_time = pg.time.get_ticks()
        self.frame = 0
        self.animation_speed = 50
        self.last_frame_time = pg.time.get_ticks()

    def update(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_frame_time > self.animation_speed:
            self.frame += 1
            self.last_frame_time = current_time

        self.x += math.cos(self.angle) * self.speed * self.game.delta_time
        self.y += math.sin(self.angle) * self.speed * self.game.delta_time

        if (int(self.x), int(self.y)) in self.game.map.world_map:
            self.alive = False
            return

        if hasattr(self.game, 'enemies'):
            for enemy in self.game.enemies:
                if enemy.state == 'dead':
                    continue
                dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
                if dist < 0.4:
                    enemy.take_damage(self.damage)
                    self.alive = False
                    return

        if pg.time.get_ticks() - self.spawn_time > self.lifetime:
            self.alive = False

    def draw(self):
        camera = self.game.camera
        screen_x, screen_y = camera.world_to_screen(self.x, self.y)
        screen_y -= 50

        sprite = self.game.sprite_manager.get_sprite('bullet', frame=self.frame)
        rotated_sprite = pg.transform.rotate(sprite, -math.degrees(self.angle))
        rect = rotated_sprite.get_rect(center=(int(screen_x), int(screen_y)))
        self.game.screen.blit(rotated_sprite, rect)
