import sys

import pygame


class GameManager:
    """Gerenciador principal — inicialização, main loop e controle de scenes."""

    def __init__(self, width: int = 960, height: int = 540, fps: int = 60,
                 title: str = "Survivors"):
        pygame.init()
        self.screen_width = width
        self.screen_height = height
        self.fps = fps
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True

        # Pilha de scenes — o topo é a scene ativa
        self._scene_stack: list = []

    @property
    def active_scene(self):
        return self._scene_stack[-1] if self._scene_stack else None

    def push_scene(self, scene):
        self._scene_stack.append(scene)

    def pop_scene(self):
        if self._scene_stack:
            self._scene_stack.pop()

    def change_scene(self, scene):
        """Substitui a scene ativa (descarta tudo acima)."""
        self._scene_stack.clear()
        self._scene_stack.append(scene)

    def run(self):
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0
            dt = min(dt, 0.05)  # cap para evitar saltos grandes

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    break

            if not self.running:
                break

            scene = self.active_scene
            if scene is None:
                self.running = False
                break

            scene.handle_events(events)
            scene.update(dt)
            scene.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
        sys.exit()
