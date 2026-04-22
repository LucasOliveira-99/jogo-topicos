import sys
import os

# Garante que o diretório do jogo está no path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.game_manager import GameManager
from scenes.main_menu import MainMenuScene


def main():
    gm = GameManager(width=960, height=540, fps=60, title="Survivors")
    gm.push_scene(MainMenuScene(gm))
    gm.run()


if __name__ == "__main__":
    main()
