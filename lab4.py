import matplotlib.pyplot as plt
import math

class Lab04:
    def __init__(self, P0, Q0, r, u, s, a, K):
        # poczatkowe wartosci:
        self.P0 = P0
        self.Q0 = Q0

        # parametry:
        self.r = r
        self.u = u
        self.s = s
        self.a = a
        self.K = K

        # punkty stałe:
        self.P_star = self.u / (self.s * self.a)
        self.Q_star = (self.r / self.s) * (1 - self.u / (self.s * self.a * self.K))
        self.fixed_points = [(0.0, 0.0), (self.K, 0.0), (self.P_star, self.Q_star)  ]

    # ofiara/krolik: dP/dt = f1
    def f1(self, P, Q):
        return self.r * P * (1 - P / self.K) - self.s * P * Q

    # drapieznik/lis: dQ/dt = f2
    def f2(self, P, Q):
        return -self.u * Q + self.a * self.s * P * Q

    def jacobian(self, P, Q):
        j11 = self.r - (2 * self.r * P / self.K) - self.s * Q
        j12 = -self.s * P
        j21 = self.a * self.s * Q
        j22 = -self.u + self.a * self.s * P
        return [[j11, j12], [j21, j22]]

    def theory(self, filename="wnioski_lab4.txt"):
        lines = []
        lines.append("ANALIZA TEORETYCZNA UKLADU CIAGLEGO")
        lines.append("Warunki stabilności dla układu ciaglego:")
        lines.append(" 1. Slad: tr(J) = j11 + j22")
        lines.append(" 2. Wyznacznik: det(J) = j11*j22 - j12*j21")
        lines.append(" 3. Wyroznik: tr(J)**2 - 4det(J)\n")

        for (x, y) in self.fixed_points:
            J = self.jacobian(x, y)
            tr_J = J[0][0] + J[1][1]
            det_J = J[0][0] * J[1][1] - J[0][1] * J[1][0]
            delta = tr_J**2 - 4 * det_J

            lines.append(f"PUNKT STALY: (P*, Q*) = ({x:.4f}, {y:.4f})")
            lines.append(f" tr(J) = {tr_J:.4f}")
            lines.append(f" det(J) = {det_J:.4f}")
            lines.append(f" Delta = {delta:.4f}")

            if tr_J < 0 and det_J > 0:
                lines.append("Punkt STABILNY")
                if delta < 0:
                    lines.append("Ognisko.")
                else:
                    lines.append("Wezel.")
            else:
                lines.append("Punkt NIESTABILNY")
            if det_J < 0:
                lines.append("Siodlo.")
                
            lines.append("-" * 60)

        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
            print(f"Zapisano teoretyczna analize stabilnosci do pliku: {filename}")

# metody numeryczne:
    def euler(self, dt, T):
        t, P, Q = [0], [self.P0], [self.Q0]       
        N = int(T / dt)
        for n in range(N):
            try:
                Pn, Qn = P[-1], Q[-1]
                P_next = Pn + dt * self.f1(Pn, Qn)
                Q_next = Qn + dt * self.f2(Pn, Qn)
                P.append(P_next)
                Q.append(Q_next)
                t.append((n + 1) * dt)
            except OverflowError:
                break 
        return t, P, Q

    def rk2(self, dt, T):
        t, P, Q = [0], [self.P0], [self.Q0]
        N = int(T / dt)
        for n in range(N):
            try:
                Pn, Qn = P[-1], Q[-1]
                k1_P = self.f1(Pn, Qn)
                k1_Q = self.f2(Pn, Qn)
                k2_P = self.f1(Pn + dt * k1_P, Qn + dt * k1_Q)
                k2_Q = self.f2(Pn + dt * k1_P, Qn + dt * k1_Q)
                P.append(Pn + (dt / 2) * (k1_P + k2_P))
                Q.append(Qn + (dt / 2) * (k1_Q + k2_Q))
                t.append((n + 1) * dt)
            except OverflowError:
                break
        return t, P, Q

    def rk4(self, dt, T):
        t, P, Q = [0], [self.P0], [self.Q0]
        N = int(T / dt)
        for n in range(N):
            try:
                Pn, Qn = P[-1], Q[-1]
                k1_P = self.f1(Pn, Qn)
                k1_Q = self.f2(Pn, Qn)
                k2_P = self.f1(Pn + 0.5 * dt * k1_P, Qn + 0.5 * dt * k1_Q)
                k2_Q = self.f2(Pn + 0.5 * dt * k1_P, Qn + 0.5 * dt * k1_Q)
                k3_P = self.f1(Pn + 0.5 * dt * k2_P, Qn + 0.5 * dt * k2_Q)
                k3_Q = self.f2(Pn + 0.5 * dt * k2_P, Qn + 0.5 * dt * k2_Q)
                k4_P = self.f1(Pn + dt * k3_P, Qn + dt * k3_Q)
                k4_Q = self.f2(Pn + dt * k3_P, Qn + dt * k3_Q)

                P.append(Pn + (dt / 6) * (k1_P + 2*k2_P + 2*k3_P + k4_P))
                Q.append(Qn + (dt / 6) * (k1_Q + 2*k2_Q + 2*k3_Q + k4_Q))
                t.append((n + 1) * dt)
            except OverflowError:
                break
        return t, P, Q

    def draw_plots(self, case_label, dt, T, results, max_plot_t=None):
        t_euler, P_euler, Q_euler = results['euler']
        t_rk2, P_rk2, Q_rk2 = results['rk2']
        t_rk4, P_rk4, Q_rk4 = results['rk4']

        plot_t = max_plot_t if max_plot_t else T  # uciecie osi czasu

        fig, axs = plt.subplots(1, 3, figsize=(18, 5))
        fig.suptitle(f"punkt {case_label}: T={T}, dt={dt}", fontsize=16)

        # Portret fazowy:
        axs[0].plot(P_euler, Q_euler, label='Euler', color='black', marker='.', linewidth=0.3, markersize=3)
        axs[0].plot(P_rk2, Q_rk2, label='RK2', color='blue', marker='.', linewidth=0.3, markersize=3)
        axs[0].plot(P_rk4, Q_rk4, label='RK4', color='red', marker='.', linewidth=0.3, markersize=3)
        axs[0].plot(self.P0, self.Q0, color='Red', marker='o', markersize=8, label='Punkt poczatkowy')
        axs[0].plot(self.P_star, self.Q_star, 'X', color='Gold', markersize=10, label='Punkt rownowagi')
        axs[0].set_title('Portret fazowy')
        axs[0].set_xlabel('Kroliki (P)')
        axs[0].set_ylabel('Lisy (Q)')
        axs[0].grid(linestyle='--', alpha=0.6)
        axs[0].legend()
        axs[0].set_xlim(left=-0.1, right=max(1.2, min(2.0, max(P_euler) if P_euler else 1.2)))
        axs[0].set_ylim(bottom=-0.1, top=max(1.2, min(1.5, max(Q_euler) if Q_euler else 1.2)))

        # Kroliki w czasie: 
        axs[1].plot(t_euler, P_euler, label='Euler', color='black', marker='.', linewidth=0.8, markersize=3)
        axs[1].plot(t_rk2, P_rk2, label='RK2', color='blue', marker='.', linewidth=0.8, markersize=3)
        axs[1].plot(t_rk4, P_rk4, label='RK4', color='red', marker='.', linewidth=0.8, markersize=3)
        axs[1].axhline(self.P_star, color='magenta', linestyle='--', alpha=0.5, label='P*')
        axs[1].set_title('Kroliki w czasie (P)')
        axs[1].set_xlabel('Czas (t)')
        axs[1].set_ylabel('P(t)')
        axs[1].set_xlim(0, plot_t)
        axs[1].set_ylim(bottom=-0.1, top=max(1.2, min(2.0, max(P_rk4) if P_rk4 else 1.2)))
        axs[1].grid(linestyle='--', alpha=0.6)
        axs[1].legend()

        # Lisy w czasie:
        axs[2].plot(t_euler, Q_euler, label='Euler', color='black', marker='.', linewidth=0.8, markersize=5)
        axs[2].plot(t_rk2, Q_rk2, label='RK2', color='blue', marker='.', linewidth=0.8, markersize=5)
        axs[2].plot(t_rk4, Q_rk4, label='RK4', color='red', marker='.', linewidth=0.8, markersize=5)
        axs[2].axhline(self.Q_star, color='magenta', linestyle='--', alpha=0.5, label='Q*')
        axs[2].set_title('Lisy w czasie (Q)')
        axs[2].set_xlabel('Czas (t)')
        axs[2].set_ylabel('Q(t)')
        axs[2].set_xlim(0, plot_t)
        axs[2].set_ylim(bottom=-0.1, top=max(1.0, min(1.5, max(Q_rk4) if Q_rk4 else 1.0)))
        axs[2].grid(linestyle='--', alpha=0.6)
        axs[2].legend()

        plt.tight_layout()
        plt.show()

    def run_scenario(self, case_label, dt, T, max_plot_t=None):
        print(f"Obliczanie symulacji dla podpunktu {case_label} (dt={dt}, T={T})...")
        results = {'euler': self.euler(dt, T), 'rk2': self.rk2(dt, T), 'rk4': self.rk4(dt, T)}
        self.draw_plots(case_label, dt, T, results, max_plot_t)

if __name__ == "__main__":
    zadanie = Lab04(P0=0.3, Q0=0.9, r=1.2, u=0.2, s=2.0, a=0.5, K=1.0)
    zadanie.theory()

    #zadanie.run_scenario(case_label="(a)", dt=0.1, T=100) 
    #zadanie.run_scenario(case_label="(b)", dt=1.0, T=1000, max_plot_t=100) # LAB3
    #zadanie.run_scenario(case_label="(c)", dt=1.1, T=1000, max_plot_t=100)
    #zadanie.run_scenario(case_label="(d)", dt=3.0, T=1000, max_plot_t=100)
    zadanie.run_scenario(case_label="(e)", dt=3.2, T=1000, max_plot_t=100)