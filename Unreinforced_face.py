import math
import numpy as np

###############################################################################
# Definition of the input
###############################################################################

# Geometry
# Tunnel diameter [m]
D = 10
# Tunnel axis depth [m]
H = 2
        
#Soil properties
# Undrained Young in [kPa]
Eu = 25*1000
# Undrained strength [kPa]
Su = 200
# Unit weight in [kN/m3]
gam = 20

#At rest lateral earth pressure [-]
k0 = 1