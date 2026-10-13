import matplotlib.pyplot as plt

"""
# parametry wejsciowe (przyklad 1.1)
R_0 = 1 # Romeo
L_0 = 1 # Julia
a_R = 0.5 
a_L = 0.7 
p_R = 0.2 
p_L = 0.5
"""
# wniosek: 
# niezaleznie od silnych uczuc poczatkowych uczucia te zbiegaja do stanu neutralnego

#1 paramtery wejsciowe (zadanie 1.1)
R_0 = 1 # Romeo
L_0 = 1 # Julia
a_R = 0.5 
a_L = 0.7 
p_R = 0.7 
p_L = 0.9 
# 


"""
#2 paramtery wejsciowe (zadanie 1.1)
R_0 = 1 # Romeo
L_0 = 1 # Julia
a_R = 1.0
a_L = 1.0 
p_R = 0.2 
p_L = -0.2 
"""

"""
#3 paramtery wejsciowe (zadanie 1.1)
R_0 = 1 # Romeo
L_0 = 1 # Julia
a_R = 0.5 
a_L = 0.8  
p_R = 0.2 
p_L = 0.5 
"""

R = [R_0]
L = [L_0]
t = [0]

dni = 100
for i in range(dni):
    R_i = a_R*R[-1] + p_R*L[-1]
    L_i = a_L*L[-1] + p_L*R[-1]

    R.append(R_i)
    L.append(L_i)
    t.append(i+1)

plt.figure(figsize=(10,5))
plt.subplot(1,2,1)
plt.plot(t,R,label='Romeo', color='Green', marker='.', linewidth=0.5, markersize=5)
plt.plot(t,L,label='Julia', color='Red', linestyle='--', marker='.', linewidth=0.5, markersize=5)
plt.title('Funkcja czasu')
plt.xlabel('Czas')
plt.ylabel('Romeo i Julia')
plt.legend()

plt.subplot(1,2,2)
plt.plot(R,L, color='Black', marker='.',linewidth=0.1, markersize=5)
plt.title('Portret fazowy')
plt.xlabel('Romeo')
plt.ylabel('Julia')

plt.tight_layout()
plt.show()


