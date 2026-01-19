import pygame as pg
from src.settings import WIDTH, HEIGHT


class UIRenderer:
    def __init__(self, game):
        self.game = game
        self.font = pg.font.Font(None, 36)
        self.large_font = pg.font.Font(None, 72)

    def render(self):
        if self.game.game_state == 'playing':
            self.render_hud()
        elif self.game.game_state == 'game_over':
            self.render_game_over()
        elif self.game.game_state == 'victory':
            self.render_victory()

    def render_hud(self):
        health_text = self.font.render(f"Health: {self.game.player.health}", True, (255, 0, 0))
        self.game.screen.blit(health_text, (10, 10))

        bar_width = 200
        bar_height = 20
        health_ratio = self.game.player.health / self.game.player.max_health

        pg.draw.rect(self.game.screen, (100, 0, 0), (10, 50, bar_width, bar_height))
        pg.draw.rect(self.game.screen, (255, 0, 0), (10, 50, bar_width * health_ratio, bar_height))
        pg.draw.rect(self.game.screen, (255, 255, 255), (10, 50, bar_width, bar_height), 2)

        score_text = self.font.render(f"Score: {self.game.score}", True, (255, 255, 255))
        self.game.screen.blit(score_text, (WIDTH - 200, 10))

        alive_enemies = sum(1 for e in self.game.enemies if e.state != 'dead')
        enemy_text = self.font.render(f"Enemies: {alive_enemies}", True, (255, 255, 255))
        self.game.screen.blit(enemy_text, (WIDTH - 200, 50))

        hint_k = self.font.render("K - Slow Motion", True, (200, 200, 200))
        self.game.screen.blit(hint_k, (10, HEIGHT - 60))

        hint_f = self.font.render("F - Rapid Fire", True, (200, 200, 200))
        self.game.screen.blit(hint_f, (10, HEIGHT - 30))

        if self.game.slow_motion:
            slow_text = self.font.render("SLOW MOTION", True, (0, 255, 255))
            slow_rect = slow_text.get_rect(center=(WIDTH // 2, 30))
            self.game.screen.blit(slow_text, slow_rect)

        if self.game.weapon.rapid_fire:
            rapid_text = self.font.render("RAPID FIRE", True, (255, 255, 0))
            rapid_rect = rapid_text.get_rect(center=(WIDTH // 2, 60))
            self.game.screen.blit(rapid_text, rapid_rect)

        mouse_x, mouse_y = pg.mouse.get_pos()

        color = (0, 255, 0)
        gap = 3
        length = 10
        thickness = 2

        pg.draw.line(self.game.screen, color,
                     (mouse_x, mouse_y - gap - length),
                     (mouse_x, mouse_y - gap), thickness)
        pg.draw.line(self.game.screen, color,
                     (mouse_x, mouse_y + gap),
                     (mouse_x, mouse_y + gap + length), thickness)
        pg.draw.line(self.game.screen, color,
                     (mouse_x - gap - length, mouse_y),
                     (mouse_x - gap, mouse_y), thickness)
        pg.draw.line(self.game.screen, color,
                     (mouse_x + gap, mouse_y),
                     (mouse_x + gap + length, mouse_y), thickness)

    def render_game_over(self):
        overlay = pg.Surface((WIDTH, HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)
        self.game.screen.blit(overlay, (0, 0))

        text = self.large_font.render("GAME OVER", True, (255, 0, 0))
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.game.screen.blit(text, rect)

        score_text = self.font.render(f"Final Score: {self.game.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        self.game.screen.blit(score_text, score_rect)

        restart_text = self.font.render("Press R to Restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
        self.game.screen.blit(restart_text, restart_rect)

    def render_victory(self):
        overlay = pg.Surface((WIDTH, HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)
        self.game.screen.blit(overlay, (0, 0))

        text = self.large_font.render("VICTORY!", True, (0, 255, 0))
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.game.screen.blit(text, rect)

        score_text = self.font.render(f"Score: {self.game.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        self.game.screen.blit(score_text, score_rect)

        restart_text = self.font.render("Press R to Play Again", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
        self.game.screen.blit(restart_text, restart_rect)
