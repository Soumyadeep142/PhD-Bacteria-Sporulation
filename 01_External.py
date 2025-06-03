from numpy import *
#from matplotlib.pyplot import *

G=25						#Strain Energy term
E=60						#External Energy
sig_tilde=800					#Surface Energy term
X=84						#Pressure term
alpha_tilde=8*10**(-5)				#alpha/(pi*a**3)
a2v=26.7					#a2v
def f(phi, h, t):	
	Y=8*pi*(2*h/(h**2+1)-2*h**3/(h**2+1)**2)
	h_prime=(a2v)*2*alpha_tilde/(1+h**2)
	A=G*cos(phi)
	B=Y*h_prime
	return (G+E-Y*h_prime-X)

def h_tilde(phi, h, t):
	return (a2v)*2*alpha_tilde/(1+h**2)
	
t=0
phi=0
h=0
s=0.01

phi_points=[phi]
t_points=[t]
h_points=[h]

while phi<=pi/2 and h<=1:
	print(t, phi, h)
	
	t=t+s
	phi=phi+s*f(phi, h, t)
	h=h+s*h_tilde(phi, h, t)
	
	t_points.append(t)
	phi_points.append(phi)
	h_points.append(h)
	
t_points=[(a2v)*t/3600 for t in t_points]	
data=column_stack((t_points, phi_points, h_points))
savetxt('E10.txt', data, fmt='%s')
