# fichier lancé par la commande "python kart_simulator"

import os

from kart_simulator.lge import LGE

lge = LGE("kart_simulator/lge.ini")
lge.run()

print(lge)