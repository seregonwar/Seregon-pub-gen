# __init__.py

# Importa le classi principali e le funzioni che vuoi rendere disponibili quando qualcuno importa il tuo pacchetto
from .gui import MainWindow
from .orbis_publishing_tools import OrbisPublishingTools

# Puoi anche definire __all__ per controllare cosa viene importato quando qualcuno usa "from package import *"
__all__ = [
    'MainWindow',
    'OrbisPublishingTools'
]

# Puoi anche aggiungere del codice di inizializzazione qui, se necessario
print("Initializing Orbis Publishing Tools package...")

# Versione del pacchetto
__version__ = "1.0.0"
