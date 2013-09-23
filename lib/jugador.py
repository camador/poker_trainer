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

    def inicializa_valoracion(self):
        """
            Inicializa la valoración de fuerza de la jugada
        """

        self.valoracion = [0, 0, 0, 0]
    

if __name__ == '__main__':
    print u'Módulo no ejecutable.'
