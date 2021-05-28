import pickle
import socket
import traceback
from threading import Thread

import numpy as np
from kivymd.toast import toast

from . import message
from .models import LogisticRegression
from .utils import adaptive_batch_size, input_size


class ClientThread(Thread):

    def __init__(self, client):
        super(ClientThread, self).__init__()
        self.client = client
        self.sock = client.sock
        self.terminate = False

    def run(self):
        # Wait for messages from server
        while not self.terminate:
            try:
                buffer = b''
                while buffer == b'':
                    buffer = self.sock.recv(102400)
                # print("buffer: ", len(buffer))
                if buffer:
                    data = pickle.loads(buffer)
                    if data and data['mtype'] == message.TRAIN_JOIN:
                        self.join_train(data['data'])
                    elif data and data['mtype'] == message.TRAIN_START:
                        self.client.local_train(data['data'])
                    elif data and data['mtype'] == message.TRAIN_STOP:
                        self.stop_train(data['data'])
                    elif data and data['mtype'] == message.DISCONNECT:
                        self.stop()
                    else:
                        toast(f"Unknown type of message: {data['mtype']}.")
            except pickle.UnpicklingError as e:
                toast(f"Corrupted message: {e}")
                traceback.print_exc()
            except socket.timeout:
                pass
            except Exception as e:
                self.terminate = True
                toast(f"Socket Exception: {e}")
                traceback.print_exc()

        self.sock.close()
        toast(f"Client disconnected")

    def send(self, msg):
        try:
            self.sock.sendall(msg)
        except socket.error as e:
            self.terminate = True
            toast(f"Socket error\n{e}")
        except Exception as e:
            toast(f"Exception\n{e}")

    def stop(self):
        self.terminate = True

    def join_train(self, data):
        self.client.params.lr = data.get('lr', self.client.params.lr)
        self.client.model = data.get('model', None)
        if data['model_name'] == "LR":
            features = input_size(data['model_name'], "mnist")
            self.client.model = LogisticRegression(features, lr=self.client.params.lr)
            self.client.model.batch_size = adaptive_batch_size(self.client.profile)
            self.client.log(log="Joined training, waiting to start ...")

            print(data['model_name'])
            print(self.client.model)
            print(self.client.model.batch_size)
            print(self.client.model.lr)

        else:
            toast(f"Model {data['model_name']} not supported.")
            exit(0)

    def stop_train(self, data):
        # go to predict screen
        self.client.log(log="Training finished.")
        self.client.manager.current = 'predict'
        summary = f"Training finished.\nAccuracy: {data['performance'][1]}\nLoss: {data['performance'][0]}\n" \
                  f"Battery usage: {data['battery_usage']}\nGlobal iteration cost: {round(data['iteration_cost'], 8)}" \
                  f"\nLocal iteration cost: {round(float(np.mean(self.client.iteration_cost)), 8)}"
        self.client.manager.get_screen("predict").ids.train_summary.text = summary
