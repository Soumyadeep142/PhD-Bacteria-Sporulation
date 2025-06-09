from numpy import *
p_range=[0, 18, 30, 41, 50, 57, 69, 90]
phi_range=[i*pi/180 for i in p_range]

R_range=[100000000000, 22.921, 14.067, 8.531, 7.575, 7.629, 7.469, 7.552]
r=5.813
R_rn=[i/r for i in R_range]
for (p,R) in zip(phi_range, R_range):
	term2=800*R**2*(1-sqrt(1-(cos(p)/R)**2))
	with open('term2.txt', 'a') as f:
		f.write(str(round(p,3)))
		f.write('	')
		f.write(str(round(term2, 3)))
		f.write('\n')
		
