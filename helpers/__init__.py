from .filosofi import *
from .sport import *

# library carte

import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.express as px
from IPython.core.display import display, HTML

# Importation des librairies classiques de python
import unicodedata
import requests
import time
import os
from tqdm import tqdm
import io
import warnings

# Importation des librairies de datascience et autres
import pandas as pd
import numpy as np
import pynsee
import pynsee.download
from pynsee.sirene import *
from pynsee.utils.init_conn import init_conn
from zipfile import ZipFile
from fuzzywuzzy import fuzz