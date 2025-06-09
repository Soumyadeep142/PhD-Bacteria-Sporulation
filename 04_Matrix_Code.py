from numpy import *
from matplotlib.pyplot import *

G=1
sig_s_P=800
Gamma=20
r=400*10**(-9)
v=15*10**(-9)
k=11250*10**(-21)
alpha=0.058*10**(-18)/3600
alpha_t=alpha/r**3
P=10**6

#########Guesses##############
R=1.30
ph=70*pi/180
X=1.4
###############################

d=sqrt(1+R**2-2*(cos(ph)**2-sin(ph)*sqrt(R**2-cos(ph)**2)))
A=(-pi*cos(ph)**2/R**3)/(sqrt(1-cos(ph)**2/R**2))+sig_s_P*(cos(ph)**2+(-1+sqrt(1-cos(ph)**2/R**2))*R**2)/(sqrt(1-cos(ph)**2/R**2)*R)
B=(-pi*sin(2*ph)/R**2)/(2*sqrt(1-cos(ph)**2/R**2))-Gamma*sin(ph)-sig_s_P*cos(ph)*sin(ph)/(sqrt(1-cos(ph)**2/R**2))
C=-G*cos(ph)+X-alpha*P/k
D=(R*sqrt(R**2-cos(ph)**2)+sin(ph))/(sqrt(R**2-cos(ph)**2)*sqrt(R**2-cos(2*ph)+2*(sqrt(R**2-cos(ph)**2))*sin(ph)))-4*d*(-pi*R+d**2*pi*R-2*d*pi*R**2+pi*R**3)/(pi*(-1+d+R)*(1+d+R)*(-1+d**2-2*d*R+R**2))
E=-1/2*(cos(ph)+cos(3*ph)-2*sqrt(R**2-cos(ph)**2)*sin(2*ph))/(sqrt(R**2-cos(ph)**2)*sqrt(R**2-cos(2*ph)+2*(sqrt(R**2-cos(ph)**2))*sin(ph)))
F=-4*d**2*alpha_t/(pi*(-1+d+R)*(1+d+R)*(-1+d**2-2*d*R+R**2))
LHS=[[A, B], [D, E]]
RHS=[C, F]
R_phi=linalg.solve(LHS, RHS)
print(R_phi[0], R_phi[1]*180/pi*600)
print(f' A={A},\n B={B},\n C={C},\n D={D},\n E={E},\n F={F}')
