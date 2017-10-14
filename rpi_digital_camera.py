#!/usr/bin/env python
# coding: utf-8
"""
- After boot, be ready to use.
- Press button, capture image.
- Save the image to a usb storage.

In the case:
- No USB storage detected: cannot save the image.
- Multiple USB storage detected: use the first one (order by UUID(probably)).
"""

import os
import time
import picamera
import argparse
import logging
import shutil
import RPi.GPIO as GPIO
from datetime import datetime

logger = logging.getLogger()
MEDIA_DIR = "/media/pi/"
SAVE_DIR_NAME = "DCIM"
FILENAME_PREFIX = "picam"
BUTTON_PIN = 18
STATUS_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(STATUS_PIN, GPIO.OUT)
GPIO.output(STATUS_PIN, 0)


def blinking(pin):
    for i in range(6):
        GPIO.output(pin, 1)
        time.sleep(0.1)
        GPIO.output(pin, 0)
        time.sleep(0.1)


def save_img_to_storage(tmp_file, cap_time):
    try:
        media = os.listdir(MEDIA_DIR)
        logger.debug(media)
    except Exception as e:
        logger.error(e)
        media = []

    # when storage is mounted, save image.
    if len(media) == 0:
        blinking(STATUS_PIN)
        raise Exception("No storage devices!")

    media_root = os.path.join(MEDIA_DIR, media[0])
    directories = os.listdir(media_root)
    logger.debug(directories)
    # mkdir
    if SAVE_DIR_NAME not in directories:
        os.mkdir(os.path.join(media_root, SAVE_DIR_NAME))
    filename = FILENAME_PREFIX + "_" + \
        cap_time.strftime("%Y%m%d_%H%M%S%f") + ".jpg"
    shutil.copy2(tmp_file, os.path.join(media_root, SAVE_DIR_NAME, filename))
    return True


def capture_and_save(camera):
    tmp_file = "/tmp/" + FILENAME_PREFIX + "_tmp.jpg"
    camera.capture(tmp_file)
    cap_time = datetime.now()
    saved = save_img_to_storage(tmp_file, cap_time)
    if not saved:
        raise Exception("Cannot save image!")


def main():
    sw_status = 1
    with picamera.PiCamera() as camera:
        camera.resolution = camera.MAX_RESOLUTION
        logger.debug("Camera starting...")
        camera.start_preview(resolution=(1024, 768))
        # Camera warm-up time
        time.sleep(2)
        logger.debug("Ready.")
        GPIO.output(STATUS_PIN, 1)
        try:
            while True:
                sw_status = GPIO.input(BUTTON_PIN)
                if sw_status == 0:
                    logger.debug("Button pressed.")
                    GPIO.output(STATUS_PIN, 0)
                    GPIO.output(STATUS_PIN, 0)
                    capture_and_save(camera)
                    logger.info("The image was successfully saved.")
                    logger.debug("Ready.")
                    GPIO.output(STATUS_PIN, 1)
        except Exception as e:
            logger.error(e)
        finally:
            camera.close()


if __name__ == '__main__':
    # args
    parser = argparse.ArgumentParser(
        description="Generate 24 hours instagram hashtag and word ranking.")
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Debug mode.")
    args = parser.parse_args()

    # logger
    if args.debug:
        LOG_LEVEL = logging.DEBUG
    else:
        LOG_LEVEL = logging.INFO
    formatter = logging.Formatter(
        fmt="[%(asctime)s] %(levelname)s [%(name)s/%(funcName)s() at line %(lineno)d]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    logger.setLevel(LOG_LEVEL)
    # stdout出力
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(LOG_LEVEL)
    logger.addHandler(stream_handler)

    try:
        while True:
            main()
            time.sleep(1)
    except Exception as e:
        logger.error(e)
    finally:
        GPIO.cleanup()
