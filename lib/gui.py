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


    ##
    ## MAIN
    ##
    def main(self):
        """
            Método de inicio
        """

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
            Avanza hasta el siguiente paso 
        """

        # Fija el texto del botón para el siguiente paso
        self.pushbutton_paso.setText(self.config.PASOS[self.get_siguiente_paso()])
    
    ##
    ## MÉTODOS AUXILIARES
    ##
    def get_siguiente_paso(self):
        """
            Calcula, fija y devuelve el siguiente paso
        """
    
        self.paso += 1

        if self.paso == self.num_pasos:
            self.paso = 0

        return self.paso

if __name__ == '__main__':
    print u'Módulo no ejecutable.'
