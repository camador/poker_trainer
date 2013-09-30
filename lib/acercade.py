#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# César Amador - camador.git@gmail.com 
#
# Licenciado bajo Creative Commons Reconocimiento 3.0 Unported: http://creativecommons.org/licenses/by/3.0/deed.es_ES
#

# PyQt
from PyQt4 import uic, QtGui


# Otros
import sys
import os

class Acercade(QtGui.QWidget):
    """
        Ventana 'Acerca de...'
    """

    def __init__(self):

        # Inicicializa el ancestro
        QtGui.QWidget.__init__(self)

        # Lee el fichero que contiene la interfaz gráfica
        self.ui = uic.loadUi(os.path.join('lib', 'acercade.ui'))

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
        self.ui.exec_()
    
if __name__ == '__main__':
    print u'Módulo no ejecutable.'
