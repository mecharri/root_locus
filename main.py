import numpy as np
import matplotlib.pyplot as plt
import control as ctl
import math
import symbolic

s = ctl.TransferFunction.s

# Sistema a lazo abierto
P1 = 1e3
P2 = 100e3
P3 = 500e3
A0 = 1e3
G = A0/((s/P1+1)*(s/P2+1)*(s/P3+1))


k =1
# Sistema realimentado
H = G/(1+k*G)
# Muestro ganancia lazo cerrado para comprobar resultado
print(H)
#Separo en parte real e imaginaria de los polos y ceros a lazo cerrado para hacer diagrama de polos y ceros
x_polos = ctl.pole(H).real
y_polos = ctl.pole(H).imag

x_zeros = ctl.zero(H).real
y_zeros = ctl.zero(H).imag

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.scatter(x_polos,y_polos,marker="x")
# ax.scatter(x_zeros, y_zeros, marker="o")
ax.set_xlabel('sigma')
ax.set_ylabel('jw')
ax.set_title("Polos de la transferencia a lazo cerrado")

# Hago la respuesta al escalón
Tau_dominante = 1/min(abs(x_polos))
#El tau dominante es la inversa del polo más cerca del eje imaginario
t_resp = 4* Tau_dominante
tvec = np.linspace(0,t_resp,5000) #Vector de tiempos de 5k puntos de 0 a 4 veces el tau dominante
tvec, yout= ctl.step_response(H, tvec)

fig2 = plt.figure()
ax2 = fig2.add_subplot(1,1,1)
ax2.plot(tvec,yout)

ax2.set_xlabel('tiempo [s]')
ax2.set_ylabel('volts [V]')
ax2.set_title("Respuesta al escalón")

#Hago el bodel de la ganancia de lazo
fig3 = plt.figure()
w = np.logspace(math.log10(min(P1,P2,P3)/10),math.log10(10*max(P1,P2,P3))) #Empiezo una década antes del primer polo y termino una década despues
mag,phase,omega = ctl.bode(k*G,w,dB=1, deg = 1, plot= 1,margins=1);
gm, pm, Wcg, Wcp = ctl.margin(k*G) #Margen de fase y magnitud con sus pulsaciones
print(gm)
print(pm)


plt.show()
