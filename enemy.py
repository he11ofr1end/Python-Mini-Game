import math
import pygame as pg
from animated_sprite import AnimatedSprite


class Enemy(AnimatedSprite):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, 'enemy')
        self.health = 100
        self.max_health = 100
        self.speed = 0.003
        self.size = 0.3
        self.state = 'idle'
        self.attack_range = 1.0
        self.attack_damage = 10
        self.attack_cooldown = 1000
        self.last_attack_time = 0

    def update(self):
        if self.state == 'dead':
            return

        dx = self.game.player.x - self.x
        dy = self.game.player.y - self.y
        dist = math.hypot(dx, dy)

        if dist < self.attack_range:
            self.state = 'attack'
            self.attack_player()
        elif dist < 15:
            self.state = 'chase'
            self.chase_player(dx, dy, dist)
        else:
            self.state = 'idle'

        if self.state in ['chase', 'attack']:
            self.update_animation()

        angle = math.atan2(dy, dx)
        self.update_direction(angle)

    def chase_player(self, dx, dy, dist):
        move_x = (dx / dist) * self.speed * self.game.delta_time
        move_y = (dy / dist) * self.speed * self.game.delta_time

        next_x = self.x + move_x
        next_y = self.y + move_y

        can_move_x = (int(next_x), int(self.y)) not in self.game.map.world_map
        can_move_y = (int(self.x), int(next_y)) not in self.game.map.world_map

        if can_move_x or can_move_y:
            for other in self.game.enemies:
                if other is self or other.state == 'dead':
                    continue

                if can_move_x:
                    test_dist_x = math.hypot(next_x - other.x, self.y - other.y)
                    if test_dist_x < (self.size + other.size):
                        can_move_x = False

                if can_move_y:
                    test_dist_y = math.hypot(self.x - other.x, next_y - other.y)
                    if test_dist_y < (self.size + other.size):
                        can_move_y = False

        if can_move_x:
            self.x = next_x
        if can_move_y:
            self.y = next_y

    def attack_player(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_attack_time > self.attack_cooldown:
            if hasattr(self.game.player, 'take_damage'):
                self.game.player.take_damage(self.attack_damage)
            self.last_attack_time = current_time

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.state = 'dead'
            if hasattr(self.game, 'score'):
                self.game.score += 10

    def draw(self):
        if self.state == 'dead':
            return
        super().draw()

        camera = self.game.camera
        screen_x, screen_y = camera.world_to_screen(self.x, self.y)
        bar_width = 40
        bar_height = 4
        health_ratio = self.health / self.max_health

        pg.draw.rect(self.game.screen, (100, 0, 0),
                     (screen_x - bar_width//2, screen_y - 35, bar_width, bar_height))
        pg.draw.rect(self.game.screen, (255, 0, 0),
                     (screen_x - bar_width//2, screen_y - 35, bar_width * health_ratio, bar_height))
