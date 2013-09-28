#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# César Amador - camador.git@gmail.com 
#
# Licenciado bajo Creative Commons Reconocimiento 3.0 Unported: http://creativecommons.org/licenses/by/3.0/deed.es_ES
#

class Jugador:
    """
        Clase que representa una jugada desde el punto de vista del jugador, abarcando de Preflop 
        a River e incluyendo la valoración de fuerza
    """

    def __init__(self):
        """
            Inicializa el objeto
        """
    
        # Cartas del jugador
        self.cartas = list()
        
        # Valoración de cada mano (preflop, flop, turn y river):
        # 0 - Sin valorar
        # 1 - Nada (N)
        # 2 - Mano Débil (MD)
        # 3 - Mano Media (MM)
        # 4 - Mano Fuerte (MF)
        # 5 - Mano Muy Fuerte (MMF)
        self.valoracion = [0, 0, 0, 0]

        # Revisión de la valoración de la jugada por cada paso (Flop, Turn y River)
        # 0 -> Incorrecto
        # 1 -> Correcto
        self.revision = [None, None, None]

        # Marcador para indicar si la jugada ha sido revisada
        self.revisada = False

    def revision_pleno(self):
        """
            Devuelve True si el jugador ha acertado en todas las valoraciones
        """

        # Valor a devolver
        pleno = True

        # Recorre la lista de revisiones y cambia el valor de 'pleno' cuando encuentra
        # un error o un paso sin valorar
        for paso in range(3):
            if self.revision[paso] != 1:
                pleno = False
    
        return pleno

if __name__ == '__main__':
    print u'Módulo no ejecutable.'
