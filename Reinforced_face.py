import math
import numpy as np

###############################################################################
# Definition of the input
###############################################################################

# Geometry
# Tunnel diameter [m]
D = 12
# Tunnel axis depth [m]
H = 78
        
#Soil properties
# Undrained Young in [kPa]
Eu = 25*1000
# Undrained strength [kPa]
Su = 225
# Unit weight in [kN/m3]
gam = 20

#Reinforcements properties
# Lenght in [m]
L = 18
# Diameter in [m]
d = 0.12
# Equivalent stiffness in [kPa]
Er = 30*1000*1000
# number
n = 100

#At rest lateral earth pressure [-]
k0 = 1


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

#calculating everything necessary for introducing reinforcements in the face characteristic curve
DQf = 0.8*L/D*d/D*n
Es = Er*d**2/(Eu*L**2)
R1 = 0.47*L/D
R2 = (1-math.exp(-2*n*d/D))
R3 = 1/2 + 1/2*(80*Es-1)/(80*Es+1)
DR = R1*R2*R3

afr = (afu + DQf)/(1+DR)


#elastic residual displacement [m]
ufrel = 1/3*sf0/Eu*D




#Final Qf value
Qf = sf0/Su

#Non-dimensional displacement
if Qf<afr:
    qf = Qf/(1+DR)
else:
    qf = afr/(1+DR)*math.exp(Qf/afr-1)

#Dimensional displacement [m]
uf = qf*ufrel*Su/sf0

uf = round(uf,3)
print('The face displacement is equal to',uf,'m')

