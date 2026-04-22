import pygame

from core.game_scene import GameScene


class GameWorld(GameScene):
    """World inicial temporário para permitir fluxo de navegação do menu."""

    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.font = None

    def _ensure_font(self):
        if self.font is None:
            self.font = pygame.font.SysFont("arial", 28)

    def handle_events(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game_manager.running = False

    def update(self, dt: float):
        pass

    def draw(self, screen: pygame.Surface):
        self._ensure_font()
        screen.fill((20, 20, 25))
        text = self.font.render("GameWorld inicial (ESC para sair)", True, (220, 220, 220))
        screen.blit(text, text.get_rect(center=(self.game_manager.screen_width // 2,
                                                self.game_manager.screen_height // 2)))
