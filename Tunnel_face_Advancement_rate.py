import math
import numpy as np

###############################################################################
# Definition of the input
###############################################################################

# Geometry
# Tunnel diameter [m]
D  = 10
# Tunnel axis depth [m]
H  = 90
# Position of water table w.r.t. tunnel axis depth [m]
Hw = 85 

    
#Mechanical/hydraulic properties
# Drained Young modulus in [kPa]
E = 25*1000
# Poisson ratio [-]
nu = 0.3
# Friction angle [degree]
phi = 25
# Soil saturated unit weight in [kN/m3]
gam = 20
# Water unit weight in [kN/m3]
gamw = 10
# Permeability [m/day]
k = 1e-4


#At rest lateral earth pressure [-]
k0 = 1

# Lenght of segmental lining ring (only for spoil assessment) [m]
Lr = 1.0

#Final total stress on the face [kPa]
sf = 0
#Excavation rate [m/day]
vex = 10

###############################################################################
# Calculations
###############################################################################


#Evaluation of stresses at tunnel axis depth
# Average total vertical stress at tunnel axis depth [kPa]
sv0 = gam*H
# Average pore water pressure on the tunnel face [kPa]
u0 = gamw*Hw
# Average vertical effective stress at the tunnel face [kPa]
sveff = sv0 - u0
# Average horizontal effective stress on the tunnel face  [kPa]
sheff = sveff*k0
# Average horizontal total stress on the tunnel face  [kPa]
sf0 = sheff  + u0
# Geostatic stress anisotropy:
ks  = sf0/sv0
# Geostatic stress anisotropy:
peff  = (sveff+2*sheff)/3

#Additional soil properties
# Extension critical state line
Me = 6*math.sin(phi*math.pi/180)/(3+math.sin(phi*math.pi/180))
# alpha obtained by interpolating fig. 13 of Flessati & di Prisco
alpha = 0.0005*phi**2-0.009*phi+1
# Equivalent undrained strenght
Sus = alpha*Me/2*peff
#limit effective stress
seffL=(gam-gamw)*D*(1/(9*math.tan(phi*math.pi/180))-0.05)
#Elastic bulk modulus
K = E/(3*(1-2*nu))
#Elastic undrained modulus
Eu = 1.5*E/(1+nu)

# Excavation rate
# Influence length
La = 1.5*D
# Excavation time
tu = La/vex
# Non-dimensional excavation rate
Upsilon = gamw*D**2/(k*K*tu)

#Non dimensional characteristic curve parameters
#Initial slope
R = 0.725 + (1-0.725)*0.065*Upsilon**(0.635)/(0.065*Upsilon**(0.635)+1)

#Yield point
#Undrained yielding value obtained by interpolating Fig. 16 of 
#di Prisco et al. (2018), 10.1007/s11440-017-0564-y
if ks<1:
    afu = 0.022+1.54*ks
else:
    afu = 1.324 + 0.24*ks
#Partially drained yielding point
af = 0.686 + (afu-0.686)*0.2*Upsilon**(0.635)/(0.2*Upsilon**(0.635)+1)

#Limit load
#Drained non dimensional limit load
QLd = (sheff-seffL)/Sus
#Partially drained limit load
QL = QLd + 1.6*Upsilon


#elastic residual displacement [m]
ufrel = 1/3*sf0/Eu*D

#Final Qf value
Qf = (sf0-sf)/Sus

#Non-dimensional displacement
if Qf<af:
    qf = Qf/R
else:
    qf = af/R*math.exp(Qf/af-1) + (Qf-af)/(QL-Qf)


#Output calculation
#Dimensional displacement [m]
uf = qf*ufrel*Sus/sf0
#Spoil weight per each lining segment [kN]
Ws = math.pi*D**2/4*(Lr+uf)*gam
#Volume loss at the face [%]
VLf = uf/La*100

#Output print
uf = round(uf,3)
print('The face displacement is equal to',uf,'m')
Ws = round(Ws,0)
print('The spoil weight per each lining segment is equal to',Ws,'kN')
VLf = round(VLf,2)
print('The volume loss at the face is equal to',VLf,'%')
