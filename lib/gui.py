#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# César Amador - camador.git@gmail.com 
#
# Licenciado bajo Creative Commons Reconocimiento 3.0 Unported: http://creativecommons.org/licenses/by/3.0/deed.es_ES
#

# PyQt
from PyQt4 import uic, QtGui, QtCore

# Póker
from lib.config import Config 
from lib.jugador import Jugador
from lib.mesa import Mesa
from lib.crupier import Crupier

# Otros
import sys
import os

class GUI(QtGui.QWidget):
    """
        Interfaz gráfica de usuario 
    """

    def __init__(self):

        #
        # Configuración
        #
        self.config = Config()

        # Instancia los objetos del jugador, mesa y crupier
        self.jugador = Jugador()
        self.mesa = Mesa()
        self.crupier = Crupier(self.config)

        # Lista de jugadas
        self.lista_jugadas = list()

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

        # Indicadores de la fuerza de las jugadas
        self.label_fuerza_flop = self.ui.findChild(QtGui.QLabel, 'lblFuerzaFlop')
        self.label_fuerza_turn = self.ui.findChild(QtGui.QLabel, 'lblFuerzaTurn')
        self.label_fuerza_river = self.ui.findChild(QtGui.QLabel, 'lblFuerzaRiver')

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

        # Lista de jugadas
        self.listview_jugadas.clicked.connect(self.on_jugada_clicked)


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
        self.set_paso(self.crupier.paso)

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
        self.set_paso(self.crupier.siguiente_paso())

        if self.crupier.paso == 1:
            self.flop()

        elif self.crupier.paso == 2:
            self.turn()

        elif self.crupier.paso == 3:
            self.river()

        else:
            self.preflop()

    def preflop(self):
        """
            Dos cartas para el jugador, ninguna en la mesa 
        """

        # Inicializa la mesa
        self.inicializa_mesa()

        # Cartas del jugador
        self.jugador.cartas.insert(0, self.crupier.repartir_carta())
        self.jugador.cartas.insert(1, self.crupier.repartir_carta())
        
        self.label_jugador_carta_1.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(self.jugador.cartas[0])))
        self.label_jugador_carta_2.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(self.jugador.cartas[1])))

    def flop(self):
        """ 
            Tres cartas en la mesa
        """ 
        
        # Activa los botones para la fuerza
        self.activa_botones_fuerza(True)

        # Genera las cartas
        self.mesa.cartas.insert(0, self.crupier.repartir_carta())
        self.mesa.cartas.insert(1, self.crupier.repartir_carta())
        self.mesa.cartas.insert(2, self.crupier.repartir_carta())
        
        # Y las muestras
        self.label_mesa_carta_1.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(self.mesa.cartas[0])))
        self.label_mesa_carta_2.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(self.mesa.cartas[1])))
        self.label_mesa_carta_3.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(self.mesa.cartas[2])))

    def turn(self):
        """ 
            Cuarta carta de la mesa
        """ 

        # Genera la carta
        self.mesa.cartas.insert(3, self.crupier.repartir_carta())
        
        # Y la muestra
        self.label_mesa_carta_4.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(self.mesa.cartas[3])))

    def river(self):
        """ 
            Quinta carta de la mesa
        """ 

        # Genera la carta
        self.mesa.cartas.insert(4, self.crupier.repartir_carta())
        
        # Y la muestra
        self.label_mesa_carta_5.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(self.mesa.cartas[4])))
    

    ##
    ## FUERZA
    ##
    def on_fuerza(self, fuerza):
        """
            Establece la fuerza de la jugada para el paso actual
        """

        # Fuerza asignada al paso anterior
        self.jugador.valoracion[self.crupier.paso] = fuerza


    ##
    ## LISTA
    ##
    @QtCore.pyqtSlot(QtGui.QStandardItemModel)
    def on_jugada_clicked(self, model_index):
        """
            Muestra en la mesa la jugada seleccionada con su valoración de fuerza
            correspondiente
        """

        # Limpia la mesa y fuerza a Preflop el siguiente paso (simulando encontrarse en River)
        self.inicializa_mesa()
        self.crupier.paso = 2
        self.set_paso(self.crupier.siguiente_paso())

        # Obtiene índice de la fila seleccionada
        jugada = model_index.row()

        # Muestra las cartas del jugador y la mesa
        jugador = self.lista_jugadas[jugada][0]
        self.label_jugador_carta_1.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(jugador.cartas[0])))
        self.label_jugador_carta_2.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(jugador.cartas[1])))

        mesa = self.lista_jugadas[jugada][1]
        self.label_mesa_carta_1.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(mesa.cartas[0])))
        self.label_mesa_carta_2.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(mesa.cartas[1])))
        self.label_mesa_carta_3.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(mesa.cartas[2])))
        self.label_mesa_carta_4.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(mesa.cartas[3])))
        self.label_mesa_carta_5.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(mesa.cartas[4])))

        # Muestra la valoración de fuerza
        valoraciones = self.jugador.valoracion
        self.label_fuerza_flop.setStyleSheet(self.config.ESTILOS_FUERZA[valoraciones[1]])
        self.label_fuerza_flop.show()
        self.label_fuerza_turn.setStyleSheet(self.config.ESTILOS_FUERZA[valoraciones[2]])
        self.label_fuerza_turn.show()
        self.label_fuerza_river.setStyleSheet(self.config.ESTILOS_FUERZA[valoraciones[3]])
        self.label_fuerza_river.show()


    ##
    ## MÉTODOS AUXILIARES
    ##
    def set_paso(self, paso = 0):
        """
            Establece el texto del botón de los pasos según el valor del parámetro recibido 
        """
        self.pushbutton_paso.setText(self.crupier.pasos[paso])



    def inicializa_mesa(self):
        """
            Prepara la mesa para iniciar una nueva ronda:
            - Guarda la información de la ronda anterior
            - Limpia la mesa 
        """
    
        # Si se trata de la primera ronda tras ejecutar el programa la quinta carta de la mesa
        # no existirá porque no habrá habido todavía ningún River. En caso contrario realiza las
        # siguientes acciones con la última jugada:
        # 
        # - Actualiza la lista de jugadas de la pantalla
        # - Actualiza la lista de las jugadas (list)
        if len(self.mesa.cartas) == 5: 

            #
            # Lista de judadas de pantalla
            #

            # Número de jugadas de la lista. En este momento todavía no ha sido añadida la jugada actual.
            num_jugadas = self.model_jugadas.rowCount() + 1
            
            # Formato del item: 
            #
            #  Nº de jugada - Cartas del jugador - Cartas de la mesa
            #  1 - Ks 3h - Jc Ad 3s 7c Kh
            jugada = str(num_jugadas) + ' - '
            jugada += self.config.CARTAS[self.jugador.cartas[0]]['nombre'] + ' '
            jugada += self.config.CARTAS[self.jugador.cartas[1]]['nombre']
            jugada += ' - '
            jugada += self.config.CARTAS[self.mesa.cartas[0]]['nombre'] + ' '
            jugada += self.config.CARTAS[self.mesa.cartas[1]]['nombre'] + ' '
            jugada += self.config.CARTAS[self.mesa.cartas[2]]['nombre'] + ' '
            jugada += self.config.CARTAS[self.mesa.cartas[3]]['nombre'] + ' '
            jugada += self.config.CARTAS[self.mesa.cartas[4]]['nombre']

            # Crea el item y lo añade a la lista
            item = QtGui.QStandardItem(jugada)
            self.model_jugadas.appendRow(item)

            # Actualiza el título de la lista con el contador de jugadas
            self.dockwidget_jugadas.setWindowTitle('Jugadas ({0})'.format(num_jugadas))

            #
            # Lista de jugadas (list)
            #
            self.lista_jugadas.insert(num_jugadas, [self.jugador, self.mesa])

        #
        # Prepara los widgets para una nueva ronda
        #

        # Desactiva los botones de la fuerza porque hasta el flop no pueden pulsarse
        self.activa_botones_fuerza(False)

        # Oculta los indicadores de fuerza
        self.label_fuerza_flop.hide()
        self.label_fuerza_turn.hide()
        self.label_fuerza_river.hide()
        
        #
        # Limpia la mesa
        # 

        # Se recogen las cartas de la mesa, es decir, se inicializan los objetos
        # del jugador, mesa y crupier
        self.jugador = Jugador()
        self.mesa = Mesa()
        self.crupier = Crupier(self.config)
    
        # Cartas de la mesa
        self.label_mesa_carta_1.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(0)))
        self.label_mesa_carta_2.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(0)))
        self.label_mesa_carta_3.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(0)))
        self.label_mesa_carta_4.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(0)))
        self.label_mesa_carta_5.setPixmap(QtGui.QPixmap(self.config.get_imagen_carta(0)))

    def activa_botones_fuerza(self, activar = True):
        """
            Activa o desactiva los botones de la fuerza
        """

        self.pushbutton_fuerza5.setEnabled(activar)
        self.pushbutton_fuerza4.setEnabled(activar)
        self.pushbutton_fuerza3.setEnabled(activar)
        self.pushbutton_fuerza2.setEnabled(activar)
        self.pushbutton_fuerza1.setEnabled(activar)
    

if __name__ == '__main__':
    print u'Módulo no ejecutable.'
