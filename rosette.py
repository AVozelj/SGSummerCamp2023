import numpy as np

eps_alpha = 435
eps_beta = 321
eps_gamma = -101

alpha=0
beta=45
gamma=90

cs1 = np.cos(np.radians(alpha))
cs2 = np.cos(np.radians(beta))
cs3 = np.cos(np.radians(gamma))
sn1 = np.sin(np.radians(alpha))
sn2 = np.sin(np.radians(beta))
sn3 = np.sin(np.radians(gamma))

M = np.array([[cs1**2,sn1**2,cs1*sn1],[cs2**2,sn2**2,cs2*sn2],[cs3**2,sn3**2,cs3*sn3]])

eps = np.array([eps_alpha,eps_beta,eps_gamma])

epsX,epsY,gammaXY = np.linalg.solve(M, eps)

print(epsX,epsY,gammaXY)

eps1 = (epsX+epsY)/2 + np.sqrt(((epsX-epsY)/2)**2 + (gammaXY/2)**2)

eps2 = (epsX+epsY)/2 - np.sqrt(((epsX-epsY)/2)**2 + (gammaXY/2)**2)

fi = np.degrees(0.5*np.arctan2(gammaXY,epsX-epsY))

gamma_max = np.sqrt(((epsX-epsY)/2)**2 + (gammaXY/2)**2)

fi_s = np.degrees(0.5*np.arctan2(-(epsX-epsY),gammaXY))

print(eps1,eps2)

print(fi)   

print(gamma_max, fi_s)

YM = 2.1e5
poisson = 0.3

#
eps1 *= 1e-6
eps2 *= 1e-6

s1 = (YM/(1-poisson**2))*(eps1+poisson*eps2)
s2 = (YM/(1-poisson**2))*(eps2+poisson*eps1)

print(s1,s2)