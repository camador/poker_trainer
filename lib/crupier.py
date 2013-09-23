#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# César Amador - camador.git@gmail.com 
#
# Licenciado bajo Creative Commons Reconocimiento 3.0 Unported: http://creativecommons.org/licenses/by/3.0/deed.es_ES
#

from random import randint

class Crupier:
    """
        Clase que representa una jugada desde el punto de vista del crupier, abarcando de Preflop 
        a River
    """


    def __init__(self, config):
        """
            Establece los valores iniciales
        """

        # Cartas repartidas
        self.cartas = list()

        # Pasos
        self.pasos = config.PASOS
        self.num_pasos = len(self.pasos)

        # Paso (Preflop, flop, turn y river)
        self.paso = 0

    def siguiente_paso(self):
        """
            Calcula, fija y devuelve el siguiente paso
        """
    
        self.paso += 1

        if self.paso == self.num_pasos:
            self.paso = 0

        return self.paso

    def repartir_carta(self):
        """
            Genera y devuelve una carta aleatoria de las que todavía no han sido repartidas 
        """
        
        carta = False

        while not carta:

            # Genera la carta aleatoria
            carta = randint(1, 52)

            try:
                # Comprueba que la carta no haya sido ya repartida
                self.cartas.index(carta)
                
                # La carta existe, busca otra
                carta = False 

            except:

                # La carta no existe, la guarda en las cartas ya repartidas
                self.cartas.append(carta)

        return carta 

if __name__ == '__main__':
    print u'Módulo no ejecutable.'
