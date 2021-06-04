# SmartFed: Democratizing Federated Learning

> This repository contains the code for the Android implementation of the SmartFed algorithm. This Application is for demonstration purposes and it is by no means built for production usage.

---

### **Backend**: Parameter Server (PS)

The `backend` folder contains the code for the parameter server (PS). It can be deployed on a local machine or in the cloud with a public IP address.

The PS accepts connections and disconnections from any device at any time. Each connected device is sent the machine learning model with current parameters. Once a new round it started the PS sends the model parameters and the selected block for training in the next round.

A disconnected or stale device are considered as new devices and receive the most recent model parameters once they are connected again.

#### Install python requirements

```
pip install -r requirements.txt
```

#### Congifure and run the PS

To configure the Parameter Server update the configuration file `backend/config.py`. the default parameters are: 

```
# file: backend/config.py
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 45000
ROUNDS = 500
FRAC = 0.8
BLOCK_SIZE = 0
LEARNING_RATE = 0.001
GAR = "average"
F = 0
ATTACK = "No"
MIN_ACTIVE_WORKERS = 2
```
Download the `MNIST` dataset for model evaluation and move it the the datasets folder `backend/datasets`.

`MNIST` download link: https://mega.nz/file/3aA2VLLD#vdW4CjZg3TRqD2qECdGgLZ9Iu8N0w2EAobQV298Hqi8



To run the Parameter Server execute the following commands:

```
cd backend
python main.py
```



### **Frontend**: Android application.

The smartphone implementation of SmartFed uses the python cross platform library kivy (\url{https://kivy.org}). Our code is optimized to deploy the Android version. However, the application is cross platform and can be deployed also on IOS, Linux, macOS and Windows with the appropriate modifications. The application works on Android version 7+ and only requires storage permission to access the smartphone local dataset.

#### Build the android application
Install buildozer: https://buildozer.readthedocs.io/en/latest/installation.html

Execute the following command to build the Android application:

```
cd frontend
buildozer android debug deploy run logcat
```



#### Usage

The application needs first to be configured by setting the correct IP address and port of the server. Next, the computation profile needs to be selected. For simplicity, we suggest three configurable computation profiles with the following default values:

- Low configuration: train the model using only 16 data points at each round.
- Moderate configuration: train the model using 128 data points at each round.
- Powerful configuration: train the model using the number of data points chosen specified in the “Number of samples” text input.

Once configured, the application will receive the selected model from the PS and start training once the PS sends the current model parameters and the selected block to train in the next round. Once the training is finished, a new screen is activated with a summary of the training.

#### Screenshots

<img src="https://tva1.sinaimg.cn/large/008i3skNgy1gr6q3b7lw9j30u01t0q6f.jpg" alt="welcome" style="zoom:25%;" /><img src="https://tva1.sinaimg.cn/large/008i3skNgy1gr6q3q2lptj30u01t0q8w.jpg" alt="configure" style="zoom:25%;" /><img src="https://tva1.sinaimg.cn/large/008i3skNgy1gr6q3ykheaj30u01t0tbh.jpg" alt="train" style="zoom:25%;" /><img src="https://tva1.sinaimg.cn/large/008i3skNgy1gr6q43qb1gj60u01t0jvo02.jpg" alt="result" style="zoom:25%;" />




