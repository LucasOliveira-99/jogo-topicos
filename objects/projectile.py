from __future__ import annotations

from dataclasses import dataclass

import pygame

from objects.game_object import GameObject


@dataclass(slots=True)
class Projectile(GameObject):
    """Projétil simples disparado pelo jogador."""

    speed: float = 420.0
    color: tuple[int, int, int] = (255, 236, 102)
    max_lifetime: float = 1.5
    lifetime: float = 0.0

    def update(self, dt: float):
        super().update(dt)
        self.lifetime += dt
        if self.lifetime >= self.max_lifetime:
            self.active = False

    def draw(self, screen: pygame.Surface, camera=None):
        rect = self.rect
        if camera is not None:
            rect = camera.apply(rect)
        pygame.draw.rect(screen, self.color, rect)