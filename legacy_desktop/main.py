"""
================================================================================
CYBER-DOOM 2099: PUNTO DE ENTRADA PRINCIPAL (Main Entry Point)
================================================================================
Inicializa el motor estructurado en arquitectura de capas:
  - src.config       (Capa de Configuración y Constantes)
  - src.audio        (Capa de Síntesis de Audio)
  - src.graphics     (Capa de Texturas y Sprites)
  - src.domain       (Capa de Entidades y Lógica de Negocio)
  - src.engine       (Capa de Motor Raycasting 2.5D DDA y Mapa)
  - src.ui           (Capa de Presentación, HUD y Pantallas)
  - src.core         (Capa de Orquestación y Game Loop)
================================================================================
"""

import sys
import os

# Asegurar que el directorio raíz del proyecto esté en el PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.game_manager import CyberDoomGameManager

def main():
    game = CyberDoomGameManager()
    game.run()

if __name__ == "__main__":
    main()
