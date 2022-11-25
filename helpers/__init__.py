print("--- import helpers ---")
from . import filosofi
from . import sport
from . import cartes

from importlib import reload

reload(filosofi)
reload(sport)
reload(cartes)

#a supprimer à l'occasion
from .filosofi import *
from .sport import *
from .cartes import *