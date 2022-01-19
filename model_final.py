import math

import keyboard

import mss.tools

import numpy as np

import serial

import torch

import time

from PIL import Image

import cv2

arduino = serial.Serial('COM7', 9600, timeout=0)

# model = torch.hub.load('C:/yolov5-master', 'custom', path=r'C:\Users\user\Desktop\valorant_hack_inprogress\best.pt', source='local', force_reload=True) # to be changed

model = torch.hub.load(r'.\yolov5-master',
                       'custom', path=r'C:\Users\user\Desktop\valorant_aim_assist\best.pt',
                       source='local', force_reload=True) # to be changed

device = torch.device('cuda') # to be changed

# model.to(device) # to be changed

# model.cuda() # to be changed
print("now using cuda")

index = 0 # use to label the images

head_body_ratio_normal = 0.89  # to be changed represent the increase in y location of the cursor to ensure it hits the head
head_body_ratio_bulldog = 0.85 # for using bulldog
head_body_ratio_used = head_body_ratio_normal



with mss.mss() as sct:
    # Use the first monitor, change to desired monitor number

    dimensions = sct.monitors[1]

    SQUARE_SIZE = 600

    # Part of the screen to capture

    monitor = {"top": int((dimensions['height'] / 2) - (SQUARE_SIZE / 2)),

               "left": int((dimensions['width'] / 2) - (SQUARE_SIZE / 2)),

               "width": SQUARE_SIZE,

               "height": SQUARE_SIZE}

    while True:

        # READING OUTPUT FROM THE MODEL 

        # SCREEN CAPTURE AND CONVERTING TO MODEL'S SUPPORTED FORMAT

        # Screenshot

        BRGframe = np.array(sct.grab(monitor))

        # Convert to format model can read

        RGBframe = BRGframe[:, :, [2, 1, 0]]

        # PASSING CONVERTED SCREENSHOT INTO MODEL

        results = model(RGBframe, size=600)

        model.conf = 0.6

        # READING OUTPUT FROM MODEL AND DETERMINING DISTANCES TO ENEMIES FROM CENTER OF THE WINDOW

        # Get number of enemies / num of the rows of .xyxy[0] array 

        enemyNum = results.xyxy[0].shape[0]

        if enemyNum == 0:
            print("passing")
            pass

        else:

            # Reset distances array to prevent duplicating items 

            distances = []

            closest = 1000

            # Cycle through results (enemies) and get the closest

            for i in range(enemyNum):

                x1 = float(results.xyxy[0][i, 0])

                x2 = float(results.xyxy[0][i, 2])

                y1 = float(results.xyxy[0][i, 1])

                y2 = float(results.xyxy[0][i, 3])

                centerX = (x2 - x1) / 2 + x1

                centerY = (y2 - y1) / 2 + y1

                distance = math.sqrt(((centerX - 300) ** 2) + ((centerY - 300) ** 2))

                distances.append(distance)

                # Get the shortest distance from the array (distances)

                if distances[i] < closest:
                    closest = distances[i]

                    closestEnemy = i

                    # cv2.line(results.imgs[0], (int(centerX), int(centerY)), (300, 300), (255, 0, 0), 1, cv2.LINE_AA)

            # Getting the coordinates of the closest enemy

            x1 = float(results.xyxy[0][closestEnemy, 0])

            x2 = float(results.xyxy[0][closestEnemy, 2])

            y1 = float(results.xyxy[0][closestEnemy, 1])

            y2 = float(results.xyxy[0][closestEnemy, 3])



            Xenemycoord = (x2 - x1) / 2 + x1

            # Yenemycoord = (y2 - y1) / 2 * (1-head_body_ratio) + y1 # to be  changed

            # Yenemycoord = (y2 - y1) * (1 - head_body_ratio_bulldog) + y1  # to be  changed
            # Yenemycoord = (y2 - y1) * (1 - head_body_ratio_normal) + y1  # to be  changed
            Yenemycoord = (y2 - y1) * (1 - head_body_ratio_used) + y1  # to be  changed
            # MOVING THE MOUSE

            difx = int(Xenemycoord - (SQUARE_SIZE / 2))

            dify = int(Yenemycoord - (SQUARE_SIZE / 2))

            # # to be changed
            # if difx > 127:
            #     difx = 50
            # if difx < -127:
            #     difx = -50
            # if dify > 127:
            #     dify = 50
            # if dify < -127:
            #     dify = -50



            if not(keyboard.is_pressed('`')):
                print("moving crosshair")
                index += 1
                # data = str(difx) + ':' + str(dify) # to be changed stores the format of the mouse movement we change to ',' for now, originally is ':'


                data = str(difx) + ',' + str(dify) + '\n'


                arduino.write(data.encode())
                time.sleep(0.2) # to be changed

                print(data)

                # storing the output results as jpg images (optional)

                cv2.rectangle(results.imgs[0], tuple(int([x1, y1])), tuple(int([x2, y2])), (255,255,255), 2)
                im = Image.fromarray(results.imgs[0])
                im.save(f".\\outputs\\{index}.jpg")