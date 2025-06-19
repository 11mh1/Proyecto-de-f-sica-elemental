from manim import *
import numpy as np

class IntegracionCinematica(Scene):
    def construct(self):
        def a(t): return 2.82  # Funcion
        t0 = 0
        t1 = 0.61

        def v(t): return self.integral_numerica(a, t0, t)
        def x(t): return self.integral_numerica(v, t0, t)

        x_max = max(3, t1 + 0.5)
        y_max = np.ceil(max(5, a(t1), v(t1), x(t1)) + 2)

        ejes = Axes(
            x_range=[t0, x_max, 0.5],
            y_range=[0, y_max, self.salto_y(y_max)],
            x_length=7,
            y_length=5,
            axis_config={
                "include_numbers": True,
                "font_size": 24
            },
            tips=False
        ).to_edge(DOWN)

        self.play(Create(ejes))

        self.mostrar_funcion(ejes, a, t0, t1, "a(t)", color=BLUE)
        self.mostrar_funcion(ejes, v, t0, t1, "v(t)", color=GREEN)
        self.mostrar_funcion(ejes, x, t0, t1, "x(t)", color=ORANGE)

        self.wait(2)

    def integral_numerica(self, func, a, b):
        dx = 0.01
        if b <= a:
            return 0
        x_vals = np.arange(a, b, dx)
        y_vals = np.array([func(xi) for xi in x_vals])
        return np.trapz(y_vals, x_vals)

    def mostrar_funcion(self, ejes, funcion, a, b, nombre, color):
        curva = ejes.plot(
            funcion,
            x_range=[a, b],
            color=color,
            use_smoothing=False
        )
        area = ejes.get_area(curva, x_range=(a, b), color=color, opacity=0.4)

        
        etiqueta = MathTex(nombre, color=color).to_corner(UL)

        
        etiquetas_titulo = {
            "a(t)": "Gráfica de la aceleración",
            "v(t)": "Gráfica de la velocidad",
            "x(t)": "Gráfica de la posición"
        }
        texto = Text(etiquetas_titulo.get(nombre, nombre), font_size=36).to_edge(UP)

        # Punto rojo 
        punto_final = Dot(
            ejes.c2p(b, funcion(b)),
            color=RED,
            radius=0.08
        )
        etiqueta_valor = MathTex(
            f"{nombre[:-3]}({b}) = {funcion(b):.2f}", color=RED
        ).scale(0.7).next_to(punto_final, UP)

        # Animaciones
        self.play(Write(etiqueta))
        self.play(Create(curva), run_time=2)
        self.play(FadeIn(area), run_time=2)
        self.play(FadeIn(punto_final), FadeIn(etiqueta_valor))
        self.play(Write(texto))
        self.wait(2)
        self.play(*[
            FadeOut(mob) for mob in
            [curva, area, etiqueta, texto, punto_final, etiqueta_valor]
        ])

    def salto_y(self, y_max):
        if y_max <= 4:
            return 1
        elif y_max <= 8:
            return 2
        elif y_max <= 15:
            return 5
        else:
            return 10
