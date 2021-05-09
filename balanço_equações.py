"""Em um misturador perfeito, avalia a resposta dinâmica a concentração da espécie A, o volume e a temperatura."""

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


# define modelo de mistura
def vaso(x, t, q, qf, Caf, Tf):
    # Entradas (4):
    # qf = Vazão Volumétrica de Entrada (l/min)
    # q = Vazão Volumétrica de Saída (l/min)
    # Caf = Concentração da Alimentação (mol/l)
    # Tf = Temperatura da Alimentação (K)

    # Estados (3):
    # Volume (l)
    V = x[0]

    # Concentração de A (mol/l)
    Ca = x[1]

    # Temperatura (K)
    T = x[2]

    # Parâmetros
    # Reação
    rA = 0.0

    # Balanço de massa: derivada do volume
    dVdt = qf - q

    # Balanço das espécies: derivada da concentração
    # Regra da cadeia: d(V*Ca)/dt = Ca * dV/dt + V * dCa/dt
    dCadt = (qf*Caf - q*Ca)/V - rA - (Ca*dVdt/V)

    # Balanço de energia: derivada da temperatura
    # Regra da cadeia: d(V*T)/dt = T * dV/dt + V * dT/dt
    dTdt = (qf*Tf - q*T)/V - (T*dVdt/V)

    # Retorna derivadas
    return [dVdt, dCadt, dTdt]


# Condições iniciais dos estados
print("Insira as condições iniciais abaixo por favor.")
V0 = float(input("Volume inicial do componente A dentro do tanque (l): "))
Ca0 = float(input("Concentração inicial do componente A no tanque (mol/l): "))
T0 = float(input("Temperatura inicial do tanque (K): "))
y0 = [V0, Ca0, T0]

# Intervalo de tempo (min)
t = np.linspace(0, 10, 100)

# Vazão Volumétrica de Entrada (l/min)
qf = np.ones(len(t)) * 5.2
qf[50:] = 5.1

# Vazão Volumétrica de Saída (l/min)
q = np.ones(len(t)) * 5.0

# Concentração da Alimentação (mol/l)
Caf = np.ones(len(t)) * 1.0
Caf[30:] = 0.5

# Temperatura de Alimentação (K)
Tf = np.ones(len(t)) * 300.0
Tf[70:] = 325.0

# Armazenamento de resultados
V = np.ones(len(t)) * V0
Ca = np.ones(len(t)) * Ca0
T = np.ones(len(t)) * T0

# Ciclo a cada etapa de tempo
for i in range(len(t)-1):
    # Simula
    entradas = (q[i], qf[i], Caf[i], Tf[i])
    ts = [t[i], t[i + 1]]
    y = odeint(vaso, y0, ts, args=entradas)
    # Armazena resultados
    V[i + 1] = y[-1][0]
    Ca[i + 1] = y[-1][1]
    T[i + 1] = y[-1][2]
    # Ajusta condição inicial para o próximo ciclo
    y0 = y[-1]

# Constrói resultados e salva o arquivo de dados
dado = np.vstack((t, qf, q, Tf, Caf, V, Ca, T))  # Pilha vertical
dado = dado.T  # transpor dado
np.savetxt('dado.txt', dado, delimiter=',')

# Traça as entradas e os resultados
plt.figure()

plt.subplot(3, 2, 1)
plt.plot(t, qf, 'b--', linewidth=3)
plt.plot(t, q, 'b:', linewidth=3)
plt.ylabel('Vazão Volumétrica (L/min)')
plt.legend(['Inlet', 'Outlet'], loc='best')

plt.subplot(3, 2, 3)
plt.plot(t, Caf, 'r--', linewidth=3)
plt.ylabel('Caf (mol/L)')
plt.legend(['Concentração da Alimentação'], loc='best')

plt.subplot(3, 2, 5)
plt.plot(t, Tf, 'k--', linewidth=3)
plt.ylabel('Tf (K)')
plt.legend(['Temperatura da Alimentação'], loc='best')
plt.xlabel('Tempo (min)')

plt.subplot(3, 2, 2)
plt.plot(t, V, 'b-', linewidth=3)
plt.ylabel('Volume (L)')
plt.legend(['Volume'], loc='best')

plt.subplot(3, 2, 4)
plt.plot(t, Ca, 'r-', linewidth=3)
plt.ylabel('Ca (mol/L)')
plt.legend(['Concentração'], loc='best')

plt.subplot(3, 2, 6)
plt.plot(t, T, 'k-', linewidth=3)
plt.ylabel('T (K)')
plt.legend(['Temperatura'], loc='best')
plt.xlabel('Tempo (min)')

plt.show()
