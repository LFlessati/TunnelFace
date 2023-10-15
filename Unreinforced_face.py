import math
import numpy as np

###############################################################################
# Definition of the input
###############################################################################

# Geometry
# Tunnel diameter [m]
D = 10
# Tunnel axis depth [m]
H = 78
        
#Soil properties
# Undrained Young in [kPa]
Eu = 25*1000
# Undrained strength [kPa]
Su = 250
# Unit weight in [kN/m3]
gam = 20

#At rest lateral earth pressure [-]
k0 = 1

#Final stress on the face [kPa]
sf = 0

###############################################################################
# Calculations
###############################################################################

#geostatic stress anisotropy:
ks  = (k0*(gam-9.81)+9.81)/gam

#average total stress on the tunnel face [kPa]
sf0 = ks*gam*H

#yielding value obtaineb by interpolating Fig. 16 of 
#di Prisco et al. (2018), 10.1007/s11440-017-0564-y
if ks<1:
    afu = 0.022+1.54*ks
else:
    afu = 1.324 + 0.24*ks

#elastic residual displacement [m]
ufrel = 1/3*sf0/Eu*D

#Final Qf value
Qf = (sf0-sf)/Su

#Non-dimensional displacement
if Qf<afu:
    qf = Qf
else:
    qf = afu*math.exp(Qf/afu-1)

#Dimensional displacement [m]
uf = qf*ufrel*Su/sf0

uf = round(uf,3)
print('The face displacement is equal to',uf,'m')

