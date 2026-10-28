import matplotlib.pyplot as plt

# analiza modelu nieliniowego drapieznik - ofiara
class Lab03:
    def __init__(self, 
                 P_0: float, 
                 Q_0: float, 
                 r: float, 
                 u: float, 
                 s: float,
                 a: float, 
                 K: float):
        self.N = 100 # liczba generacji
        self.P_0 = P_0 # poczatkowa gestosc krolikow
        self.Q_0 = Q_0 # poczatkowa gestosc lisow
        self.r = r # wspolczynnik wzrostu populacji krolikow
        self.u = u # wspolczynnik smiertelnosci lisow
        self.s = s # wspolczynnik skutecznosci ataku
        self.a = a # liczba urodzen lisow na atak
        self.K = K # pojemnosc srodowiska dla krolikow

        self.P = [self.P_0]
        self.Q = [self.Q_0]
        self.t = [0]

        self.P_star = self.u / (self.s * self.a)
        self.Q_star = (self.r * (1 - (self.u / (self.s * self.a * self.K)))) / self.s

        self.fixed_points = [
            (0.0, 0.0),
            (self.K, 0.0),
            (self.P_star, self.Q_star)
        ]

    def theory(self, jacobian, fixed_points, filename="wnioski.txt"):
        """
        metoda analizujaca punkty stale za pomoca warunkow Jury'ego dla ukladu 2D.
        argumenty:
        - jacobian: funkcja przyjmujaca punkt staly i zwracajaca macierz 2x2: [[J11, J12], [J21, J22]]
        - fixed_points: lista punktow stalych
        - filename: nazwa pliku tekstowego do zapisu wnioskow.
        """
    
        lines = []
        lines.append("ANALIZA TEORETYCZNA PUNKTOW STALYCH UKLADU (WARUNKI JURY'EGO)")
        lines.append(" ")
        lines.append("Przypomnienie warunkow Jury'ego dla stabilnosci punktu stalego:")
        lines.append("  Warunek 1: |tr(J)| < 1 + det(J)")
        lines.append("  Warunek 2: det(J) < 1")
        lines.append("Oba warunki musza zachodzic jednoczesnie, aby punkt staly byl stabilny.\n")

        for (x, y) in fixed_points:
            J = jacobian(x, y)
            j11, j12 = J[0][0], J[0][1]
            j21, j22 = J[1][0], J[1][1]

            tr_J = j11 + j22
            abs_tr_J = abs(tr_J)
            det_J = j11 * j22 - j12 * j21

            margin_1 = 1 + det_J - abs_tr_J
            condition_1 = margin_1 > 0

            margin_2 = 1 - det_J 
            condition_2 = margin_2 > 0

            delta = tr_J**2 - 4.0 * det_J  

            lines.append("----------------------------------------------------------------------")
            lines.append(f"PUNKT STALY: (x*, y*) = ({x:.6f}, {y:.6f})")
            lines.append("----------------------------------------------------------------------")
           
            lines.append("Weryfikacja warunkow:")
            # Warunek 1
            if abs(margin_1) < 1e-9:
                c1_description = "Przypadek nierozstrzygajacy."
            elif condition_1:
                if margin_1 < 0.03:
                    c1_description = "SPELNIONY (DELIKATNIE)."
                elif margin_1 < 0.15:
                    c1_description = "SPELNIONY (WYRAZNIE)."
                else:
                    c1_description = "SPELNIONY (MOCNO)."
            else:
                if abs(margin_1) < 0.03:
                    c1_description = "NIESPELNIONY (DELIKATNIE)."
                elif abs(margin_1) < 0.2:
                    c1_description = "NIESPELNIONY (WYRAZNIE)."
                else:
                    c1_description = "NIESPELNIONY (MOCNO)."

            # Warunek 2
            if abs(margin_2) < 1e-9:
                c2_description = "Przypadek nierozstrzygajacy."
            elif condition_2:
                if margin_2 < 0.03:
                    c2_description = "SPELNIONY (DELIKATNIE)."
                elif margin_2 < 0.15:
                    c2_description = "SPELNIONY (WYRAZNIE)."
                else:
                    c2_description = "SPELNIONY (MOCNO)."
            else:
                if abs(margin_2) < 0.03:
                    c2_description = "NIESPELNIONY (DELIKATNIE)."
                elif abs(margin_2) < 0.2:
                    c2_description = "NIESPELNIONY (WYRAZNIE)."
                else:
                    c2_description = "NIESPELNIONY (MOCNO)."

            lines.append(f"   * Warunek 1 (|tr(J)| < 1 + det(J)):  {abs_tr_J:.6f} < {1+det_J:.6f}  --> {c1_description}")
            lines.append(f"   * Warunek 2 (det(J) < 1):            {det_J:.6f} < 1.000000  --> {c2_description}\n")

            lines.append("WERDYKT:")
            if condition_1 and condition_2:
                lines.append("   -> PUNKT STALY JEST STABILNY.")
                min_margin = min(margin_1, margin_2)
                if min_margin < 0.03:
                    speed_desc = "Wolne"
                elif min_margin < 0.15:
                    speed_desc = "Umiarkowane"
                else:
                    speed_desc = "Szybkie"
                lines.append(f"   -> Tempo zbiegania: {speed_desc}")
                if delta < 0:
                    lines.append("   -> Charakter ruchu: Spirala.")
                else:
                    lines.append("   -> Charakter ruchu: Normalnie.")

            elif abs(margin_1) < 1e-9 or abs(margin_2) < 1e-9:
                lines.append("   -> Warunek Jury'ego nie rozstrzyga.")

            else:
                lines.append("   -> PUNKT STALY JEST NIESTABILNY.")
                if condition_1 and not condition_2:
                    if abs(margin_2) < 0.03:
                        lines.append("   -> Odpychanie po wolno rozkrecajacej sie spirali.") 
                    else:
                        lines.append("   -> Odpychanie po szybko rozkrecajacej sie spirali.")
                elif not condition_1 and condition_2:
                    if abs(margin_1) < 0.03:
                        lines.append("   -> Siodlowe wolne odpychanie.") 
                    else:
                        lines.append("   -> Siodlowe szybkie odpychanie.") 
                else:
                    lines.append("   -> Odpychanie we wszystkich kierunkach - oba warunki nie zachodza.")

            lines.append("\n")

        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        
        print(f"Zapisano analize teoretyczna do pliku: {filename}")

    def simulation(self):
        for n in range(self.N):
            P_current = self.P[-1]
            Q_current = self.Q[-1]

            P_next = P_current * (1 + self.r * (1 - P_current / self.K)) - self.s * P_current * Q_current
            Q_next = (1 - self.u) * Q_current + self.a * self.s * P_current * Q_current
            
            self.P.append(P_next)
            self.Q.append(Q_next)
            self.t.append(n + 1)

    def drawPlot(self):       
        max_val = max(max(self.P), max(self.Q))
        
        plt.figure(figsize=(12, 6))

        # wykres 1
        plt.subplot(1, 2, 1)
        plt.plot(self.t, self.P, label='Kroliki (P)', color='Green', marker='.', linewidth=0.8, markersize=5)
        plt.plot(self.t, self.Q, label='Lisy (Q)', color='Red', linestyle='--', marker='.', linewidth=0.8, markersize=5)
        plt.title('Gestosc populacji w kolejnych generacjach')
        plt.xlabel('Generacje')
        plt.ylabel('Kroliki i lisy')
        plt.xlim(0, max(self.t)) 
        plt.ylim(0, max_val * 1.15)
        plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
        plt.legend()

        # wykres 2
        plt.subplot(1, 2, 2)
        plt.plot(self.P, self.Q, color='Black', marker='.', linewidth=0.6, markersize=5) 
        plt.title('Portret fazowy')
        plt.xlabel('Kroliki (P)')
        plt.ylabel('Lisy (Q)')
        
        min_P, max_P = min(min(self.P), self.P_star), max(max(self.P), self.P_star)
        min_Q, max_Q = min(min(self.Q), self.Q_star), max(max(self.Q), self.Q_star)
        span_P = max(max_P - min_P, 0.01)
        span_Q = max(max_Q - min_Q, 0.01)
        
        plt.xlim(max(0, min_P - 0.15 * span_P), max_P + 0.15 * span_P)
        plt.ylim(max(0, min_Q - 0.15 * span_Q), max_Q + 0.15 * span_Q)
        plt.grid(color='lightgray', linestyle='--', linewidth=0.5) 
        plt.plot(self.P[0], self.Q[0], color='Red', marker='o', markersize=8, label='Punkt poczatkowy')
        plt.plot(self.P_star, self.Q_star, color='Gold', marker='X', markersize=9, markeredgecolor='black', label='Punkt staly')

        plt.legend()
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    zadanie = Lab03(P_0=0.1, Q_0=0.2, r=0.5, u=0.2, s=2.2, a=0.9, K=0.7)
    zadanie.theory(
        jacobian=lambda P, Q: [
          [1 + zadanie.r - (2 * zadanie.r / zadanie.K) * P - zadanie.s * Q, -zadanie.s * P],
          [zadanie.a * zadanie.s * Q, 1 - zadanie.u + zadanie.a * zadanie.s * P]
        ],
        fixed_points=zadanie.fixed_points,
        filename="wnioski.txt"
    )
    zadanie.simulation() 
    zadanie.drawPlot()
