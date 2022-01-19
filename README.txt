In order to use the AI, you need an arduino leonardo board with a host shield 

The weighting of the program is already pre-trained, if you prefer using your own trained model, you may replace it with the best.pt file
- remember to replace the coco128.yaml file with your file (name it the same as the coco128.yaml file or change the path in C:\Users\user\Desktop\valorant_aim_assist\yolov5-master\detect.py line 53)
- please make sure that the first label represents the enemy coordinates

the model_final.py (You may modify some of the contents)
-line 19 stores the port for the arduino leonardo board which can be checked with the arduino ide; the baud rate can also be customized (default is 9600)
-line 23 first argument requires a string with the path to the yolov5-master directory
-line 24 third argument requires a string with the path to the weighting file.pt
-line 27 enable this line to use gpu to run the model (recommended) 
	to use gpu, make sure that you have installed cuda and cudnn as shown in this video https://www.youtube.com/watch?v=StH5YNrY0mE
-line 36 Stores the normal head to body ratio of enemies, you may twitch with the values to your liking
-line 37 Stores the head to body of eneies for bulldog, you may twitch with the values to your liking
-line 38 Assign the ratio used to the variable head_body_ratio_used
-line 163 the key to stop the program from making mouse movements as long as its pressed down, it is '`' at default, you may change to any key you like
-line 177 - 181 to save the result inside the outputs file, optional (may affect program efficiency)


Arduino_valorant_mouse\Arduino_valorant_mouse.ino (You may modify some of the contents)
You should upload this code to your Arduino Leonardo board before using the program
Remember to sync the serial port and it's baud rate with the model_final.py


aim_assist_env.yml
Stores the environment needed for the Anaconda environment


Please follow https://www.youtube.com/watch?v=StH5YNrY0mE if you want to run the program with gpu (recommended)


How to use:
1: plug in the Arduino Leonardo board with host shield connected to a mouse or its receiver (some mouse may not be compatible)
2: activate the environment that is installed above and run "python path\model_final.py"
3: The program is now running



Reference: https://github.com/ultralytics/yolov5 https://www.youtube.com/watch?v=StH5YNrY0mE https://www.youtube.com/watch?v=K8qs9GlE4UQ https://www.unknowncheats.me/forum/valorant/467372-valorant-cheat-arduino-yolov5-ai.html https://www.youtube.com/watch?v=nBttwvgNOr8
