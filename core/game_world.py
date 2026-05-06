import pygame

from core.game_scene import GameScene
from core.camera import Camera
from objects.player import Player
from objects.enemy import Enemy
from objects.projectile import Projectile


class GameWorld(GameScene):
    """World inicial com jogador e câmera seguindo o personagem."""

    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.font = None
        self.small_font = None
        self.game_over = False
        self.kills = 0
        self.projectiles: list[Projectile] = []
        self.last_aim_direction = pygame.math.Vector2(1.0, 0.0)
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

    def _ensure_fonts(self):
        if self.font is None:
            self.font = pygame.font.SysFont("arial", 48, bold=True)
            self.small_font = pygame.font.SysFont("arial", 24)

    def _shoot(self):
        direction = self.last_aim_direction
        projectile = Projectile(
            x=self.player.x + self.player.width / 2 - 4,
            y=self.player.y + self.player.height / 2 - 4,
            width=8,
            height=8,
            velocity_x=direction.x * 420.0,
            velocity_y=direction.y * 420.0,
        )
        self.projectiles.append(projectile)

    def handle_events(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_manager.running = False
                elif self.game_over and (event.key == pygame.K_r or event.key == pygame.K_RETURN):
                    self.game_manager.change_scene(GameWorld(self.game_manager))
                elif not self.game_over and event.key == pygame.K_SPACE:
                    self._shoot()

    def update(self, dt: float):
        if self.game_over:
            return

        self.player.update(dt)
        if self.player.velocity_x != 0.0 or self.player.velocity_y != 0.0:
            self.last_aim_direction = pygame.math.Vector2(
                self.player.velocity_x,
                self.player.velocity_y,
            ).normalize()
        for projectile in self.projectiles:
            projectile.update(dt)
        
        # Atualizar inimigos com referência ao player
        for enemy in self.enemies:
            enemy.update(dt, self.player.rect)
            if self.player.rect.colliderect(enemy.rect):
                self.game_over = True
                self.player.velocity_x = 0.0
                self.player.velocity_y = 0.0
                break

        for projectile in self.projectiles:
            if not projectile.active:
                continue
            for enemy in self.enemies:
                if not enemy.active:
                    continue
                if projectile.rect.colliderect(enemy.rect):
                    projectile.active = False
                    enemy.active = False
                    self.kills += 1
                    break

        self.projectiles = [projectile for projectile in self.projectiles if projectile.active]
        self.enemies = [enemy for enemy in self.enemies if enemy.active]
        
        self.camera.follow(self.player.rect)

    def draw(self, screen: pygame.Surface):
        screen.fill((20, 20, 25))

        for projectile in self.projectiles:
            projectile.draw(screen, self.camera)
        
        # Desenhar inimigos
        for enemy in self.enemies:
            enemy.draw(screen, self.camera)
        
        # Desenhar jogador por último (no topo)
        self.player.draw(screen, self.camera)

        # Desenhar HUD
        self._ensure_fonts()
        hud_text = self.small_font.render(
            f"Inimigos restantes: {len(self.enemies)}", True, (255, 255, 255)
        )
        screen.blit(hud_text, (10, 10))
        kills_text = self.small_font.render(
            f"Eliminacoes: {self.kills}", True, (220, 220, 220)
        )
        screen.blit(kills_text, (10, 36))

        if self.game_over:
            self._ensure_fonts()
            overlay = pygame.Surface(
                (self.game_manager.screen_width, self.game_manager.screen_height),
                pygame.SRCALPHA,
            )
            overlay.fill((120, 0, 0, 120))
            screen.blit(overlay, (0, 0))

            title = self.font.render("GAME OVER", True, (255, 235, 235))
            hint = self.small_font.render(
                "Pressione R ou ENTER para reiniciar",
                True,
                (255, 255, 255),
            )
            screen.blit(
                title,
                title.get_rect(
                    center=(
                        self.game_manager.screen_width // 2,
                        self.game_manager.screen_height // 2 - 20,
                    )
                ),
            )
            screen.blit(
                hint,
                hint.get_rect(
                    center=(
                        self.game_manager.screen_width // 2,
                        self.game_manager.screen_height // 2 + 30,
                    )
                ),
            )
