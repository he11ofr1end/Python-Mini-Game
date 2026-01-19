import pygame as pg
import os


class SpriteManager:
    def __init__(self):
        self.sprites = {}
        self.use_images = True
        self.zombie_frames = {}
        self.load_sprites()

    def load_sprites(self):
        if self.use_images and os.path.exists('sprites'):
            try:
                self.load_sprite_images()
                print("Sprites loaded")
            except Exception as e:
                print(f"Error: {e}")
                self.load_procedural_sprites()
        else:
            self.load_procedural_sprites()

    def load_procedural_sprites(self):
        self.sprites['player'] = self.create_player_sprites()
        self.sprites['enemy'] = self.create_enemy_sprites()
        self.sprites['muzzle_flash'] = self.create_muzzle_flash()
        self.sprites['bullet'] = self.create_bullet()

    def load_sprite_images(self):
        player_loaded = False
        self.sprites['player'] = {}
        for direction in ['up', 'down', 'left', 'right']:
            self.sprites['player'][direction] = []
            for frame in range(4):
                img_path = f'sprites/player/{direction}_{frame}.png'
                if os.path.exists(img_path):
                    sprite = pg.image.load(img_path).convert_alpha()
                    self.sprites['player'][direction].append(sprite)
                    player_loaded = True

        if not player_loaded:
            self.sprites['player'] = self.create_player_sprites()

        enemy_loaded = False
        self.sprites['enemy'] = {}
        for direction in ['up', 'down', 'left', 'right']:
            self.sprites['enemy'][direction] = []
            for frame in range(4):
                img_path = f'sprites/enemy/{direction}_{frame}.png'
                if os.path.exists(img_path):
                    sprite = pg.image.load(img_path).convert_alpha()
                    self.sprites['enemy'][direction].append(sprite)
                    enemy_loaded = True

        if not enemy_loaded:
            self.sprites['enemy'] = self.create_enemy_sprites()

        if os.path.exists('sprites/muzzle_flash.png'):
            self.sprites['muzzle_flash'] = pg.image.load('sprites/muzzle_flash.png').convert_alpha()
        else:
            self.sprites['muzzle_flash'] = self.create_muzzle_flash()

        if os.path.exists('sprites/bullet.png'):
            self.sprites['bullet'] = pg.image.load('sprites/bullet.png').convert_alpha()
        else:
            self.sprites['bullet'] = self.create_bullet()

        self.load_zombie_sprites()
        self.load_swat_sprites()
        self.load_bullet_sprites()

    def load_bullet_sprites(self):
        bullet_path = 'bullets'
        if not os.path.exists(bullet_path):
            return

        img_path = f'{bullet_path}/All_Fire_Bullet_Pixel_16x16_00.png'
        if not os.path.exists(img_path):
            return

        sheet = pg.image.load(img_path).convert_alpha()

        bullet_frames = []
        start_x = 0
        start_y = 32

        for i in range(8):
            bullet_sprite = pg.Surface((16, 16), pg.SRCALPHA)
            bullet_sprite.blit(sheet, (0, 0), (start_x + i * 16, start_y, 16, 16))
            scaled_bullet = pg.transform.scale(bullet_sprite, (24, 24))
            bullet_frames.append(scaled_bullet)

        if bullet_frames:
            self.sprites['bullet'] = bullet_frames
            self.sprites['bullet_animated'] = True
        else:
            self.sprites['bullet_animated'] = False

    def load_swat_sprites(self):
        swat_path = 'sprites/SWAT/Soldier_1'
        if not os.path.exists(swat_path):
            return

        walk_sheet = None
        if os.path.exists(f'{swat_path}/Walk.png'):
            walk_sheet = pg.image.load(f'{swat_path}/Walk.png').convert_alpha()

        walk_frames = self.extract_frames(walk_sheet, 7) if walk_sheet else []

        self.sprites['player'] = {}

        if walk_frames:
            self.sprites['player']['right'] = walk_frames[:4]
            self.sprites['player']['left'] = [pg.transform.flip(f, True, False) for f in walk_frames[:4]]
            self.sprites['player']['up'] = walk_frames[:4]
            self.sprites['player']['down'] = walk_frames[:4]

    def load_zombie_sprites(self):
        img_path = 'sprites/enemy.png'
        if not os.path.exists(img_path):
            return

        img = pg.image.load(img_path).convert_alpha()
        img = pg.transform.scale(img, (85, 85))
        img_flipped = pg.transform.flip(img, True, False)

        self.sprites['enemy'] = {}
        self.sprites['enemy']['right'] = [img, img, img, img]
        self.sprites['enemy']['left'] = [img_flipped, img_flipped, img_flipped, img_flipped]
        self.sprites['enemy']['up'] = [img, img, img, img]
        self.sprites['enemy']['down'] = [img, img, img, img]

        self.zombie_frames['attack'] = []
        self.zombie_frames['idle'] = []

    def extract_frames(self, sprite_sheet, num_frames):
        if sprite_sheet is None:
            return []

        sheet_width = sprite_sheet.get_width()
        sheet_height = sprite_sheet.get_height()
        frame_width = sheet_width // num_frames

        frames = []
        for i in range(num_frames):
            frame = pg.Surface((frame_width, sheet_height), pg.SRCALPHA)
            frame.blit(sprite_sheet, (0, 0), (i * frame_width, 0, frame_width, sheet_height))
            scaled_frame = pg.transform.scale(frame, (128, 128))
            frames.append(scaled_frame)

        return frames

    def create_player_sprites(self):
        sprites = {}
        for direction in ['up', 'down', 'left', 'right']:
            sprites[direction] = []
            for frame in range(4):
                sprite = pg.Surface((48, 48), pg.SRCALPHA)
                pg.draw.circle(sprite, (0, 200, 0), (24, 24), 20)
                if direction == 'up':
                    pg.draw.circle(sprite, (0, 150, 0), (24, 15), 8)
                elif direction == 'down':
                    pg.draw.circle(sprite, (0, 150, 0), (24, 33), 8)
                elif direction == 'left':
                    pg.draw.circle(sprite, (0, 150, 0), (15, 24), 8)
                elif direction == 'right':
                    pg.draw.circle(sprite, (0, 150, 0), (33, 24), 8)
                offset = 2 if frame % 2 == 0 else -2
                pg.draw.circle(sprite, (0, 255, 0), (24, 24 + offset), 5)
                sprites[direction].append(sprite)
        return sprites

    def create_enemy_sprites(self):
        sprites = {}
        for direction in ['up', 'down', 'left', 'right']:
            sprites[direction] = []
            for frame in range(4):
                sprite = pg.Surface((48, 48), pg.SRCALPHA)
                pg.draw.circle(sprite, (200, 0, 0), (24, 24), 20)
                pg.draw.circle(sprite, (255, 255, 0), (18, 20), 4)
                pg.draw.circle(sprite, (255, 255, 0), (30, 20), 4)
                offset = 3 if frame % 2 == 0 else -3
                pg.draw.rect(sprite, (150, 0, 0), (10, 35 + offset, 28, 10))
                sprites[direction].append(sprite)
        return sprites

    def create_muzzle_flash(self):
        sprite = pg.Surface((32, 32), pg.SRCALPHA)
        pg.draw.circle(sprite, (255, 255, 0), (16, 16), 12)
        pg.draw.circle(sprite, (255, 200, 0), (16, 16), 8)
        return sprite

    def create_bullet(self):
        sprite = pg.Surface((8, 8), pg.SRCALPHA)
        pg.draw.circle(sprite, (255, 255, 0), (4, 4), 4)
        return sprite

    def get_sprite(self, sprite_type, direction='down', frame=0):
        if sprite_type in ['player', 'enemy']:
            return self.sprites[sprite_type][direction][frame]
        elif sprite_type == 'bullet' and self.sprites.get('bullet_animated', False):
            return self.sprites['bullet'][frame % len(self.sprites['bullet'])]
        else:
            return self.sprites[sprite_type]
