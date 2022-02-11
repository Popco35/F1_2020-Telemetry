from sqlite3 import Time
#from PyQt5 import QtWidgets, QtCore
from PySide6 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
import socket
from f1_2020_telemetry.packets import *
from random import randint


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("F1 Telemetry")
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        # Create list with all telemetry
        self.x = list(range(100))  # 100 time points
        self.yThrottle = list(range(100))
        self.yBrake = list(range(100))
        self.ySpeed = list(range(100))

        # set background color, axis and title
        self.graphWidget.setBackground('w')
        self.graphWidget.setTitle("F1 2020 Telemetry")
        styles = {'color': 'b', 'font-size': '20px'}
        self.graphWidget.setLabel('left', 'Percentage(%)', **styles)
        self.graphWidget.setLabel('bottom', 'Time', **styles)
        self.graphWidget.setLabel('right', 'Speed (Km/h)', **styles)

        # Creating dataline for each plot that is rendered
        penT = pg.mkPen(color=(255, 0, 0))
        penB = pg.mkPen(color=(0, 0, 255))
        pen = pg.mkPen(color=(0, 0, 0))
        self.data_line = self.graphWidget.plot(
            self.x, self.yThrottle, pen=penT, name="Throttle")
        self.data_line2 = self.graphWidget.plot(
            self.x, self.yBrake, pen=penB, name="Brake")
        self.data_line3 = self.graphWidget.plot(
            self.x, self.ySpeed, pen=pen, name="Speed")
        # Set timer with update_data function
        self.graphWidget.addLegend()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(3)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

        self.graphWidget.setYRange(0, 100, padding=0.05)

    def update_plot_data(self):
        udp_packet = udp_socket.recv(2048)
        packet = unpack_udp_packet(udp_packet)
        if isinstance(packet, PacketCarTelemetryData_V1):

            self.yThrottle = self.yThrottle[1:]  # Remove the first
            # Add a new random value.
            self.yThrottle.append(packet.carTelemetryData[0].throttle*100)

            self.yBrake = self.yBrake[1:]  # Remove the first
            # Add a new random value.
            self.yBrake.append(packet.carTelemetryData[0].brake*100)
            self.ySpeed = self.ySpeed[1:]  # Remove the first
            # Add a new random value.
            self.ySpeed.append(0.2777777*packet.carTelemetryData[0].speed)

            self.x = self.x[1:]  # Remove the first y element.
            # Add a new value 1 higher than the last.
            self.x.append(self.x[-1] + 1)

        # Update the data.
        self.data_line.setData(self.x, self.yThrottle)
        self.data_line2.setData(self.x, self.yBrake)
        self.data_line3.setData(self.x, self.ySpeed)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    global udp_socketp
    udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_socket.bind(("", 20777))
    main()
