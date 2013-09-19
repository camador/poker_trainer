#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# César Amador - camador.git@gmail.com 
#
# Licenciado bajo Creative Commons Reconocimiento 3.0 Unported: http://creativecommons.org/licenses/by/3.0/deed.es_ES
#

class Config():
    """
        Valores de configuración del juego
    """

    # Pasos
    PASOS = ['FLOP', 'TURN', 'RIVER', 'PREFLOP']

    # Cartas
    CARTAS = [
                {'imagen': 'Blue_Back', 'nombre': 'Reverso'},

                {'imagen': 'ace_of_spades', 'nombre': 'As'},
                {'imagen': '2_of_spades', 'nombre': '2s'},
                {'imagen': '3_of_spades', 'nombre': '3s'},
                {'imagen': '4_of_spades', 'nombre': '4s'},
                {'imagen': '5_of_spades', 'nombre': '5s'},
                {'imagen': '6_of_spades', 'nombre': '6s'},
                {'imagen': '7_of_spades', 'nombre': '7s'},
                {'imagen': '8_of_spades', 'nombre': '8s'},
                {'imagen': '9_of_spades', 'nombre': '9s'},
                {'imagen': '10_of_spades', 'nombre': '10s'},
                {'imagen': 'jack_of_spades', 'nombre': 'Js'},
                {'imagen': 'queen_of_spades', 'nombre': 'Qs'},
                {'imagen': 'king_of_spades', 'nombre': 'Ks'},

                {'imagen': 'ace_of_hearts', 'nombre': 'Ah'},
                {'imagen': '2_of_hearts', 'nombre': '2h'},
                {'imagen': '3_of_hearts', 'nombre': '3h'},
                {'imagen': '4_of_hearts', 'nombre': '4h'},
                {'imagen': '5_of_hearts', 'nombre': '5h'},
                {'imagen': '6_of_hearts', 'nombre': '6h'},
                {'imagen': '7_of_hearts', 'nombre': '7h'},
                {'imagen': '8_of_hearts', 'nombre': '8h'},
                {'imagen': '9_of_hearts', 'nombre': '9h'},
                {'imagen': '10_of_hearts', 'nombre': '10h'},
                {'imagen': 'jack_of_hearts', 'nombre': 'Jh'},
                {'imagen': 'queen_of_hearts', 'nombre': 'Qh'},
                {'imagen': 'king_of_hearts', 'nombre': 'Kh'},

                {'imagen': 'ace_of_diamonds', 'nombre': 'Ad'},
                {'imagen': '2_of_diamonds', 'nombre': '2d'},
                {'imagen': '3_of_diamonds', 'nombre': '3d'},
                {'imagen': '4_of_diamonds', 'nombre': '4d'},
                {'imagen': '5_of_diamonds', 'nombre': '5d'},
                {'imagen': '6_of_diamonds', 'nombre': '6d'},
                {'imagen': '7_of_diamonds', 'nombre': '7d'},
                {'imagen': '8_of_diamonds', 'nombre': '8d'},
                {'imagen': '9_of_diamonds', 'nombre': '9d'},
                {'imagen': '10_of_diamonds', 'nombre': '10d'},
                {'imagen': 'jack_of_diamonds', 'nombre': 'Jd'},
                {'imagen': 'queen_of_diamonds', 'nombre': 'Qd'},
                {'imagen': 'king_of_diamonds', 'nombre': 'Kd'},

                {'imagen': 'ace_of_clubs', 'nombre': 'Ac'},
                {'imagen': '2_of_clubs', 'nombre': '2c'},
                {'imagen': '3_of_clubs', 'nombre': '3c'},
                {'imagen': '4_of_clubs', 'nombre': '4c'},
                {'imagen': '5_of_clubs', 'nombre': '5c'},
                {'imagen': '6_of_clubs', 'nombre': '6c'},
                {'imagen': '7_of_clubs', 'nombre': '7c'},
                {'imagen': '8_of_clubs', 'nombre': '8c'},
                {'imagen': '9_of_clubs', 'nombre': '9c'},
                {'imagen': '10_of_clubs', 'nombre': '10c'},
                {'imagen': 'jack_of_clubs', 'nombre': 'Jc'},
                {'imagen': 'queen_of_clubs', 'nombre': 'Qc'},
                {'imagen': 'king_of_clubs', 'nombre': 'Kc'}
            ]

if __name__ == '__main__':
    print u'Módulo no ejecutable.'
