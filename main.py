import sys
import pygame as pg
import os
import random
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
        self.init_music()
        self.game_state = 'playing'
        self.slow_motion = False
        self.slow_motion_end_time = 0
        self.slow_motion_factor = 0.3
        self.new_game()

    def init_music(self):
        pg.mixer.init()
        music_path = 'sounds/background.mp3'
        if os.path.exists(music_path):
            pg.mixer.music.load(music_path)
            pg.mixer.music.set_volume(0.6)
            pg.mixer.music.play(-1)

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.camera = Camera(self)
        self.weapon = Weapon(self)
        self.ui_renderer = UIRenderer(self)
        num_enemies = random.randint(10, 25)
        free_positions = self.map.get_free_positions()
        random.shuffle(free_positions)
        self.enemies = [Enemy(self, pos[0], pos[1]) for pos in free_positions[:num_enemies]]
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
