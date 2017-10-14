# rpi_digital_camera

## Features

- After boot, be ready to use.
- Press button, capture image.
- Save the image to a usb storage.

## 利用の流れ
1. 電源入れる
2. 準備ができたらLEDが点灯するので、USBメモリを入れる
3. LEDがついてるときにボタンを押すと撮影。
4. その場でUSBメモリに保存(ここで3-5秒かかる)
5. ふたたびLEDが点灯したら撮影可能

## 連続撮影速度について
- いま3-5秒。これはUSBへの書き込みに時間がかかるため。
- もし画像の解像度を下げれば、連続撮影速度はあげられる。
- 解像度はいま3280x2464で、ラズパイカメラの最大解像度。1画像5MBぐらい。
- それか、撮影と別の並列処理でUSBへの保存を行うならば連続撮影時間は大きく短縮可能。ただしこれは追加の工数かかります。

---

# 開発者向けの内容

## Environment

name|description
:--|:--
OS  | RASPBIAN STRETCH WITH DESKTOP Version September 2017
SD Card  | 8GB

## 仕様
- データの保存場所: USBメモリに`DCIM`フォルダを作り、画像を保存します。すでに`DCIM`フォルダがある場合は、その中に保存します。
- データ名: picam_YYYYMMDD_hhmmssffffff.jpg (日付時刻ミリ秒)
- USBメモリが挿入されてない場合: 撮影はできるが保存されない
- USBメモリが複数挿入されている場合: どれかひとつに保存される


## Initial setup (for developper)

### Environment settings

>  After raspbian install.

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
git clone https://github.com/Drunkar/rpi_digital_camera.git
cd rpi_digital_camera
sudo cp rpicam.service /etc/systemd/system/rpicam.service
sudo systemctl enable rpicam
sudo chmod +x rpi_digital_camera.py
sudo reboot
```
