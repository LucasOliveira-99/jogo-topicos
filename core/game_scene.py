from abc import ABC, abstractmethod

import pygame


class GameScene(ABC):
    """Classe abstrata base para todas as cenas do jogo (worlds e menus)."""

    def __init__(self, game_manager):
        self.game_manager = game_manager

    @abstractmethod
    def handle_events(self, events: list[pygame.event.Event]):
        pass

    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface):
        pass
