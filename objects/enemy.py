from __future__ import annotations

from dataclasses import dataclass

import pygame

from objects.game_object import GameObject


@dataclass(slots=True)
class Enemy(GameObject):
    """Inimigo com IA básica de patrulha e perseguição."""

    speed: float = 100.0
    vision_range: float = 150.0
    color: tuple[int, int, int] = (255, 0, 0)
    direction_x: float = 1.0  # Direção de patrulha inicial
    direction_y: float = 0.0

    def _calculate_distance(self, rect: pygame.Rect) -> float:
        """Calcula distância entre este inimigo e um alvo."""
        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2
        target_x = rect.centerx
        target_y = rect.centery
        dx = target_x - center_x
        dy = target_y - center_y
        return (dx**2 + dy**2) ** 0.5

    def pursue(self, target_rect: pygame.Rect):
        """Persegue o alvo se estiver dentro do alcance de visão."""
        distance = self._calculate_distance(target_rect)
        
        if distance < self.vision_range:
            # Calcular direção para o alvo
            center_x = self.x + self.width / 2
            center_y = self.y + self.height / 2
            target_x = target_rect.centerx
            target_y = target_rect.centery
            
            dx = target_x - center_x
            dy = target_y - center_y
            
            # Normalizar a direção
            if distance > 0:
                direction = pygame.math.Vector2(dx, dy).normalize()
                self.velocity_x = direction.x * self.speed
                self.velocity_y = direction.y * self.speed
            return True
        return False

    def patrol(self):
        """Patrulha alternando entre direções."""
        self.velocity_x = self.direction_x * self.speed
        self.velocity_y = self.direction_y * self.speed

    def update(self, dt: float, player_rect: pygame.Rect | None = None):
        """Atualiza o inimigo com IA básica."""
        if player_rect is not None:
            is_pursuing = self.pursue(player_rect)
        else:
            is_pursuing = False

        if not is_pursuing:
            self.patrol()

        # Atualizar posição baseado na velocidade
        super().update(dt)

    def draw(self, screen: pygame.Surface, camera=None):
        """Desenha o inimigo na tela."""
        rect = self.rect
        if camera is not None:
            rect = camera.apply(rect)
        pygame.draw.rect(screen, self.color, rect)
