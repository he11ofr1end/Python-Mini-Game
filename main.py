import sys
import pygame as pg
import os

from map import Map
from player import Player
from camera import Camera
from sprite_manager import SpriteManager
from enemy import Enemy
from weapon import Weapon
from ui_renderer import UIRenderer
from src.settings import RES, FPS


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        pg.mouse.set_visible(False)
        self.sprite_manager = SpriteManager()
        self.game_state = 'playing'
        self.slow_motion = False
        self.slow_motion_end_time = 0
        self.slow_motion_factor = 0.3
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.camera = Camera(self)
        self.weapon = Weapon(self)
        self.ui_renderer = UIRenderer(self)
        self.enemies = [
            Enemy(self, 5, 3), Enemy(self, 8, 3), Enemy(self, 11, 3), Enemy(self, 14, 3),
            Enemy(self, 17, 3), Enemy(self, 20, 3), Enemy(self, 23, 3), Enemy(self, 26, 3),
            Enemy(self, 5, 6), Enemy(self, 10, 6), Enemy(self, 15, 6), Enemy(self, 20, 6),
            Enemy(self, 25, 6), Enemy(self, 30, 6), Enemy(self, 35, 6), Enemy(self, 5, 9),
            Enemy(self, 10, 9), Enemy(self, 15, 9), Enemy(self, 20, 9), Enemy(self, 25, 9),
            Enemy(self, 30, 9), Enemy(self, 35, 9), Enemy(self, 5, 12), Enemy(self, 10, 12),
            Enemy(self, 15, 12), Enemy(self, 20, 12), Enemy(self, 25, 12), Enemy(self, 30, 12),
            Enemy(self, 5, 15), Enemy(self, 10, 15), Enemy(self, 15, 15), Enemy(self, 20, 15),
            Enemy(self, 25, 15), Enemy(self, 30, 15), Enemy(self, 5, 18), Enemy(self, 10, 18),
            Enemy(self, 15, 18), Enemy(self, 20, 18), Enemy(self, 25, 18), Enemy(self, 30, 18),
        ]
        self.bullets = []
        self.score = 0
        self.game_state = 'playing'

    def game_over(self):
        self.game_state = 'game_over'

    def update(self):
        if self.game_state == 'playing':
            self.player.update()
            self.camera.update()
            self.weapon.update()

            for enemy in self.enemies:
                enemy.update()

            for bullet in self.bullets[:]:
                bullet.update()
                if not bullet.alive:
                    self.bullets.remove(bullet)

            if all(e.state == 'dead' for e in self.enemies):
                self.game_state = 'victory'

        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)

        if self.slow_motion:
            if pg.time.get_ticks() > self.slow_motion_end_time:
                self.slow_motion = False
            else:
                self.delta_time *= self.slow_motion_factor

        pg.display.set_caption(f'{self.clock.get_fps():.1f}')

    def draw(self):
        self.screen.fill('black')

        if self.game_state == 'playing':
            self.map.draw()

            for enemy in sorted(self.enemies, key=lambda e: e.y):
                enemy.draw()

            for bullet in self.bullets:
                bullet.draw()

            self.player.draw()
            self.weapon.draw()

        self.ui_renderer.render()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

            if self.game_state == 'playing':
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    self.weapon.fire()
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    self.weapon.fire()
                if event.type == pg.KEYDOWN and event.key == pg.K_k:
                    self.slow_motion = True
                    self.slow_motion_end_time = pg.time.get_ticks() + 10000
                if event.type == pg.KEYDOWN and event.key == pg.K_f:
                    self.weapon.toggle_rapid_fire()

            if self.game_state in ['game_over', 'victory']:
                if event.type == pg.KEYDOWN and event.key == pg.K_r:
                    self.new_game()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
