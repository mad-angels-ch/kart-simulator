# fichier lancé par la commande "python kart_simulator"

import os
import time

from kart_simulator.lge import LGE

lge = LGE("kart_simulator/lge.ini")
lge.start()

time.sleep(2)

lge.stop()