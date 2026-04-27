from __future__ import annotations

from dataclasses import dataclass

import pygame


@dataclass(slots=True)
class Camera:
    """Camera 2D simples para acompanhar o que acontece no mundo."""

    x: float = 0.0
    y: float = 0.0
    width: int = 0
    height: int = 0

    def center_on(self, x: float, y: float):
        self.x = x - (self.width / 2)
        self.y = y - (self.height / 2)

    def follow(self, target: pygame.Rect, world_width: int | None = None,
               world_height: int | None = None):
        self.center_on(target.centerx, target.centery)
        if world_width is not None and world_height is not None:
            self.clamp_to_world(world_width, world_height)

    def clamp_to_world(self, world_width: int, world_height: int):
        max_x = max(0, world_width - self.width)
        max_y = max(0, world_height - self.height)
        self.x = max(0, min(self.x, max_x))
        self.y = max(0, min(self.y, max_y))

    def apply(self, rect: pygame.Rect) -> pygame.Rect:
        return rect.move(-int(self.x), -int(self.y))