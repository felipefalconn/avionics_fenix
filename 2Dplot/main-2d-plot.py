import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt

class GraphWidget(QWidget):
    def __init__(self, parent=None):
        super(GraphWidget, self).__init__(parent)

        self.time_data = np.arange(1, 201)
        self.velocity_random = np.random.uniform(-10, 30, 200)
        self.acceleration_random = np.random.uniform(-5, 5, 200)
        self.height_random = np.cumsum(self.velocity_random)

        self.plot_widget_acceleration = pg.PlotWidget(self)
        self.plot_widget_velocity = pg.PlotWidget(self)
        self.plot_widget_height = pg.PlotWidget(self)

        self.init_plots()

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.plot_widget_acceleration, 0, 0)
        self.layout.addWidget(self.plot_widget_velocity, 0, 1)
        self.layout.addWidget(self.plot_widget_height, 1, 0, 1, 2)  # Ocupa duas colunas

        self.animation_timer = pg.QtCore.QTimer(self)
        self.animation_timer.timeout.connect(self.update_plot)
        self.frame = 0

        self.init_ui()

        # Definindo a variável para rastrear o modo atual (claro ou escuro)
        self.is_dark_mode = False

    def init_plots(self):
        self.plot_acceleration = self.plot_widget_acceleration.plot(pen='#2B2A32', symbolBrush='#2B2A32', symbolPen='w')
        self.plot_widget_acceleration.setTitle('Aceleração', color='k')  # Título em preto
        self.plot_widget_acceleration.setLabel('left', 'α (m/s²)')
        self.plot_widget_acceleration.setLabel('bottom', 'tempo (s)', color='k')
        self.plot_widget_acceleration.setBackground('w')  # Fundo branco

        self.plot_velocity = self.plot_widget_velocity.plot(pen='#3d2163', symbolBrush='#3d2163', symbolPen='w')
        self.plot_widget_velocity.setTitle('Velocidade', color='k')  # Título em preto
        self.plot_widget_velocity.setLabel('left', 'v (m/s)')
        self.plot_widget_velocity.setLabel('bottom', 'tempo (s)', color='k')
        self.plot_widget_velocity.setBackground('w')  # Fundo branco

        self.plot_height = self.plot_widget_height.plot(pen='#355eab', symbolBrush='#355eab', symbolPen='w')
        self.plot_widget_height.setTitle('Altura', color='k')  # Título em preto
        self.plot_widget_height.setLabel('left', 'h (m)')
        self.plot_widget_height.setLabel('bottom', 'tempo (s)', color='k')
        self.plot_widget_height.setBackground('w')  # Fundo branco

        self.plot_widget_acceleration.getPlotItem().getAxis('bottom').setTextPen(color='#000000')
        self.plot_widget_acceleration.getPlotItem().getAxis('left').setTextPen(color='#000000')

        self.plot_widget_velocity.getPlotItem().getAxis('bottom').setTextPen(color='#000000')
        self.plot_widget_velocity.getPlotItem().getAxis('left').setTextPen(color='#000000')

        self.plot_widget_height.getPlotItem().getAxis('bottom').setTextPen(color='#000000')
        self.plot_widget_height.getPlotItem().getAxis('left').setTextPen(color='#000000')



    def init_ui(self):
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

        self.layout.addLayout(button_layout, 2, 0, 1, 2)  # Adiciona os botões na linha 2

        for button in [self.show_acceleration_button, self.show_velocity_button, self.show_height_button, self.dark_mode_button]:
            button.clicked.connect(self.toggle_button)

        self.animation_timer.start(1000)  # 1000 milliseconds interval

    def update_plot(self):
        if self.frame < len(self.time_data):
            self.plot_acceleration.setData(self.time_data[:self.frame + 1], self.acceleration_random[:self.frame + 1], symbol='o')
            self.plot_velocity.setData(self.time_data[:self.frame + 1], self.velocity_random[:self.frame + 1], symbol='o')
            self.plot_height.setData(self.time_data[:self.frame + 1], self.height_random[:self.frame + 1], symbol='o')
            self.frame += 1
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
        # Alternar entre os modos claro e escuro
        self.is_dark_mode = not self.is_dark_mode

        if self.is_dark_mode:
            background_color = '#111'
            text_color = '#fff'
            self.plot_widget_acceleration.clear()
            self.plot_widget_velocity.clear()
            self.plot_widget_height.clear()
            self.plot_acceleration = self.plot_widget_acceleration.plot(pen='#85ffb6', symbolBrush='#85ffb6', symbolPen='#111')
            self.plot_velocity = self.plot_widget_velocity.plot(pen='#9652d1', symbolBrush='#9652d1', symbolPen='#111')
            self.plot_height = self.plot_widget_height.plot(pen='#d0c3f7', symbolBrush='#d0c3f7', symbolPen='#111')
            self.plot_widget_acceleration.getPlotItem().getAxis('bottom').setTextPen(color='w')
            self.plot_widget_acceleration.getPlotItem().getAxis('left').setTextPen(color='w')

            self.plot_widget_velocity.getPlotItem().getAxis('bottom').setTextPen(color='w')
            self.plot_widget_velocity.getPlotItem().getAxis('left').setTextPen(color='w')

            self.plot_widget_height.getPlotItem().getAxis('bottom').setTextPen(color='w')
            self.plot_widget_height.getPlotItem().getAxis('left').setTextPen(color='w')

        else:
            background_color = 'w'
            text_color = 'k'
            self.plot_acceleration = self.plot_widget_acceleration.plot(pen='#2B2A32', symbolBrush='#2B2A32', symbolPen='w')
            self.plot_velocity = self.plot_widget_velocity.plot(pen='#3d2163', symbolBrush='#3d2163', symbolPen='w')
            self.plot_height = self.plot_widget_height.plot(pen='#355eab', symbolBrush='#355eab', symbolPen='w')



        # Aplicar as alterações aos gráficos
        self.plot_widget_acceleration.setBackground(background_color)
        self.plot_widget_velocity.setBackground(background_color)
        self.plot_widget_height.setBackground(background_color)

        self.plot_widget_acceleration.setTitle('Aceleração', color=text_color)
        self.plot_widget_acceleration.setLabel('left', 'α (m/s²)', color=text_color)
        self.plot_widget_acceleration.setLabel('bottom', 'tempo (s)', color=text_color)

        self.plot_widget_velocity.setTitle('Velocidade', color=text_color)
        self.plot_widget_velocity.setLabel('left', 'v (m/s)', color=text_color)
        self.plot_widget_velocity.setLabel('bottom', 'tempo (s)', color=text_color)

        self.plot_widget_height.setTitle('Altura', color=text_color)
        self.plot_widget_height.setLabel('left', 'h (m)', color=text_color)
        self.plot_widget_height.setLabel('bottom', 'tempo (s)', color=text_color)

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
