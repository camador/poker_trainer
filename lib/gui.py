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
from lib.estadistica import Estadistica

# Acerca de
from lib.acercade import Acercade

# Otros
import sys
import os
from time import gmtime, strftime

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

        # Estadísticas
        self.estadistica = Estadistica()

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

        # Estilos
        # Si existe el fichero de estilos lo carga
        fichero_qss = os.path.join('lib', self.config.ESTILOS)
        if os.path.isfile(fichero_qss):
            with open(fichero_qss, 'r') as estilos:
                self.app.setStyleSheet(estilos.read())

        # Lee los widgets
        self.lee_widgets()

        # Conecta las señales
        self.conecta_senales()

    def lee_widgets(self):
        """
            Lee los widgets y los asigna a variables
        """

        # Botón Salir
        #self.pushbutton_salir = self.ui.findChild(QtGui.QPushButton, 'pbtSalir')

        # Botón Paso
        self.pushbutton_paso = self.ui.findChild(QtGui.QPushButton, 'pbtPaso')

        # Botones para la fuerza de la jugada
        self.botones_fuerza = [
                    self.ui.findChild(QtGui.QPushButton, 'pbtFuerza1'),
                    self.ui.findChild(QtGui.QPushButton, 'pbtFuerza2'),
                    self.ui.findChild(QtGui.QPushButton, 'pbtFuerza3'),
                    self.ui.findChild(QtGui.QPushButton, 'pbtFuerza4'),
                    self.ui.findChild(QtGui.QPushButton, 'pbtFuerza5')
                ]

        # Cartas de la mesa
        self.label_mesa_cartas = [
                    self.ui.findChild(QtGui.QLabel, 'lblMesaCarta1'),
                    self.ui.findChild(QtGui.QLabel, 'lblMesaCarta2'),
                    self.ui.findChild(QtGui.QLabel, 'lblMesaCarta3'),
                    self.ui.findChild(QtGui.QLabel, 'lblMesaCarta4'),
                    self.ui.findChild(QtGui.QLabel, 'lblMesaCarta5')
                ]
        
        # Cartas del jugador
        self.label_jugador_cartas = [
                    self.ui.findChild(QtGui.QLabel, 'lblJugadorCarta1'),
                    self.ui.findChild(QtGui.QLabel, 'lblJugadorCarta2')
                ]

        # Indicadores de la fuerza de las jugadas
        self.label_fuerza = {
                    'flop': self.ui.findChild(QtGui.QLabel, 'lblFuerzaFlop'),
                    'turn': self.ui.findChild(QtGui.QLabel, 'lblFuerzaTurn'),
                    'river': self.ui.findChild(QtGui.QLabel, 'lblFuerzaRiver')
                }

        # Porcentaje de aciertos
        self.label_porcentaje = {
                    'flop': self.ui.findChild(QtGui.QLabel, 'lblPorcentajeFlop'),
                    'turn': self.ui.findChild(QtGui.QLabel, 'lblPorcentajeTurn'),
                    'river': self.ui.findChild(QtGui.QLabel, 'lblPorcentajeRiver'),
                    'total': self.ui.findChild(QtGui.QLabel, 'lblPorcentajeTotal')
                }

        # Número de jugadas revisadas
        self.label_numero_revisiones = self.ui.findChild(QtGui.QLabel, 'lblNumeroRevisiones')

        # Groupbox para la lista de jugadas
        self.groupbox_jugadas = self.ui.findChild(QtGui.QGroupBox, 'grbJugadas')

        # Lista de jugadas
        self.listview_jugadas = self.ui.findChild(QtGui.QListView, 'lsvJugadas')

        # Model de la lista de jugadas
        self.model_jugadas = QtGui.QStandardItemModel(self.listview_jugadas)
        self.listview_jugadas.setModel(self.model_jugadas)

        # Selection Model de la lista de jugadas
        self.selec_model_jugadas = self.listview_jugadas.selectionModel()

        # Botones de la lista de jugadas
        self.pushbutton_guardar = self.ui.findChild(QtGui.QPushButton, 'pbtGuardar')
        self.pushbutton_limpiar = self.ui.findChild(QtGui.QPushButton, 'pbtLimpiar')


        # Controles de revisión
        self.groupbox_revision = self.ui.findChild(QtGui.QGroupBox, 'grbRevision')
        self.radiobutton_revision = {
                    'flop': [
                            self.ui.findChild(QtGui.QRadioButton, 'rdbFlopOk'),
                            self.ui.findChild(QtGui.QRadioButton, 'rdbFlopNoOk')
                        ],
                    'turn': [
                            self.ui.findChild(QtGui.QRadioButton, 'rdbTurnOk'),
                            self.ui.findChild(QtGui.QRadioButton, 'rdbTurnNoOk')
                        ],
                    'river': [
                            self.ui.findChild(QtGui.QRadioButton, 'rdbRiverOk'),
                            self.ui.findChild(QtGui.QRadioButton, 'rdbRiverNoOk')
                        ]
                }
        self.pushbutton_revision = self.ui.findChild(QtGui.QPushButton, 'pbtRevision')

        # Menú
        self.action_acerca_de = self.ui.findChild(QtGui.QAction, 'actionAcerca_de')
        self.menu_jugadas = self.ui.findChild(QtGui.QMenu, 'menuJugadas')

        # Barra de estado
        self.statusbar_barra_de_estado = self.ui.findChild(QtGui.QStatusBar, 'statusBar')

    def conecta_senales(self):
        """
            Conecta las señales de los widges
        """

        # Botón Salir
        #self.pushbutton_salir.clicked.connect(self.on_salir)

        # Botón Paso
        self.pushbutton_paso.clicked.connect(self.on_paso)

        # Botones para la fuerza de la jugada
        # lambda porque la función tiene parámetros
        self.botones_fuerza[4].clicked.connect(lambda: self.on_fuerza(5))
        self.botones_fuerza[3].clicked.connect(lambda: self.on_fuerza(4))
        self.botones_fuerza[2].clicked.connect(lambda: self.on_fuerza(3))
        self.botones_fuerza[1].clicked.connect(lambda: self.on_fuerza(2))
        self.botones_fuerza[0].clicked.connect(lambda: self.on_fuerza(1))

        # Lista de jugadas
        self.selec_model_jugadas.currentRowChanged.connect(self.on_jugada_row_changed)
        self.pushbutton_guardar.clicked.connect(self.on_guardar)
        self.pushbutton_limpiar.clicked.connect(self.on_limpiar)

        # Revisión
        self.pushbutton_revision.clicked.connect(self.on_revision)

        # Menú
        self.action_acerca_de.triggered.connect(self.on_acerca_de)

    ##
    ## MAIN
    ##
    def main(self):
        """
            Método de inicio
        """
        
        #
        # Estado inicial del interfaz
        #

        # Texto para el botón de los pasos
        self.set_paso(self.crupier.paso)

        # Primer paso: preflop
        self.preflop()

        # Barra de estado
        self.statusbar_barra_de_estado.showMessage('Bienvenido a Poker Trainer', self.config.DURACION_MENSAJES)


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
    ## ACERCA DE
    ##
    @QtCore.pyqtSlot()
    def on_acerca_de(self):
        """
            Termina la ejecución del programa
        """

        # Muestra la ventana 'Acerca de'
        acercade = Acercade()
        acercade.main()

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
        for i in range(2):
            self.jugador.cartas.insert(i, self.crupier.repartir_carta())
            imagen_carta = QtGui.QPixmap(self.config.get_imagen_carta(self.jugador.cartas[i]))
            self.label_jugador_cartas[i].setPixmap(imagen_carta)

    def flop(self):
        """ 
            Tres cartas en la mesa
        """ 
        
        # Activa los botones para la fuerza
        self.activa_botones_fuerza(True)

        # Reparte las cartas
        for i in range(3):
            self.mesa.cartas.insert(i, self.crupier.repartir_carta())
            imagen_carta = QtGui.QPixmap(self.config.get_imagen_carta(self.mesa.cartas[i]))
            self.label_mesa_cartas[i].setPixmap(imagen_carta)

    def turn(self):
        """ 
            Cuarta carta de la mesa
        """ 

        # Genera la carta
        self.mesa.cartas.insert(3, self.crupier.repartir_carta())
        
        # Y la muestra
        imagen_carta = QtGui.QPixmap(self.config.get_imagen_carta(self.mesa.cartas[3]))
        self.label_mesa_cartas[3].setPixmap(imagen_carta)

    def river(self):
        """ 
            Quinta carta de la mesa
        """ 

        # Genera la carta
        self.mesa.cartas.insert(4, self.crupier.repartir_carta())
        
        # Y la muestra
        imagen_carta = QtGui.QPixmap(self.config.get_imagen_carta(self.mesa.cartas[4]))
        self.label_mesa_cartas[4].setPixmap(imagen_carta)
    

    ##
    ## FUERZA
    ##
    def on_fuerza(self, fuerza):
        """
            Establece la fuerza de la jugada para el paso actual
        """

        # Fuerza asignada al paso anterior
        self.jugador.valoracion[self.crupier.paso] = fuerza

        # Fija el color del indicador correspondiente en función de la fuerza seleccionada y
        # lo muestra
        if self.crupier.paso == 1:
            nombre = 'flop'
        
        elif self.crupier.paso == 2:
            nombre = 'turn'
        
        else:
            nombre = 'river'
            
        self.label_fuerza[nombre].setStyleSheet(self.config.ESTILOS_FUERZA[fuerza])
        self.label_fuerza[nombre].show()

    ##
    ## LISTA
    ##
    @QtCore.pyqtSlot(QtGui.QStandardItemModel)
    def on_jugada_row_changed(self, model_index):
        """
            Muestra en la mesa la jugada seleccionada con su valoración de fuerza
            correspondiente
        """

        # Sólo si hay jugadas que procesar (rowChanged se lanza tras vaciar la lista)
        if self.lista_jugadas:

            # Limpia la mesa y fuerza a Preflop el siguiente paso (simulando encontrarse en River)
            self.inicializa_mesa()
            self.crupier.paso = 2
            self.set_paso(self.crupier.siguiente_paso())

            # Obtiene índice de la fila seleccionada
            jugada = model_index.row()

            # Muestra las cartas del jugador y la mesa
            jugador = self.lista_jugadas[jugada][0]
            for i in range(2):
                imagen_carta = QtGui.QPixmap(self.config.get_imagen_carta(jugador.cartas[i]))
                self.label_jugador_cartas[i].setPixmap(imagen_carta)

            mesa = self.lista_jugadas[jugada][1]
            for i in range(5):
                imagen_carta = QtGui.QPixmap(self.config.get_imagen_carta(mesa.cartas[i]))
                self.label_mesa_cartas[i].setPixmap(imagen_carta)

            # Muestra la valoración de fuerza
            valoracion = jugador.valoracion
            self.label_fuerza['flop'].setStyleSheet(self.config.ESTILOS_FUERZA[valoracion[1]])
            self.label_fuerza['turn'].setStyleSheet(self.config.ESTILOS_FUERZA[valoracion[2]])
            self.label_fuerza['river'].setStyleSheet(self.config.ESTILOS_FUERZA[valoracion[3]])

            for label in self.label_fuerza.itervalues():
                label.show()

            # Activa los controles de revisión y fija los valores, si los hay
            self.activa_revision(True)

            pasos = ['flop', 'turn', 'river']
            for i in range(3):

                paso = pasos[i]

                # Recupera el valor de la revisón
                revision = jugador.revision[i]

                if revision == 1:

                    # Correcto. Marca el radiobutton Ok
                    self.radiobutton_revision[paso][0].setChecked(True)

                elif revision == 0:

                    # Correcto. Marca el radiobutton NoOk
                    self.radiobutton_revision[paso][1].setChecked(True)

    @QtCore.pyqtSlot()
    def on_guardar(self):
        """
            Guarda la lista de las jugadas y las estadísticas en un fichero con el siguiente formato:

             POKER TRAINER
            ---------------

            Sesion: 2013-10-01 19:15:53

            Lista de jugadas
            ----------------
                                                        +-----------------------------+
                                                        |       Fuerza (Acierto)      |
            +--------------------------------+----------+---------+-------------------+
            |             Jugada             | Revisada |  Flop   |  Turn   |  River  |
            +--------------------------------+----------+---------+---------+---------+
            | 1 - 10h 8h - 9d 10s 6d Ah 3s   |    X     | MF (S)  | MM (S)  | MD (S)  | 
            +--------------------------------+----------+---------+---------+---------+
            | 2 - Qs 2d - 4s Qd 3s 9h 7h     |    X     | MMF (S) | MMF (S) | MMF (N) | 
            +--------------------------------+----------+---------+---------+---------+
            | 3 - 4h 6c - Qd 3c 9h 3s 10c    |          |         |         |         | 
            +--------------------------------+----------+---------+---------+---------+
            | 4 - Ad 7h - 2d 10s Js 9s 3d    |    X     | N (S)   | N (N)   | N (-)   | 
            +--------------------------------+----------+---------+---------+---------+
            | 5 - 6h 5h - Kh 10s 9d 4s Ad    |    X     | -- (N)  | MMF (N) | MD (N)  | 
            +--------------------------------+----------+---------+---------+---------+

            Estadísticas
            ------------
            Porcentaje de aciertos (sobre 4 revisiones):
            +--------+--------+--------+--------+
            |  Flop  |  Turn  |  River |  Total |
            +--------+--------+--------+--------+
            |   5.00 | 100.00 |   5.00 | 100.00 |
            +--------+--------+--------+--------+

        """
        
        # Avisa al usuario de que se está guardando la sesión
        self.statusbar_barra_de_estado.showMessage('Guardando jugadas...', self.config.DURACION_MENSAJES)

        try:

            # Comprueba si existe el directorio para las sesiones
            if not os.path.isdir(self.config.DIR_SESIONES):

                # El directorio no existe, intenta crearlo
                os.makedirs(self.config.DIR_SESIONES)

            # Nombre del fichero
            fecha = gmtime()
            nombre_fichero = 'poker_trainer-{0}.txt'.format(strftime('%Y_%m_%d-%H_%M_%S', fecha))
            nombre_fichero = os.path.join(self.config.DIR_SESIONES, nombre_fichero)

            # Crea el fichero y guarda la información
            with open(nombre_fichero, 'w') as fichero:

                # Cabecera
                fichero.write(' POKER TRAINER\n')
                fichero.write('---------------\n')

                fichero.write('\n')
                fichero.write('Sesión: {0}\n'.format(strftime('%Y-%m-%d %H:%M:%S', fecha)))
                fichero.write('\n')

                # Lista de jugadas
                fichero.write('Lista de jugadas\n')
                fichero.write('----------------\n')

                fichero.write(u'                                            +-----------------------------+\n')
                fichero.write(u'                                            |       Fuerza (Acierto)      |\n')
                fichero.write(u'+--------------------------------+----------+---------+-------------------+\n')
                fichero.write(u'|             Jugada             | Revisada |  Flop   |  Turn   |  River  |\n')
                fichero.write(u'+--------------------------------+----------+---------+---------+---------+\n')

                fuerzas = ['--', 'N', 'MD', 'MM', 'MF', 'MMF'] 

                # lista_jugadas contiene [jugador, mesa, texto_jugadas]
                for jugada in self.lista_jugadas:

                    # Si la jugada está revisada añade la información a la línea
                    if jugada[0].revisada:

                        # Marca la fila como revisada
                        revisada = 'X'

                        # Recupera las valoraciones de fuerza que hizo el usuario
                        valoraciones = jugada[0].valoracion
                        revisiones = jugada[0].revision

                        # valoraciones es una lista con 4 elementos, las valoraciones de Preflop a River,
                        # como en Preflop no se hacen valoraciones de fuerza, se omite el primer elemento
                        for paso in range(1, 4):

                            # valoraciones[paso] contiene un valor de 0 a 5
                            # 0 - Sin valorar
                            # 1 - Nada (N)
                            # 2 - Mano Débil (MD)
                            # 3 - Mano Media (MM)
                            # 4 - Mano Fuerte (MF)
                            # 5 - Mano Muy Fuerte (MMF)
                            fuerza = fuerzas[valoraciones[paso]]

                            # Recupera la revisión del paso (paso - 1 porque sólo hay 
                            # revisiones para Flop, Turn y River)                                
                            # Los valores de la revisión pueden ser:
                            # None - No revisado
                            # 0 - Incorrecto
                            # 1 - Correcto
                            if revisiones[paso - 1] == 1:
                                acierto = 'S'

                            elif revisiones[paso - 1] == 0:
                                acierto = 'N'

                            else:
                                acierto = '-'

                            # Forma la cadena con los datos calculados
                            celda = '{0} ({1})'.format(fuerza, acierto)

                            # Asigna la cadena calculada al paso correspondiente
                            if paso == 1:
                                flop = celda 

                            elif paso == 2:
                                turn = celda 

                            else:
                                river = celda

                    else:
                        # Si no lo está, deja todos los campos en blanco
                        revisada = ''
                        flop = ''
                        turn = ''
                        river = ''
                        
                    fichero.write(u'| {0: <30} | {1: ^8} | {2: <7} | {3: <7} | {4: <7} | \n'.format(jugada[2], revisada, flop, turn, river))
                    fichero.write(u'+--------------------------------+----------+---------+---------+---------+\n')

                # Estadísticas
                fichero.write('\n')
                fichero.write('Estadísticas\n')
                fichero.write('------------\n')

                porcentajes = {'flop': 0, 'turn': 0, 'river': 0, 'total': 0}
                for paso in ['flop', 'turn', 'river', 'total']:
                    porcentajes[paso] = float(self.label_porcentaje[paso].text())

                fichero.write('Porcentaje de aciertos (sobre {0} revisiones):\n'.format(self.estadistica.revisadas))
                fichero.write(u'+--------+--------+--------+--------+\n')
                fichero.write(u'|  Flop  |  Turn  |  River |  Total |\n')
                fichero.write(u'+--------+--------+--------+--------+\n')
                fichero.write( '| {0[flop]: >6.2f} | {0[turn]: >6.2f} | {0[river]: >6.2f} | {0[total]: >6.2f} |\n'.format(porcentajes))
                fichero.write(u'+--------+--------+--------+--------+')

                # Autopropaganda
                fichero.write('\n')
                fichero.write('\n')
                fichero.write('---\n')
                fichero.write('Generado por Poker Trainer\n')
                fichero.write('https://github.com/camador/poker_trainer')

            # Mensaje para el usuario
            mensaje = u'Sesión guardada correctamente en {0}'.format(nombre_fichero)
            
        except:
            # Mensaje para el usuario
            mensaje = u'Error al guardar la sesión'

        # Informa al usuario
        self.statusbar_barra_de_estado.showMessage(mensaje, self.config.DURACION_MENSAJES)


    @QtCore.pyqtSlot()
    def on_limpiar(self):
        """
            Limpia la lista de jugadas y las estadísticas
        """

        # Limpia la lista (list)
        self.lista_jugadas = list()

        # Limpia la lista (widget)
        self.model_jugadas.removeRows(0, self.model_jugadas.rowCount())
        
        # Actualiza el título de la lista con el contador de jugadas
        self.groupbox_jugadas.setTitle('Jugadas')

        # Resetea las estadísticas
        self.estadistica = Estadistica()
        self.label_numero_revisiones.setText('(sobre 0 revisiones)')
        for paso in ['flop', 'turn', 'river', 'total']:
            self.label_porcentaje[paso].setText('0')

        # Desactiva los controles de revisión
        self.activa_revision(False)

        # Informa al usuario
        self.statusbar_barra_de_estado.showMessage(u'Jugadas y estadísticas eliminadas', self.config.DURACION_MENSAJES)

        # Desactiva los botones y menú de la lista de jugadas
        self.activa_botones_jugada(False)
        

    ##
    ## REVISION
    ##
    @QtCore.pyqtSlot()
    def on_revision(self):
        """
            Guarda los valores de revisión de la jugada y pasa a la siguiente, si existe
        """

        # Recupera la jugada
        jugada = self.selec_model_jugadas.currentIndex().row()
        jugador = self.lista_jugadas[jugada][0]

        # Marcador de jugada ya revisada
        revisada = jugador.revisada

        # Indicador de acierto en los tres pasos
        revision_pleno = jugador.revision_pleno()

        # Número de pasos no revisados (radiobuttons no seleccionados)
        pasos_no_revisados = 0
        
        # Por cada paso comprueba la revisión:
        # {
        #   paso1 = [radiook, radionook],
        #   ...
        #   pason = [radiook, radionook]
        # }
        pasos = ['flop', 'turn', 'river']
        for i in range(3):

            paso = pasos[i]

            # Tres estados posibles:
            # - Correcto -> Primer radiobutton de la lista marcado (Ej.: rdbFlopOk)
            # - Incorrecto -> Segundo radiobutton de la lista marcado (Ej.: rdbFlopNoOk)
            # - Sin revisar -> Ningún radiobutton marcado
            #
            # Para cada paso el valor de la revisión puede ser:
            # 0 -> Incorrecto
            # 1 -> Correcto
            if self.radiobutton_revision[paso][0].isChecked():

                # Actualización de las estadísticas
                # Aumenta el contador cuando cambia la revisión
                if jugador.revision[i] != 1:
                    self.estadistica.actualiza_paso(paso, 1)

                # Correcto
                jugador.revision[i] = 1

            elif self.radiobutton_revision[paso][1].isChecked():

                # Actualización de las estadísticas
                # Decrementa el contador cuando la revisión anterior era correcta
                if jugador.revision[i] == 1:
                    self.estadistica.actualiza_paso(paso, -1)

                # Incorrecto
                jugador.revision[i] = 0

            else:

                # Sin revisar
                pasos_no_revisados += 1

        # Contador de acierto en los tres pasos
        # Si en la nueva revisión todo son aciertos y en la anterior no, incrementa
        # el contador
        nuevo_revision_pleno = jugador.revision_pleno()
        if nuevo_revision_pleno and revision_pleno != nuevo_revision_pleno:
            self.estadistica.actualiza_paso('total', 1)

        # Contador de jugadas revisadas
        # Si la jugada no había sido anteriormente revisada, y en la actual revisión se ha marcado
        # algún radiobutton, incrementa el contador de jugadas revisadas y la marca como revisada
        if not revisada and pasos_no_revisados < 3:
            self.estadistica.revisadas += 1
            jugador.revisada = True

        # Actualiza las estadísticas si hay alguna jugada revisada
        if self.estadistica.revisadas > 0:

            # Número de revisiones
            self.label_numero_revisiones.setText('(sobre {0} revisiones)'.format(self.estadistica.revisadas))
            for paso in ['flop', 'turn', 'river', 'total']:

                # Cálculo del porcentaje
                porcentaje = self.estadistica.porcentaje_paso(paso)
                
                # Formato según el valor
                if porcentaje == 100 or porcentaje == 0:
                    texto_label = '{0:.0f}'.format(porcentaje)
                else:
                    texto_label = '{0:.2f}'.format(porcentaje)

                # Muestra el porcentaje
                self.label_porcentaje[paso].setText(texto_label)

        # Siguiente jugada de la lista
        index = self.listview_jugadas.moveCursor(QtGui.QAbstractItemView.MoveNext, QtCore.Qt.NoModifier)
        self.listview_jugadas.setCurrentIndex(index)
        self.selec_model_jugadas.select(index, QtGui.QItemSelectionModel.SelectCurrent)

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
            self.groupbox_jugadas.setTitle('Jugadas ({0})'.format(num_jugadas))

            #
            # Lista de jugadas (list)
            #
            self.lista_jugadas.append([self.jugador, self.mesa, jugada])

            # Activa los botones y el menú de la lista de jugadas
            self.activa_botones_jugada(True)

        #
        # Prepara los widgets para una nueva ronda
        #

        # Desactiva los controles de revisión
        self.activa_revision(False)

        # Desactiva los botones de la fuerza porque hasta el flop no pueden pulsarse
        self.activa_botones_fuerza(False)

        # Oculta los indicadores de fuerza
        for label in self.label_fuerza.itervalues():
            label.hide()
        
        #
        # Limpia la mesa
        # 

        # Se recogen las cartas de la mesa, es decir, se inicializan los objetos
        # del jugador, mesa y crupier
        self.jugador = Jugador()
        self.mesa = Mesa()
        self.crupier = Crupier(self.config)
    
        # Cartas de la mesa
        reverso = QtGui.QPixmap(self.config.get_imagen_carta(0))
        for carta in self.label_mesa_cartas:
            carta.setPixmap(reverso)

    def activa_botones_fuerza(self, activar = True):
        """
            Activa o desactiva los botones de la fuerza
        """

        for boton in self.botones_fuerza:
            boton.setEnabled(activar)
    
    def activa_revision(self, activar = True):
        """
            Activa o desactiva los controles de revisión
        """

        # Limpia las selecciones de los radiobuttons
        for paso in self.radiobutton_revision:

            self.radiobutton_revision[paso][0].setAutoExclusive(False)
            self.radiobutton_revision[paso][0].setChecked(False)
            self.radiobutton_revision[paso][1].setChecked(False)
            self.radiobutton_revision[paso][0].setAutoExclusive(True)

        # Los activa o desactiva
        self.groupbox_revision.setEnabled(activar)

    def activa_botones_jugada(self, activar = True):
        """
            Activa o desactiva los botones y menú de la lista de jugadas 
        """
        
        # Botones
        self.pushbutton_guardar.setEnabled(activar)
        self.pushbutton_limpiar.setEnabled(activar)

        # Menú
        self.menu_jugadas.setEnabled(activar)

if __name__ == '__main__':
    print u'Módulo no ejecutable.'
