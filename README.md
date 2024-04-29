# uav-opencv-vision-system
Dedicated for Raspberry Pi 4

```console
sudo apt update && upgrade
```
```console
python3 -m venv venv_name
```

```console
source nazwa venv_name/bin/activate
```

```console
sudo apt install libopencv-dev libatlas-base-dev libjasper-dev libqtgui4
python3-pyqt5 libhdf5-dev libhdf5-103
```
```console
pip install numpy
```

```console
pip install opencv-python
```
or
```console
pip install opencv-contrib-python
```

Calibrate your camera with calibration script:

```console
python3 cam_calibration.py
```
Take a few photos of calibration board in various positions.

Next exec process script to calculate calibration matrix:
```console
python3 process.py
```
Finally start detection app:
```console
python3 detect.py
```
