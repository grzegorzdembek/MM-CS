import matplotlib.pyplot as plt

# analiza modelu romansu na przykladzie Romea i Julii
class Lab01:
    def __init__(self, R_0: float, L_0: float, a_R: float, a_L: float, p_R: float, p_L: float):
        self.R_0 = R_0
        self.L_0 = L_0
        self.a_R = a_R
        self.a_L = a_L
        self.p_R = p_R
        self.p_L = p_L

        self.R = [R_0]
        self.L = [L_0]
        self.t = [0]

    def simulation(self, days=100):
        for day in range(days):
            R_next = self.a_R*self.R[-1] + self.p_R*self.L[-1]
            L_next = self.a_L*self.L[-1] + self.p_L*self.R[-1] 
            
            self.R.append(R_next)
            self.L.append(L_next)
            self.t.append(day+1)

    def drawPlot(self):       
        max_val = max(max(self.R), max(self.L))    
        min_val = min(min(self.R), min(self.L))
        limit = max(abs(max_val), abs(min_val))
        limit = limit * 1.1

        plt.figure(figsize=(12, 7))

        plt.subplot(1, 2, 1)
        plt.plot(self.t, self.R, label='Romeo', color='Blue', marker='.', linewidth=0.5, markersize=5)
        plt.plot(self.t, self.L, label='Julia', color='Green', linestyle='--', marker='.', linewidth=0.5, markersize=5)
        plt.title('Funkcja czasu')
        plt.xlabel('Czas')
        plt.ylabel('Romeo i Julia')
        plt.xlim(0, max(self.t)) 
        plt.ylim(-limit, limit)
        plt.axhline(y=0, color='gray', linestyle='-', linewidth=0.5) 
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(self.R, self.L, color='Black', marker='.', linewidth=0.5, markersize=5) 
        plt.title('Portret fazowy')
        plt.xlabel('Romeo')
        plt.ylabel('Julia')
        plt.xlim(-limit, limit)
        plt.ylim(-limit, limit)
        plt.axhline(y=0, color='gray', linestyle='-', linewidth=0.5) 
        plt.axvline(x=0, color='gray', linestyle='-', linewidth=0.5)
        plt.grid(color='lightgray', linestyle='--', linewidth=0.5) 
        plt.plot(self.R[0], self.L[0], color='Red', marker='o', markersize=8, label='Punkt początkowy')
        plt.legend() 

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":

    # Niezależnie od początkowych uczuć (R_0, L_0), 
    # emocje obojga z czasem całkowicie wygasają do zera (obojętności).
    #przyklad = Lab01(R_0=1, L_0=1, a_R=0.5, a_L=0.7, p_R=0.2, p_L=0.5)
    #przyklad.simulation(days=100) 
    #przyklad.drawPlot()
  
    #przyklad = Lab01(R_0=-1, L_0=1, a_R=0.5, a_L=0.7, p_R=0.2, p_L=0.5)
    #przyklad.simulation(days=100) 
    #przyklad.drawPlot()

    #przyklad = Lab01(R_0=-1, L_0=-1, a_R=0.5, a_L=0.7, p_R=0.2, p_L=0.5)
    #przyklad.simulation(days=100) 
    #przyklad.drawPlot()
 
    # Uczucia gwałtownie rosną w nieskończoność,
    # przy starcie z wartości dodatnich w stronę coraz silniejszej miłości, 
    # a z ujemnych w stronę wiekszej nienawiści.
    zadanie1 = Lab01(R_0=1, L_0=1, a_R=0.5, a_L=0.7, p_R=0.7, p_L=0.9)
    zadanie1.simulation(days=100) 
    zadanie1.drawPlot()

    #zadanie1 = Lab01(R_0=-1, L_0=1, a_R=0.5, a_L=0.7, p_R=0.7, p_L=0.9)
    #zadanie1.simulation(days=100) 
    #zadanie1.drawPlot()

    #zadanie1 = Lab01(R_0=-1, L_0=2, a_R=0.5, a_L=0.7, p_R=0.7, p_L=0.9)
    #zadanie1.simulation(days=100) 
    #zadanie1.drawPlot()

    # Para wpada w niekończącą się huśtawkę nastrojów (na zmianę miłość i nienawiść), 
    # a siła tych emocji z każdym kolejnym cyklem coraz bardziej rośnie (spirala się rozkręca).
    #zadanie2 = Lab01(R_0=1, L_0=1, a_R=1, a_L=1, p_R=0.2, p_L=-0.2)
    #zadanie2.simulation(days=100) 
    #zadanie2.drawPlot()

    #zadanie2 = Lab01(R_0=-1, L_0=1, a_R=1, a_L=1, p_R=0.2, p_L=-0.2)
    #zadanie2.simulation(days=100) 
    #zadanie2.drawPlot()

    #zadanie2 = Lab01(R_0=-1, L_0=2, a_R=1, a_L=1, p_R=0.2, p_L=-0.2)
    #zadanie2.simulation(days=100) 
    #zadanie2.drawPlot()

    # Po kilkunastu dniach uczucia zatrzymują się na stałym poziomie,
    # a ostateczna siła uczuć zależy od tego, z jakich wartości para wystartowała.
    #zadanie3 = Lab01(R_0=1, L_0=1, a_R=0.5, a_L=0.8, p_R=0.2, p_L=0.5)
    #zadanie3.simulation(days=100) 
    #zadanie3.drawPlot()

    #zadanie3 = Lab01(R_0=-1, L_0=1, a_R=0.5, a_L=0.8, p_R=0.2, p_L=0.5)
    #zadanie3.simulation(days=100) 
    #zadanie3.drawPlot()

    #zadanie3 = Lab01(R_0=-1, L_0=2, a_R=0.5, a_L=0.8, p_R=0.2, p_L=0.5)
    #zadanie3.simulation(days=100) 
    #zadanie3.drawPlot()