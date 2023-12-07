import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor


class GraphWidget(QWidget):
    def __init__(self, parent=None):
        super(GraphWidget, self).__init__(parent)

        self.window_start = 0
        self.window_finish = 0
        self.update_window_start = True
        self.update_window_finish = True

        # Dados sintéticos para apresentação
        self.time_data = np.arange(1, 201)
        self.velocity_random = np.append(np.random.uniform(
            0.5, 30, 100), np.random.uniform(-10, -0.2, 100))
        self.acceleration_random = np.append(np.random.uniform(
            0.5, 5, 100), np.random.uniform(-5, -0.2, 100))
        self.height_random = np.cumsum(self.velocity_random)

        self.plot_widget_acceleration   = pg.PlotWidget(self)
        self.plot_widget_velocity       = pg.PlotWidget(self)
        self.plot_widget_height         = pg.PlotWidget(self)

        self.init_plots()
        self.init_statistics()

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.plot_widget_acceleration, 0, 0)
        self.layout.addWidget(self.plot_widget_velocity, 0, 1)
        self.layout.addWidget(self.plot_widget_height, 1,
                              0, 1, 1)  # Ocupa duas colunas
        self.layout.addLayout(self.widget_statistics, 1, 1, 1, 1)

        self.animation_timer = pg.QtCore.QTimer(self)
        self.animation_timer.timeout.connect(self.update_plot)
        self.frame = 0

        self.init_ui()

        # Definindo a variável para rastrear o modo atual (claro ou escuro)
        self.is_dark_mode = False

    def init_plots(self):
        ''' 
        Inicializa os gráficos de aceleração, velocidade e altura.
        '''
        self.plot_acceleration = self.plot_widget_acceleration.plot(
            pen='#2B2A32', symbolBrush='#2B2A32', symbolPen='w')
        self.plot_widget_acceleration.setTitle(
            'Aceleração', color='k')  # Título em preto
        self.plot_widget_acceleration.setLabel('left', 'α (m/s²)')
        self.plot_widget_acceleration.setLabel(
            'bottom', 'tempo (s)', color='k')
        self.plot_widget_acceleration.setBackground('w')  # Fundo branco

        self.plot_velocity = self.plot_widget_velocity.plot(
            pen='#3d2163', symbolBrush='#3d2163', symbolPen='w')
        self.plot_widget_velocity.setTitle(
            'Velocidade', color='k')  # Título em preto
        self.plot_widget_velocity.setLabel('left', 'v (m/s)')
        self.plot_widget_velocity.setLabel('bottom', 'tempo (s)', color='k')
        self.plot_widget_velocity.setBackground('w')  # Fundo branco

        self.plot_height = self.plot_widget_height.plot(
            pen='#355eab', symbolBrush='#355eab', symbolPen='w')
        self.plot_widget_height.setTitle(
            'Altura', color='k')  # Título em preto
        self.plot_widget_height.setLabel('left', 'h (m)')
        self.plot_widget_height.setLabel('bottom', 'tempo (s)', color='k')
        self.plot_widget_height.setBackground('w')  # Fundo branco

        self.plot_widget_acceleration.getPlotItem().getAxis(
            'bottom').setTextPen(color='#000000')
        self.plot_widget_acceleration.getPlotItem().getAxis(
            'left').setTextPen(color='#000000')

        self.plot_widget_velocity.getPlotItem().getAxis(
            'bottom').setTextPen(color='#000000')
        self.plot_widget_velocity.getPlotItem().getAxis(
            'left').setTextPen(color='#000000')

        self.plot_widget_height.getPlotItem().getAxis(
            'bottom').setTextPen(color='#000000')
        self.plot_widget_height.getPlotItem().getAxis(
            'left').setTextPen(color='#000000')

    def init_statistics(self):
        '''
        Inicializa as variáveis para análise estatística. Velocidade atual, altura atual, aceleração atual, apogeu e tempo de vôo.
        '''
        # Velocity
        self.velocidade = QLabel(self)
        self.curr_velocity = 0

        # Height
        self.altura = QLabel(self)
        self.curr_height = 0

        # Acceleration
        self.aceleracao = QLabel(self)
        self.curr_acceleration = 0

        # Apogee
        self.apogeu = QLabel(self)
        self.curr_apogee = 0

        # Flight time
        self.tempo_de_voo = QLabel(self)
        self.curr_flight_time = 0

        # Time window parameters (initial, final)
        self.initial_time_window_label = QLabel(self)
        self.initial_time_window_label.setText("Tempo inicial:")
        self.initial_time_window = QLineEdit()
        self.initial_time_window.setPlaceholderText("0")
        self.initial_time_window.textChanged.connect(self.change_window_start)
        self.final_time_window_label = QLabel(self)
        self.final_time_window_label.setText("Tempo final:")
        self.final_time_window = QLineEdit()
        self.final_time_window.setPlaceholderText("0")
        self.final_time_window.textChanged.connect(self.change_window_finish)

        self.update_statistics(0)
        self.widget_statistics = QGridLayout()

        self.widget_statistics.addWidget(self.velocidade, 0, 0)
        self.velocidade.setFixedWidth(250)
        self.widget_statistics.addWidget(self.altura, 1, 0)
        self.altura.setFixedWidth(250)
        self.widget_statistics.addWidget(self.aceleracao, 2, 0)
        self.widget_statistics.addWidget(self.apogeu, 3, 0)
        self.widget_statistics.addWidget(self.tempo_de_voo, 4, 0)

        self.widget_statistics.addWidget(self.initial_time_window_label, 0, 1)
        self.widget_statistics.addWidget(self.final_time_window_label, 1, 1)
        self.widget_statistics.addWidget(self.initial_time_window, 0, 2)
        self.widget_statistics.addWidget(self.final_time_window, 1, 2)

    def change_window_start(self, value):
        '''
        Atualiza of valor do tempo inicial da janela temporal para o valor indicado e fixa
        a janela para começar desse valor.
        '''
        if value == '':
            self.window_start = self.frame - 1
            self.update_window_start = True
        else:
            self.window_start = int(value) - 1
            self.update_window_start = False

    def change_window_finish(self, value):
        '''
        Atualiza of valor do tempo final da janela temporal para o valor indicado e fixa
        a janela para terminar nesse valor.
        '''
        if value == '':
            self.window_finish = self.frame
            self.update_window_finish = True
        else:
            self.window_finish = int(value) - 1
            self.update_window_finish = False

    def init_ui(self):
        '''
        Inicializa o layout dos gráficos na interface.
        '''
        button_layout = QHBoxLayout()  # Trocado para QHBoxLayout

        # Alterações nos estilos dos botões para torná-los menores e mais estilizados
        self.show_acceleration_button = QPushButton('Ocultar Aceleração', self)
        self.show_velocity_button = QPushButton('Ocultar Velocidade', self)
        self.show_height_button = QPushButton('Ocultar Altura', self)
        self.dark_mode_button = QPushButton('Dark Mode', self)

        for button in [self.show_acceleration_button, self.show_velocity_button, self.show_height_button, self.dark_mode_button]:
            button.setStyleSheet("QPushButton { background-color: #2B2A32; color: white; padding: 5px; }"
                                 "QPushButton:hover { background-color: #383742; }")

        button_layout.addWidget(self.show_acceleration_button)
        button_layout.addWidget(self.show_velocity_button)
        button_layout.addWidget(self.show_height_button)
        button_layout.addWidget(self.dark_mode_button)

        # Adiciona os botões na linha 2
        self.layout.addLayout(button_layout, 2, 0, 1, 2)

        for button in [self.show_acceleration_button, self.show_velocity_button, self.show_height_button, self.dark_mode_button]:
            button.clicked.connect(self.toggle_button)

        self.animation_timer.start(1000)  # 1000 milliseconds interval
        self.setAutoFillBackground(True)

    def update_statistics(self, frame):
        '''
        Atualiza os valores das variáveis de acordo com o valor do último frame.
        '''
        if frame > 0:
            self.curr_velocity = self.velocity_random[frame]
            self.curr_height = self.height_random[frame]
            self.curr_acceleration = self.acceleration_random[frame]
            if self.height_random[frame] > self.curr_apogee:
                self.curr_apogee = self.height_random[frame]
            self.curr_flight_time += 1
        self.velocidade.setText(
            f"Velocidade: {round(self.curr_velocity, 2)} m/s")
        self.altura.setText(f"Altura: {round(self.curr_height, 2)} m")
        self.aceleracao.setText(
            f"Aceleração: {round(self.curr_acceleration, 2)} m/s²")
        self.apogeu.setText(f"Apogeu: {round(self.curr_apogee, 2)} m")
        self.tempo_de_voo.setText(f"Tempo de voo: {self.curr_flight_time} s")

    def update_plot(self):
        if ((self.frame - self.window_start) > 20) and self.update_window_start:
            self.window_start += 1
            self.initial_time_window.setPlaceholderText(str(self.window_start))
        if self.frame < len(self.time_data):
            self.plot_acceleration.setData(
                self.time_data[self.window_start:self.window_finish + 1], self.acceleration_random[self.window_start:self.window_finish + 1], symbol='o')
            self.plot_velocity.setData(self.time_data[self.window_start:self.window_finish + 1],
                                       self.velocity_random[self.window_start:self.window_finish + 1], symbol='o')
            self.plot_height.setData(self.time_data[self.window_start:self.window_finish + 1],
                                     self.height_random[self.window_start:self.window_finish + 1], symbol='o')
            self.frame += 1
            if self.update_window_finish:
                self.window_finish = self.frame
                self.final_time_window.setPlaceholderText(str(self.window_finish))
            self.update_statistics(self.frame)
        else:
            self.animation_timer.stop()

    def toggle_button(self):
        sender = self.sender()
        if sender.text() == 'Dark Mode':
            self.toggle_dark_mode()
        else:
            self.toggle_plot(sender)

    def toggle_plot(self, button):
        if 'Ocultar' in button.text():
            button.setText(button.text().replace('Ocultar', 'Mostrar'))
            if 'Aceleração' in button.text():
                self.toggle_acceleration()
            elif 'Velocidade' in button.text():
                self.toggle_velocity()
            elif 'Altura' in button.text():
                self.toggle_height()
        else:
            button.setText(button.text().replace('Mostrar', 'Ocultar'))
            if 'Aceleração' in button.text():
                self.toggle_acceleration()
            elif 'Velocidade' in button.text():
                self.toggle_velocity()
            elif 'Altura' in button.text():
                self.toggle_height()

    def toggle_acceleration(self):
        if self.plot_widget_acceleration.isVisible():
            self.plot_widget_acceleration.setVisible(False)
        else:
            self.plot_widget_acceleration.setVisible(True)

    def toggle_velocity(self):
        if self.plot_widget_velocity.isVisible():
            self.plot_widget_velocity.setVisible(False)
        else:
            self.plot_widget_velocity.setVisible(True)

    def toggle_height(self):
        if self.plot_widget_height.isVisible():
            self.plot_widget_height.setVisible(False)
        else:
            self.plot_widget_height.setVisible(True)

    def toggle_dark_mode(self):
        '''
        Alterna entre os modos claro e escuro
        '''
        self.is_dark_mode = not self.is_dark_mode

        if self.is_dark_mode:
            background_color = '#111'
            text_color = '#fff'
            pen_color_a ='#85ffb6'
            pen_color_v ='#9652d1'
            pen_color_h ='#d0c3f7'
            symbol_brush_a = '#85ffb6'
            symbol_brush_v = '#9652d1'
            symbol_brush_h = '#d0c3f7'
            self.plot_widget_acceleration.clear()
            self.plot_widget_velocity.clear()
            self.plot_widget_height.clear()
            
            self.plot_widget_acceleration.getPlotItem().getAxis('bottom').setTextPen(color=text_color)
            self.plot_widget_acceleration.getPlotItem().getAxis('left').setTextPen(color=text_color)

            self.plot_widget_velocity.getPlotItem().getAxis('bottom').setTextPen(color=text_color)
            self.plot_widget_velocity.getPlotItem().getAxis('left').setTextPen(color=text_color)

            self.plot_widget_height.getPlotItem().getAxis('bottom').setTextPen(color=text_color)
            self.plot_widget_height.getPlotItem().getAxis('left').setTextPen(color=text_color)
            p = self.palette()
            p.setColor(self.backgroundRole(), QColor(background_color))
            p.setColor(self.foregroundRole(), QColor(text_color))
            self.setPalette(p)
        else:
            background_color = '#fff'
            text_color = '#111'
            pen_color_a ='#2B2A32'
            pen_color_v ='#3d2163'
            pen_color_h ='#355eab'
            symbol_brush_a = '#2B2A32'
            symbol_brush_v = '#3d2163'
            symbol_brush_h = '#355eab'
        self.plot_widget_acceleration.clear()
        self.plot_widget_velocity.clear()
        self.plot_widget_height.clear()
        self.plot_acceleration = self.plot_widget_acceleration.plot(
            pen=pen_color_a, symbolBrush=symbol_brush_a, symbolPen=background_color)
        self.plot_velocity = self.plot_widget_velocity.plot(
            pen=pen_color_v, symbolBrush=symbol_brush_v, symbolPen=background_color)
        self.plot_height = self.plot_widget_height.plot(
            pen=pen_color_h, symbolBrush=symbol_brush_h, symbolPen=background_color)
        self.plot_widget_acceleration.getPlotItem().getAxis('bottom').setTextPen(color=text_color)
        self.plot_widget_acceleration.getPlotItem().getAxis('left').setTextPen(color=text_color)

        self.plot_widget_velocity.getPlotItem().getAxis('bottom').setTextPen(color=text_color)
        self.plot_widget_velocity.getPlotItem().getAxis('left').setTextPen(color=text_color)

        self.plot_widget_height.getPlotItem().getAxis('bottom').setTextPen(color=text_color)
        self.plot_widget_height.getPlotItem().getAxis('left').setTextPen(color=text_color)
    
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(background_color))
        p.setColor(self.foregroundRole(), QColor(text_color))
        self.setPalette(p)

        # Aplicar as alterações aos gráficos
        self.plot_widget_acceleration.setBackground(background_color)
        self.plot_widget_velocity.setBackground(background_color)
        self.plot_widget_height.setBackground(background_color)

        self.plot_widget_acceleration.setTitle('Aceleração', color=text_color)
        self.plot_widget_acceleration.setLabel(
            'left', 'α (m/s²)', color=text_color)
        self.plot_widget_acceleration.setLabel(
            'bottom', 'tempo (s)', color=text_color)

        self.plot_widget_velocity.setTitle('Velocidade', color=text_color)
        self.plot_widget_velocity.setLabel('left', 'v (m/s)', color=text_color)
        self.plot_widget_velocity.setLabel(
            'bottom', 'tempo (s)', color=text_color)

        self.plot_widget_height.setTitle('Altura', color=text_color)
        self.plot_widget_height.setLabel('left', 'h (m)', color=text_color)
        self.plot_widget_height.setLabel(
            'bottom', 'tempo (s)', color=text_color)


def main():
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    graph_widget = GraphWidget(main_window)
    main_window.setCentralWidget(graph_widget)
    main_window.setGeometry(100, 100, 800, 600)
    main_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
