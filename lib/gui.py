#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PyQt
from PyQt4 import uic, QtGui, QtCore

# Otros
import sys

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
        self.ui = uic.loadUi('lib/gui.ui')

        #
        # Lee los widgets y los asigna a variables
        #

        # Botón salir
        self.pushbutton_salir = self.ui.findChild(QtGui.QPushButton, "pbtSalir")

        #
        # Conecta las señales
        #

        # Botón salir
        self.pushbutton_salir.clicked.connect(self.on_salir)

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


if __name__ == '__main__':
    print u'Módulo no ejecutable.'
