#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# César Amador - camador.git@gmail.com 
#
# Licenciado bajo Creative Commons Reconocimiento 3.0 Unported: http://creativecommons.org/licenses/by/3.0/deed.es_ES
#

class Estadistica:
    """
        Mantiene las estadísticas de acierto por pasos
    """

    def __init__(self):
        """
            Inicializa el objeto
        """
    
        # Número de jugadas revisidas
        self.revisadas = 0

        # Contadores de aciertos (los tres pasos y acierto en los tres pasos)
        self.aciertos = {
                    'flop': 0,
                    'turn': 0,
                    'river': 0,
                    'total': 0
                }

    def actualiza_paso(self, paso, valor):
        """
            Actualiza el contador del paso recibido por parámetros 
        """
        
        self.aciertos[paso] += valor

    def porcentaje_paso(self, paso):
        """
            Devuelve el porcentaje de aciertos del paso recibido por parámetros
        """

        return self.aciertos[paso] / float(self.revisadas) * 100
    

if __name__ == '__main__':
    print u'Módulo no ejecutable.'
