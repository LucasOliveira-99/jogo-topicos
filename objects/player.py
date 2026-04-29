from __future__ import annotations

from dataclasses import dataclass

import pygame

from objects.game_object import GameObject


@dataclass(slots=True)
class Player(GameObject):
    """Jogador controlado por teclado (WASD/setas)."""

    speed: float = 200.0
    color: tuple[int, int, int] = (0, 162, 255)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        direction = pygame.math.Vector2(0, 0)

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            direction.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            direction.y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            direction.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            direction.x += 1

        if direction.length_squared() > 0:
            direction = direction.normalize()

        self.velocity_x = direction.x * self.speed
        self.velocity_y = direction.y * self.speed

    def update(self, dt: float):
        self.handle_input()
        super().update(dt)

    def draw(self, screen: pygame.Surface, camera=None):
        rect = self.rect
        if camera is not None:
            rect = camera.apply(rect)
        pygame.draw.rect(screen, self.color, rect)
