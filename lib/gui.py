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

        #
        # Configuración
        #
        self.config = Config()

        # Paso actual
        self.paso = 0

        # Número de pasos
        self.num_pasos = len(self.config.PASOS)

        # Fuerzas de las jugadas
        # Las fuerzas de cada jugada (fuerzas) se guarda en fuerzas_jugadas
        self.fuerzas = [0, 0, 0, 0]
        self.fuerzas_jugadas = list()

        # Cartas de la mesa
        self.cartas_mesa = list()

        # Cartas del jugador
        self.cartas_jugador = list()

        # Cartas repartidas
        self.cartas_repartidas = list()

        #
        # GUI
        #

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
        self.pushbutton_salir = self.ui.findChild(QtGui.QPushButton, 'pbtSalir')

        # Botón Paso
        self.pushbutton_paso = self.ui.findChild(QtGui.QPushButton, 'pbtPaso')

        # Botones para la fuerza de la jugada
        self.pushbutton_fuerza5 = self.ui.findChild(QtGui.QPushButton, 'pbtFuerza5')
        self.pushbutton_fuerza4 = self.ui.findChild(QtGui.QPushButton, 'pbtFuerza4')
        self.pushbutton_fuerza3 = self.ui.findChild(QtGui.QPushButton, 'pbtFuerza3')
        self.pushbutton_fuerza2 = self.ui.findChild(QtGui.QPushButton, 'pbtFuerza2')
        self.pushbutton_fuerza1 = self.ui.findChild(QtGui.QPushButton, 'pbtFuerza1')

        # Cartas de la mesa
        self.label_mesa_carta_1 = self.ui.findChild(QtGui.QLabel, 'lblMesaCarta1')
        self.label_mesa_carta_2 = self.ui.findChild(QtGui.QLabel, 'lblMesaCarta2')
        self.label_mesa_carta_3 = self.ui.findChild(QtGui.QLabel, 'lblMesaCarta3')
        self.label_mesa_carta_4 = self.ui.findChild(QtGui.QLabel, 'lblMesaCarta4')
        self.label_mesa_carta_5 = self.ui.findChild(QtGui.QLabel, 'lblMesaCarta5')
        
        # Cartas del jugador
        self.label_jugador_carta_1 = self.ui.findChild(QtGui.QLabel, 'lblJugadorCarta1')
        self.label_jugador_carta_2 = self.ui.findChild(QtGui.QLabel, 'lblJugadorCarta2')

        # Lista de jugadas
        self.dockwidget_jugadas = self.ui.findChild(QtGui.QDockWidget, 'dckJugadas')
        self.listview_jugadas = self.ui.findChild(QtGui.QListView, 'lsvJugadas')
        self.model_jugadas = QtGui.QStandardItemModel(self.listview_jugadas)
        self.listview_jugadas.setModel(self.model_jugadas)

        #
        # Conecta las señales
        #

        # Botón Salir
        self.pushbutton_salir.clicked.connect(self.on_salir)

        # Botón Paso
        self.pushbutton_paso.clicked.connect(self.on_paso)

        # Botones para la fuerza de la jugada
        # lambda porque la función tiene parámetros
        self.pushbutton_fuerza5.clicked.connect(lambda: self.on_fuerza(5))
        self.pushbutton_fuerza4.clicked.connect(lambda: self.on_fuerza(4))
        self.pushbutton_fuerza3.clicked.connect(lambda: self.on_fuerza(3))
        self.pushbutton_fuerza2.clicked.connect(lambda: self.on_fuerza(2))
        self.pushbutton_fuerza1.clicked.connect(lambda: self.on_fuerza(1))


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

        # Guarda las fuerzas de la anterior jugada, si la hay
        num_jugadas = self.model_jugadas.rowCount()
        if num_jugadas > 0:
            self.fuerzas_jugadas.insert(num_jugadas, self.fuerzas)
            self.fuerzas = [0, 0, 0, 0]

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
    
        #
        # Actualiza la lista de jugadas
        #

        # Número de jugadas de la lista. En este momento todavía no ha sido añadida la jugada actual.
        num_jugadas = str(self.model_jugadas.rowCount() + 1)
        
        # Formato del item: 
        #
        #  Nº de jugada - Cartas del jugador - Cartas de la mesa
        #  1 - Ks 3h - Jc Ad 3s 7c Kh
        jugada = num_jugadas + ' - '
        jugada += self.config.CARTAS[self.cartas_jugador[0]]['nombre'] + ' '
        jugada += self.config.CARTAS[self.cartas_jugador[1]]['nombre']
        jugada += ' - '
        jugada += self.config.CARTAS[self.cartas_mesa[0]]['nombre'] + ' '
        jugada += self.config.CARTAS[self.cartas_mesa[1]]['nombre'] + ' '
        jugada += self.config.CARTAS[self.cartas_mesa[2]]['nombre'] + ' '
        jugada += self.config.CARTAS[self.cartas_mesa[3]]['nombre'] + ' '
        jugada += self.config.CARTAS[self.cartas_mesa[4]]['nombre']

        # Crea el item y lo añade a la lista
        item = QtGui.QStandardItem(jugada)
        self.model_jugadas.appendRow(item)

        # Actualiza el título de la lista con el contador de jugadas
        self.dockwidget_jugadas.setWindowTitle('Jugadas (' + num_jugadas + ')')

    ##
    ## FUERZA
    ##
    def on_fuerza(self, fuerza):
        """
            Establece la fuerza de la jugada para el paso actual
        """

        # Fuerza asignada al paso anterior
        self.fuerzas[self.paso] = fuerza

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
