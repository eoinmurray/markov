from sympy import *
from sympy.solvers.solvers import solve_linear_system_LU
import json
# # ansatz values
# tp_h = 20
# tp_e = 2

# tau_x = 1.6
# tau_xn = 5.1
# tau_xp = 5.1
# tau_xx = 0.96

p0, pe, ph, px, pxn, pxp, pxx = symbols('p0, pe, ph, px, pxn, pxp, pxx')

tp_h, tp_e, tau_x, tau_xn, tau_xp, tau_xx = symbols('tp_h, tp_e, tau_x, tau_xn, tau_xp, tau_xx')

tau_x = 1.6
tau_xn = 5.1
tau_xx = 0.96


x = {ph: tau_xx*tp_h**2*(tau_x*(tau_xn*tp_e*(tau_xp*(tau_xn + tp_h) + tp_e*(tau_xn + tau_xp + tp_e + tp_h)) + tau_xp*tp_h*(tau_xn + tp_h)*(tau_xn + tp_e + tp_h) + tp_e*tp_h*(tau_xn + tp_e + tp_h)*(tau_xn + tau_xp + tp_e + tp_h)) + tau_xp*(tau_xn + tp_h)*(tp_e + tp_h)**2*(tau_xn + tp_e + tp_h))/(tau_xx*(tau_xn + tp_h)*(tau_xp*tp_e*(tau_xn*(tau_x*tp_h**2 + tp_e*(tau_x + tp_h)*(tp_e + tp_h)) + tp_e*(tau_xn + tp_h)*(tp_e + tp_h)**2) + tp_h*(tau_xp*(tau_x*tp_h**2 + tp_e*(tau_x + tp_h)*(tp_e + tp_h)) + tp_h*(tau_xp + tp_e)*(tp_e + tp_h)**2)*(tau_xn + tp_e + tp_h)) + tp_e*(tau_xx*tp_e*(tau_xn*(tau_x*tp_h**2 + tp_e*(tau_x + tp_h)*(tp_e + tp_h)) + tp_e*(tau_xn + tp_h)*(tp_e + tp_h)**2) + tp_h*(tau_xx*(tau_x*tp_h**2 + tp_e*(tau_x + tp_h)*(tp_e + tp_h)) + tp_e*tp_h*(tp_e + tp_h)**2)*(tau_xn + tp_e + tp_h))*(tau_xn + tau_xp + tp_e + tp_h)), pxp: tau_xx*tp_e*tp_h**2*(tau_xn + tp_h)*(tp_e + tp_h)**2*(tau_xn + tp_e + tp_h)/(tau_xx*(tau_xn + tp_h)*(tau_xp*tp_e*(tau_xn*(tau_x*tp_h**2 + tp_e*(tau_x + tp_h)*(tp_e + tp_h)) + tp_e*(tau_xn + tp_h)*(tp_e + tp_h)**2) + tp_h*(tau_xp*(tau_x*tp_h**2 + tp_e*(tau_x + tp_h)*(tp_e + tp_h)) + tp_h*(tau_xp + tp_e)*(tp_e + tp_h)**2)*(tau_xn + tp_e + tp_h)) + tp_e*(tau_xx*tp_e*(tau_xn*(tau_x*tp_h**2 + tp_e*(tau_x + tp_h)*(tp_e + tp_h)) + tp_e*(tau_xn + tp_h)*(tp_e + tp_h)**2) + tp_h*(tau_xx*(tau_x*tp_h**2 + tp_e*(tau_x + tp_h)*(tp_e + tp_h)) + tp_e*tp_h*(tp_e + tp_h)**2)*(tau_xn + tp_e + tp_h))*(tau_xn + tau_xp + tp_e + tp_h)), p0: tau_x*tau_xx*tp_e*tp_h*(tau_xn*tp_e*(tau_xp*(tau_xn + tp_h) + tp_e*(tau_xn + tau_xp + tp_e + tp_h)) + tau_xp*tp_h*(tau_xn + tp_h)*(tau_xn + tp_e + tp_h) + tp_e*tp_h*(tau_xn + tp_e + tp_h)*(tau_xn + tau_xp + tp_e + tp_h))/(tau_xx*(tau_xn + tp_h)*(tau_xp*tp_e*(tau_xn*(tau_x*tp_h**2 + tp_e*(tau_x + tp_h)*(tp_e + tp_h)) + tp_e*(tau_xn + tp_h)*(tp_e + tp_h)**2) + tp_h*(tau_xp*(tau_x*tp_h**2 + tp_e*(tau_x + tp_h)*(tp_e + tp_h)) + tp_h*(tau_xp + tp_e)*(tp_e + tp_h)**2)*(tau_xn + tp_e + tp_h)) + tp_e*(tau_xx*tp_e*(tau_xn*(tau_x*tp_h**2 + tp_e*(tau_x + tp_h)*(tp_e + tp_h)) + tp_e*(tau_xn + tp_h)*(tp_e + tp_h)**2) + tp_h*(tau_xx*(tau_x*tp_h**2 + tp_e*(tau_x + tp_h)*(tp_e + tp_h)) + tp_e*tp_h*(tp_e + tp_h)**2)*(tau_xn + tp_e + tp_h))*(tau_xn + tau_xp + tp_e + tp_h)), px: tau_xx*tp_e*tp_h*(tp_e + tp_h)*(tau_xn*tp_e*(tau_xp*(tau_xn + tp_h) + tp_e*(tau_xn + tau_xp + tp_e + tp_h)) + tau_xp*tp_h*(tau_xn + tp_h)*(tau_xn + tp_e + tp_h) + tp_e*tp_h*(tau_xn + tp_e + tp_h)*(tau_xn + tau_xp + tp_e + tp_h))/(tau_xx*(tau_xn + tp_h)*(tau_xp*tp_e*(tau_xn*(tau_x*tp_h**2 + tp_e*(tau_x + tp_h)*(tp_e + tp_h)) + tp_e*(tau_xn + tp_h)*(tp_e + tp_h)**2) + tp_h*(tau_xp*(tau_x*tp_h**2 + tp_e*(tau_x + tp_h)*(tp_e + tp_h)) + tp_h*(tau_xp + tp_e)*(tp_e + tp_h)**2)*(tau_xn + tp_e + tp_h)) + tp_e*(tau_xx*tp_e*(tau_xn*(tau_x*tp_h**2 + tp_e*(tau_x + tp_h)*(tp_e + tp_h)) + tp_e*(tau_xn + tp_h)*(tp_e + tp_h)**2) + tp_h*(tau_xx*(tau_x*tp_h**2 + tp_e*(tau_x + tp_h)*(tp_e + tp_h)) + tp_e*tp_h*(tp_e + tp_h)**2)*(tau_xn + tp_e + tp_h))*(tau_xn + tau_xp + tp_e + tp_h)), pe: tau_xx*tp_e**2*(tau_x*(tau_xn*tp_e*(tau_xp*(tau_xn + tp_h) + tp_e*(tau_xn + tau_xp + tp_e + tp_h)) + tau_xp*tp_h*(tau_xn + tp_h)*(tau_xn + tp_e + tp_h) + tp_e*tp_h*(tau_xn + tp_e + tp_h)*(tau_xn + tau_xp + tp_e + tp_h)) + tau_xn*(tp_e + tp_h)**2*(tau_xp*(tau_xn + tp_h) + tp_e*(tau_xn + tau_xp + tp_e + tp_h)))/(tau_xx*(tau_xn + tp_h)*(tau_xp*tp_e*(tau_xn*(tau_x*tp_h**2 + tp_e*(tau_x + tp_h)*(tp_e + tp_h)) + tp_e*(tau_xn + tp_h)*(tp_e + tp_h)**2) + tp_h*(tau_xp*(tau_x*tp_h**2 + tp_e*(tau_x + tp_h)*(tp_e + tp_h)) + tp_h*(tau_xp + tp_e)*(tp_e + tp_h)**2)*(tau_xn + tp_e + tp_h)) + tp_e*(tau_xx*tp_e*(tau_xn*(tau_x*tp_h**2 + tp_e*(tau_x + tp_h)*(tp_e + tp_h)) + tp_e*(tau_xn + tp_h)*(tp_e + tp_h)**2) + tp_h*(tau_xx*(tau_x*tp_h**2 + tp_e*(tau_x + tp_h)*(tp_e + tp_h)) + tp_e*tp_h*(tp_e + tp_h)**2)*(tau_xn + tp_e + tp_h))*(tau_xn + tau_xp + tp_e + tp_h)), pxx: tp_e**2*tp_h**2*(tp_e + tp_h)**2*(tau_xn + tp_e + tp_h)*(tau_xn + tau_xp + tp_e + tp_h)/(tau_xx*(tau_xn + tp_h)*(tau_xp*tp_e*(tau_xn*(tau_x*tp_h**2 + tp_e*(tau_x + tp_h)*(tp_e + tp_h)) + tp_e*(tau_xn + tp_h)*(tp_e + tp_h)**2) + tp_h*(tau_xp*(tau_x*tp_h**2 + tp_e*(tau_x + tp_h)*(tp_e + tp_h)) + tp_h*(tau_xp + tp_e)*(tp_e + tp_h)**2)*(tau_xn + tp_e + tp_h)) + tp_e*(tau_xx*tp_e*(tau_xn*(tau_x*tp_h**2 + tp_e*(tau_x + tp_h)*(tp_e + tp_h)) + tp_e*(tau_xn + tp_h)*(tp_e + tp_h)**2) + tp_h*(tau_xx*(tau_x*tp_h**2 + tp_e*(tau_x + tp_h)*(tp_e + tp_h)) + tp_e*tp_h*(tp_e + tp_h)**2)*(tau_xn + tp_e + tp_h))*(tau_xn + tau_xp + tp_e + tp_h)), pxn: tau_xx*tp_e**2*tp_h*(tp_e + tp_h)**2*(tau_xp*(tau_xn + tp_h) + tp_e*(tau_xn + tau_xp + tp_e + tp_h))/(tau_xx*(tau_xn + tp_h)*(tau_xp*tp_e*(tau_xn*(tau_x*tp_h**2 + tp_e*(tau_x + tp_h)*(tp_e + tp_h)) + tp_e*(tau_xn + tp_h)*(tp_e + tp_h)**2) + tp_h*(tau_xp*(tau_x*tp_h**2 + tp_e*(tau_x + tp_h)*(tp_e + tp_h)) + tp_h*(tau_xp + tp_e)*(tp_e + tp_h)**2)*(tau_xn + tp_e + tp_h)) + tp_e*(tau_xx*tp_e*(tau_xn*(tau_x*tp_h**2 + tp_e*(tau_x + tp_h)*(tp_e + tp_h)) + tp_e*(tau_xn + tp_h)*(tp_e + tp_h)**2) + tp_h*(tau_xx*(tau_x*tp_h**2 + tp_e*(tau_x + tp_h)*(tp_e + tp_h)) + tp_e*tp_h*(tp_e + tp_h)**2)*(tau_xn + tp_e + tp_h))*(tau_xn + tau_xp + tp_e + tp_h))}


print solve(Eq(x[pxp], 0), tau_xp)

# T = Matrix([
#     [-tp_e-tp_h, 0, 0, tau_x, 0, 0,0],
#     [tp_e, -tp_h, 0, 0, tau_xn, 0,0],
#     [tp_h, 0, -tp_e, 0, 0, tau_xp,0],
#     [0, tp_h, tp_e, - tp_h- tp_e - tau_x, 0,0, tau_xx],
#     [0,0, 0,  tp_e, -tau_xn - tp_h, 0, 0],
#     [0, 0, 0, tp_h, 0, -tau_xp - tp_e, 0],
#     [0,0, 0, 0, tp_h, tp_e, -tau_xx],
# ])

# P = Matrix([
# 	[p0],
# 	[pe],
# 	[ph],
# 	[px],
# 	[pxn],
# 	[pxp],
# 	[pxx],
# ])


# sys = []
# for i in (T*P):
# 	sys.append(i)

# sys.append( p0+ pe+ ph+ px+ pxn+ pxp+ pxx-1 )

# x = solve(sys, [p0, pe, ph, px, pxn, pxp, pxx])
