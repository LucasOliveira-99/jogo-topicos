import pygame

from core.game_scene import GameScene
from core.camera import Camera
from objects.player import Player


class GameWorld(GameScene):
    """World inicial com jogador e câmera seguindo o personagem."""

    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.camera = Camera(game_manager.screen_width, game_manager.screen_height)
        self.player = Player(
            x=game_manager.screen_width / 2,
            y=game_manager.screen_height / 2,
            width=32,
            height=32,
        )

    def handle_events(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game_manager.running = False

    def update(self, dt: float):
        self.player.update(dt)
        self.camera.follow(self.player.rect)

    def draw(self, screen: pygame.Surface):
        screen.fill((20, 20, 25))
        self.player.draw(screen, self.camera)
