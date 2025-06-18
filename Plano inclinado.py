from manim import *
import numpy as np

class PlanoInclinadoFisico(Scene):
    def construct(self):
        # Parámetros iniciales
        altura = 30
        base = 40
        g = 9.8
        radio = 0.2

        # Cálculo del ángulo y aceleración
        theta = np.arctan(altura / base)
        a = g * np.sin(theta)

        # Puntos del plano
        punto_inferior = RIGHT * base / 2 + DOWN * altura / 2
        punto_superior = LEFT * base / 2 + UP * altura / 2

        direccion = punto_inferior - punto_superior
        direccion = direccion / np.linalg.norm(direccion)
        perpendicular = np.array([-direccion[1], direccion[0], 0])

        punto_inicial = punto_superior + perpendicular * radio
        punto_final = punto_inferior + perpendicular * radio
        distancia_total = np.linalg.norm(punto_final - punto_inicial)

        # Tiempo total de caída (MRUV)
        tiempo_total = np.sqrt(2 * distancia_total / a)

        # Duración total del video
        duracion = tiempo_total + 2

        # Escalado para visualización
        escala = 7 / max(base, altura)

        # Crear la rampa y la esfera
        rampa = Line(punto_superior, punto_inferior, color=WHITE, stroke_width=6).scale(escala)
        esfera = Circle(radius=radio, color=BLUE, fill_opacity=1).move_to(punto_inicial).scale(escala)

        # Texto fijo informativo
        texto = VGroup(
            Text(f"Altura: {altura}", font_size=32),
            Text(f"Base: {base}", font_size=32),
            Text(f"Ángulo: {np.degrees(theta):.2f}°", font_size=32),
            Text(f"Aceleración: {a:.2f} m/s²", font_size=32),
            Text(f"Tiempo total: {tiempo_total:.2f} s", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.5).to_corner(DL)

        # Añadir objetos a la escena
        self.add(rampa, esfera, texto)

        # Movimiento MRUV
        def actualizar_posicion(mob, dt):
            if not hasattr(mob, "tiempo"):
                mob.tiempo = 0
            mob.tiempo += dt

            s = 0.5 * a * mob.tiempo ** 2
            if s > distancia_total:
                s = distancia_total
            nueva_pos = punto_inicial + direccion * s
            mob.move_to(nueva_pos * escala)

        esfera.add_updater(actualizar_posicion)
        self.play(Wait(duracion))
        esfera.remove_updater(actualizar_posicion)
        self.wait(1)
