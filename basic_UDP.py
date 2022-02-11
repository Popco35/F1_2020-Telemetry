import socket
from f1_2020_telemetry.packets import *

import math
import matplotlib.pyplot as plt
import numpy as np
import time


def getPacketID(packet):
    packet_str = str(packet)
    index = packet_str.find("packetId=")
    if index != -1:
        return packet_str[index+len("packetId=")]


udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
udp_socket.bind(("", 20777))


while True:
    udp_packet = udp_socket.recv(2048)
    packet = unpack_udp_packet(udp_packet)
    if isinstance(packet, PacketCarTelemetryData_V1):
        print(packet.carTelemetryData[0].throttle)
        print()
