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

![szach_after_img](https://github.com/user-attachments/assets/4c53b3b9-6f42-4919-a855-22dd1daeb69a)

Next exec process script to calculate calibration matrix:
```console
python3 process.py
```
Finally start detection app:
```console
python3 detect.py
```

![distances_3d](https://github.com/user-attachments/assets/9071a2fb-b7e9-43e5-b8cd-dd4118f0405c)

Photos from field tests:

![distances_measure](https://github.com/user-attachments/assets/96f960a4-6363-4bce-8f34-4a4875b759a6)

![drone_fly](https://github.com/user-attachments/assets/6570618a-48a1-4ada-b489-72bfff62e1a8)

![teren_znaczniki_1](https://github.com/user-attachments/assets/4cab57a9-8c7c-49ea-88cc-5b847d684290)

