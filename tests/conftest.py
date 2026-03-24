import os
import sys

# Permite importação de módulos do projeto como `from domain.game import Game`
ROOT_PROJECT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_PROJECT not in sys.path:
    sys.path.insert(0, ROOT_PROJECT)
