import socket
import _multiprocessing

_multiprocessing.sem_unlink = None
import joblib
import plyer
import numpy as np
from kivymd.toast import toast

from conf import LOW_BATCH_SIZE, MOD_BATCH_SIZE, POW_BATCH_SIZE, DEFAULT_BATCH_SIZE


class Map(dict):
    """
    Example:
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """

    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]


def create_tcp_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, TCP_SOCKET_BUFFER_SIZE)
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, TCP_SOCKET_BUFFER_SIZE)
    # sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    return sock


def mnist(path, binary=True):
    try:
        open(path, 'r')
    except FileNotFoundError as e:
        toast(str(e))
        exit()
    X_train, Y_train = joblib.load(path)
    Y_train = Y_train.astype(int).reshape(-1, 1)
    if binary:
        # Extract 1 and 2 from train dataset
        f1 = 1
        f2 = 2
        Y_train = np.squeeze(Y_train)
        X_train = X_train[np.any([Y_train == f1, Y_train == f2], axis=0)]
        Y_train = Y_train[np.any([Y_train == f1, Y_train == f2], axis=0)]
        Y_train = Y_train - f1
        Y_train = Y_train.reshape(-1, 1)
    else:
        Y_train = np.array([np.eye(1, 10, k=int(y)).reshape(10) for y in Y_train])
    X_train = X_train / 255

    return X_train, Y_train


def sample_data(dataset, num_items):
    all_idxs = [i for i in range(len(dataset.data))]
    mask = list(np.random.choice(all_idxs, num_items, replace=False))
    np.random.shuffle(mask)
    data = dataset.data[mask, :]
    targets = dataset.targets[mask]
    return Map({'data': data, 'targets': targets})


def adaptive_batch_size(profile):
    if profile == "low":
        return LOW_BATCH_SIZE
    elif profile == "mod":
        return MOD_BATCH_SIZE
    elif profile == "pow":
        return POW_BATCH_SIZE
    else:
        return DEFAULT_BATCH_SIZE


def input_size(model: str, dataset: str):
    if model.upper() in ["LR", "LN", "SVM"]:
        if dataset.lower() == "mnist":
            return 784
        elif dataset.lower() == "boston":
            return 14
        elif dataset.lower() == "phishing":
            return 68
        else:
            log('error', f"Unknown dataset {dataset}")
            exit(0)
    else:
        if dataset.lower() == "mnist":
            return [784, 30, 10]
        else:
            log('error', f"Unsupported or Unknown dataset {dataset}")
            exit(0)


def mah(battery_start, battery_capacity):
    level = battery_start - plyer.battery.status['percentage']
    # print(f"battery_start = {battery_start} | level = {plyer.battery.status['percentage']} | mah={(level * battery_capacity) / 100}")
    return (level * battery_capacity) / 100
