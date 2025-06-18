from manim import *
import numpy as np

class PlanoInclinadoFisico(Scene):
    def construct(self):
        # Parámetros
        altura = 300  # metros
        base = 400  # metros
        g = 9.8
        radio = base*0.016  # metros

        # Cálculo del ángulo y aceleración
        theta = np.arctan(altura / base)
        a = g * np.sin(theta)

        # Distancia 
        distancia_real = np.sqrt(altura**2 + base**2)

        # Tiempo físico 
        tiempo_total = np.sqrt(2 * distancia_real / a)

       
        duracion = tiempo_total + 2

        # Escalado 
        escala = 7 / max(base, altura)

       
        punto_superior = (LEFT * base / 2 + UP * altura / 2) * escala
        punto_inferior = (RIGHT * base / 2 + DOWN * altura / 2) * escala

        direccion = punto_inferior - punto_superior
        direccion = direccion / np.linalg.norm(direccion)
        perpendicular = np.array([-direccion[1], direccion[0], 0])

        punto_inicial = punto_superior + perpendicular * radio * escala
        punto_final = punto_inferior + perpendicular * radio * escala

        
        rampa = Line(punto_superior, punto_inferior, color=WHITE, stroke_width=6)
        esfera = Circle(radius=radio * escala, color=BLUE, fill_opacity=1).move_to(punto_inicial)

        # Texto 
        texto = VGroup(
            Text(f"Altura: {altura}", font_size=32),
            Text(f"Base: {base}", font_size=32),
            Text(f"Ángulo: {np.degrees(theta):.2f}°", font_size=32),
            Text(f"Aceleración: {a:.2f} m/s²", font_size=32),
            Text(f"Tiempo total: {tiempo_total:.2f} s", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.5).to_corner(DL)

        self.add(rampa, esfera, texto)

        # Movimiento 
        def actualizar_posicion(mob, dt):
            if not hasattr(mob, "tiempo"):
                mob.tiempo = 0
            mob.tiempo += dt

            s = 0.5 * a * mob.tiempo**2  
            if s > distancia_real:
                s = distancia_real

            nueva_pos = punto_inicial + direccion * s * escala  
            mob.move_to(nueva_pos)

        esfera.add_updater(actualizar_posicion)
        self.play(Wait(duracion))
        esfera.remove_updater(actualizar_posicion)
        self.wait(1)