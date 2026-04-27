from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import pygame


@dataclass(slots=True)
class GameObject(ABC):
    """Base comum para objetos posicionados no mundo do jogo."""

    x: float
    y: float
    width: int
    height: int
    velocity_x: float = 0.0
    velocity_y: float = 0.0
    active: bool = True

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def move(self, dx: float, dy: float):
        self.x += dx
        self.y += dy

    def update(self, dt: float):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

    @abstractmethod
    def draw(self, screen: pygame.Surface, camera=None):
        raise NotImplementedError