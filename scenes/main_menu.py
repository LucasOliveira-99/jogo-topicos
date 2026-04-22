import pygame

from core.game_scene import GameScene


class MainMenuScene(GameScene):
    """Tela inicial do jogo."""

    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.title_font = None
        self.font = None
        self.small_font = None
        self.prompt_visible = True
        self.prompt_blink_timer = 0.0

    def _ensure_fonts(self):
        if self.title_font is None:
            self.title_font = pygame.font.SysFont("arial", 56, bold=True)
            self.font = pygame.font.SysFont("arial", 28)
            self.small_font = pygame.font.SysFont("arial", 18)

    def handle_events(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self._start_game()
                elif event.key == pygame.K_ESCAPE:
                    self.game_manager.running = False

    def update(self, dt: float):
        self.prompt_blink_timer += dt
        if self.prompt_blink_timer >= 0.5:
            self.prompt_blink_timer = 0.0
            self.prompt_visible = not self.prompt_visible

    def draw(self, screen: pygame.Surface):
        self._ensure_fonts()
        screen.fill((15, 15, 20))
        sw = self.game_manager.screen_width
        sh = self.game_manager.screen_height

        title = self.title_font.render("SURVIVORS", True, (255, 60, 60))
        screen.blit(title, title.get_rect(center=(sw // 2, sh // 3)))

        if self.prompt_visible:
            prompt = self.font.render("Press ENTER to start", True, (200, 200, 200))
            screen.blit(prompt, prompt.get_rect(center=(sw // 2, sh // 2 + 30)))

        esc = self.small_font.render("ESC to quit", True, (120, 120, 120))
        screen.blit(esc, esc.get_rect(center=(sw // 2, sh // 2 + 70)))

    def _start_game(self):
        from core.game_world import GameWorld
        self.game_manager.change_scene(GameWorld(self.game_manager))
