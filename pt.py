#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# POKER TRAINER
#
# Entrenador de póker
#
# César Amador - camador.git@gmail.com 
#
# Licenciado bajo Creative Commons Reconocimiento 3.0 Unported: http://creativecommons.org/licenses/by/3.0/deed.es_ES
#

# Interfaz gráfica
from lib.gui import GUI

##
## MAIN
##
def main():

    # Instancia la clase para la GUI
    gui = GUI()

    # Método de inicio
    gui.main()

    return 0


if __name__ == '__main__':

    try:
        
        # Empezando...
        main()
        
    except Exception, e:
        print '\n'
        print u'Error inesperado: '
        print '\n\t', e, '\n'
