import pygame

from core.game_scene import GameScene
from core.camera import Camera
from objects.player import Player
from objects.enemy import Enemy


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
        
        # Criar inimigos em posições iniciais
        self.enemies = [
            Enemy(x=100, y=100, width=32, height=32, speed=80.0),
            Enemy(x=400, y=200, width=32, height=32, speed=90.0, direction_x=-1.0),
            Enemy(x=600, y=400, width=32, height=32, speed=100.0, direction_y=1.0),
        ]

    def handle_events(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game_manager.running = False

    def update(self, dt: float):
        self.player.update(dt)
        
        # Atualizar inimigos com referência ao player
        for enemy in self.enemies:
            enemy.update(dt, self.player.rect)
        
        self.camera.follow(self.player.rect)

    def draw(self, screen: pygame.Surface):
        screen.fill((20, 20, 25))
        
        # Desenhar inimigos
        for enemy in self.enemies:
            enemy.draw(screen, self.camera)
        
        # Desenhar jogador por último (no topo)
        self.player.draw(screen, self.camera)
