#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# César Amador - camador.git@gmail.com 
#
# Licenciado bajo Creative Commons Reconocimiento 3.0 Unported: http://creativecommons.org/licenses/by/3.0/deed.es_ES
#

# PyQt
from PyQt4 import uic, QtGui, QtCore

# Config
from lib.config import Config 

# Otros
import sys
import os
from random import randint

class GUI(QtGui.QWidget):
    """
        Interfaz gráfica de usuario 
    """

    def __init__(self):

        # Antes de nada crea el objeto 'aplicación' de Qt
        self.app = QtGui.QApplication(sys.argv)

        # Inicicializa el ancestro
        QtGui.QWidget.__init__(self)

        # Fija el nombre de la aplicación
        self.app.setApplicationName('Poker Trainer')
        
        # Lee el fichero que contiene la interfaz gráfica
        self.ui = uic.loadUi(os.path.join('lib', 'gui.ui'))

        #
        # Lee los widgets y los asigna a variables
        #

        # Botón Salir
        self.pushbutton_salir = self.ui.findChild(QtGui.QPushButton, "pbtSalir")

        # Botón Paso
        self.pushbutton_paso = self.ui.findChild(QtGui.QPushButton, "pbtPaso")

        # Cartas de la mesa
        self.label_mesa_carta_1 = self.ui.findChild(QtGui.QLabel, 'lblMesaCarta1')
        self.label_mesa_carta_2 = self.ui.findChild(QtGui.QLabel, 'lblMesaCarta2')
        self.label_mesa_carta_3 = self.ui.findChild(QtGui.QLabel, 'lblMesaCarta3')
        self.label_mesa_carta_4 = self.ui.findChild(QtGui.QLabel, 'lblMesaCarta4')
        self.label_mesa_carta_5 = self.ui.findChild(QtGui.QLabel, 'lblMesaCarta5')
        
        # Cartas del juegador
        self.label_jugador_carta_1 = self.ui.findChild(QtGui.QLabel, 'lblJugadorCarta1')
        self.label_jugador_carta_2 = self.ui.findChild(QtGui.QLabel, 'lblJugadorCarta2')

        #
        # Conecta las señales
        #

        # Botón Salir
        self.pushbutton_salir.clicked.connect(self.on_salir)

        # Botón Paso
        self.pushbutton_paso.clicked.connect(self.on_paso)

        #
        # Configuración
        #
        self.config = Config()

        # Paso actual
        self.paso = 0

        # Número de pasos
        self.num_pasos = len(self.config.PASOS)

        # Cartas de la mesa
        self.cartas_mesa = list()

        # Cartas del jugador
        self.cartas_jugador = list()

        # Cartas repartidas
        self.cartas_repartidas = list()


    ##
    ## MAIN
    ##
    def main(self):
        """
            Método de inicio)
        """
        
        #
        # Estado inicial del interfaz
        #

        # Texto para el botón de los pasos
        self.set_paso(self.paso)

        # Primer paso: preflop
        self.preflop()


        # Muestra la ventana principal
        self.ui.show()

        # A la espera de evento
        self.app.exec_()
    
    ##
    ## VENTANA PRINCIPAL
    ##
    def window_main_destroy(self):
        """
            Termina la ejecución del programa
        """

        # Saliendo
        sys.exit()

    ##
    ## SALIR
    ##
    @QtCore.pyqtSlot()
    def on_salir(self):
        """
            Termina la ejecución del programa
        """

        # Sale
        self.window_main_destroy()

    ##
    ## PASO 
    ##
    @QtCore.pyqtSlot()
    def on_paso(self):
        """
            Avanza hasta el siguiente paso con las siguientes acciones:
            - FLOP: Reparte tres cartas en la mesa
            - TURN: Reparte la cuarta carta en la mesa
            - RIVER: Reparte la quinta carta en la mesa
            - PREFLOP: Reinicia las manos recogiendo todas las cartas, barajando y repartiendo dos
                       nuevas cartas al jugador
        """

        # Establece el siguiente paso y fija el texto correspondiente para el botón de los pasos
        self.set_paso(self.get_siguiente_paso())

        if self.paso == 1:
            self.flop()

        elif self.paso == 2:
            self.turn()

        elif self.paso == 3:
            self.river()

        else:
            self.preflop()

    def preflop(self):
        """
            Dos cartas para el jugador, ninguna en la mesa 
        """

        # Se recogen y barajan todas las cartas
        self.cartas_mesa = list()
        self.cartas_jugador = list()
        self.cartas_repartidas = list()
    
        # Cartas de la mesa
        self.label_mesa_carta_1.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(0)))
        self.label_mesa_carta_2.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(0)))
        self.label_mesa_carta_3.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(0)))
        self.label_mesa_carta_4.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(0)))
        self.label_mesa_carta_5.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(0)))

        # Cartas del jugador
        self.cartas_jugador.insert(0, self.generar_carta())
        self.cartas_jugador.insert(1, self.generar_carta())
        
        self.label_jugador_carta_1.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(self.cartas_jugador[0])))
        self.label_jugador_carta_2.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(self.cartas_jugador[1])))

    def flop(self):
        """ 
            Tres cartas en la mesa
        """ 

        # Genera las cartas
        self.cartas_mesa.insert(0, self.generar_carta())
        self.cartas_mesa.insert(1, self.generar_carta())
        self.cartas_mesa.insert(2, self.generar_carta())
        
        # Y las muestras
        self.label_mesa_carta_1.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(self.cartas_mesa[0])))
        self.label_mesa_carta_2.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(self.cartas_mesa[1])))
        self.label_mesa_carta_3.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(self.cartas_mesa[2])))

    def turn(self):
        """ 
            Cuarta carta de la mesa
        """ 

        # Genera la carta
        self.cartas_mesa.insert(3, self.generar_carta())
        
        # Y la muestra
        self.label_mesa_carta_4.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(self.cartas_mesa[3])))

    def river(self):
        """ 
            Quinta carta de la mesa
        """ 

        # Genera la carta
        self.cartas_mesa.insert(4, self.generar_carta())
        
        # Y la muestra
        self.label_mesa_carta_5.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(self.cartas_mesa[4])))
           
    
    ##
    ## MÉTODOS AUXILIARES
    ##
    def set_paso(self, paso = 0):
        """
            Establece el texto del botón de los pasos según el valor del parámetro recibido 
        """
        self.pushbutton_paso.setText(self.config.PASOS[paso])


    def get_siguiente_paso(self):
        """
            Calcula, fija y devuelve el siguiente paso
        """
    
        self.paso += 1

        if self.paso == self.num_pasos:
            self.paso = 0

        return self.paso

    def generar_carta(self):
        """
            Genera y devuelve una carta aleatoria de las que todavía no han sido repartidas 
        """
        
        carta = False

        while not carta:

            # Genera la carta aleatoria
            carta = randint(1, 52)

            try:
                # Comprueba que la carta no haya sido ya repartida
                self.cartas_repartidas.index(carta)
                
                # La carta existe, busca otra
                carta = False 

            except:

                # La carta no existe, la guarda en las cartas ya repartidas
                self.cartas_repartidas.append(carta)

        return carta 
        

if __name__ == '__main__':
    print u'Módulo no ejecutable.'
