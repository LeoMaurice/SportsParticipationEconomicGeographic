print("--- import helpers ---")
from . import filosofi
from . import sport

from importlib import reload

reload(filosofi)
reload(sport)

#a supprimer à l'occasion
from .filosofi import *
from .sport import *