"""
================================================================================
CYBER-DOOM 2099 // ACCESO DIRECTO MODULAR
================================================================================
Punto de acceso compatible para ejecución directa.
Redirige a la arquitectura por capas ubicada en el paquete 'src/'.
================================================================================
"""

import sys
import os

# Asegurar que el directorio raíz esté en sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.game_manager import CyberDoomGameManager

if __name__ == "__main__":
    game = CyberDoomGameManager()
    game.run()
