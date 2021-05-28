import pickle
import socket
import traceback
from threading import Thread

from . import message
from .utils import log


class DeviceConnection(Thread):

    def __init__(self, server, sock, address):
        super(DeviceConnection, self).__init__()
        self.server = server
        self.sock = sock
        self.address = address
        self.terminate = False

    def run(self):
        # Wait for messages from device
        while not self.terminate:
            try:
                buffer = b''
                while buffer == b'':
                    buffer = self.sock.recv(8192)  # 165536
                if buffer:
                    print(f"Server got buffer: {len(buffer)}")
                    data = pickle.loads(buffer)
                    if data and data['mtype'] == message.TRAIN_INFO:
                        self.handle_epoch(data['data'])
                    elif data and data['mtype'] == message.DISCONNECT:
                        self.handle_disconnect()
                    else:
                        log('error', f"{self.server.name}: Unknown type of message: {data['mtype']}.")
            except pickle.UnpicklingError as e:
                log('error', f"{self.server.name}: Corrupted message : {e}")
            except socket.timeout:
                pass
            except Exception as e:
                self.terminate = True
                print(f"workers1: {len(self.server.workers)}")
                self.server.workers.remove(self)
                print(f"workers2: {len(self.server.workers)}")
                log('error', f"{self.server.name} DeviceConnection: Socket Exception\n{e}")
                traceback.print_exc()

        self.sock.close()
        log('info', f"{self.server.name}: Worker disconnected")

    def send(self, msg):
        try:
            self.sock.sendall(msg)
        except socket.error as e:
            self.terminate = True
            log('error', f"{self.server.name} DeviceConnection: Socket error\n{e}")
        except Exception as e:
            log('error', f"{self.server.name} DeviceConnection: Exception\n{e}")
            traceback.print_exc()

    def stop(self):
        self.terminate = True

    def handle_epoch(self, data):
        self.server.grads.append(data['grads'])
        self.server.update_status()
        self.server.battery_usage.append(data['battery'])
        self.server.iteration_cost.append(data['time'])
        self.server.aggregate()

    def handle_disconnect(self):
        self.terminate = True
        self.sock.close()
        self.server.workers.remove(self)
