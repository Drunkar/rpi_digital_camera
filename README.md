# rpi_digital_camera

## Features

- After boot, be ready to use.
- Press button, capture image.
- Save the image to a usb storage.


## 仕様
- !データの保存場所
- !データの保存名
- !USBデバイスがない場合
- !USBデバイスが複数ある場合


## Initial setup (for developper)

### Environment settings

> !After raspbian install.

```
# enable sshd
sudo raspi-config
> 5 Interfacing Options > P2 SSH

# enable camera
sudo raspi-config
> 5 Interfacing Options > P1 Camera

# memory settings
sudo raspi-config
> 7 Advanced Options > A3 Memory Split > 256

# setup dependencies
sudo apt-get update
sudo apt-get -y upgrade
sudo rpi-update
sudo apt-get install python-picamera
sudo apt-get install ntfs-3g
```

### Register as a service

```
sudo cp rpicam.service /etc/systemd/system/rpicam.service
sudo chmod +x rpi_digital_camera.py
sudo reboot
```
