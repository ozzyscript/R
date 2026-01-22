"""
Recognizer (R)

R is a simple program (built for learning) tries to simulate
Keyboard and Mouse input only using hand gestures.

What can you do with R so far

Keyboard:

- Type all alphabit A-Z/a-z capital and small 
- Type all numbers 0-9
- Type all punctuation 
- Type all char that programmer needs
- Simulate SHIFT, CTRL SUPER(wind) keys
- Simulate Arrow keys, Enter, Backspace, Tab and Esc


Mouse:

- Move cursor up, down , left and right
- Move cursor diagonally in 4 directions
- Simulate left , right  and middle click (wheel)
- Simulate double click left
- Simulate wheel scrolling up/down


Other things:

- Control media
- Open app menu / close an app
- Resize window (hyprland) 
- Toggle fullscreen


For more info check the Docs dir(folder).
"""

import cv2 as cv
import mediapipe as mp
import time
from collections import deque
from mouse import update_mouse_physics, mouse_move_accelerated
from helper import draw_landmarks,filter_gesture
from mouse import MOUSE_MOVES
from consts import COMBO_COMMANDS, GESTURE_COMMANDS


# ======== Initialization  =========

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a gesture recognizer instance with the video mode:
options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='gesture_recognizer.task'),
    running_mode=VisionRunningMode.VIDEO, num_hands=2)



# confirm that we receive input from Cam device
# Note on Linux I have experienced Ext-Cam name
# changes video0 and video2
cap = cv.VideoCapture("/dev/video0") # external cam on Linux
if not cap.isOpened():
    print("Can't open camera.")
    exit() 



# ========= Starting point =========

def main(show_skeleton=False): 

    # Buffer to store only last N detected gestures.
    # when Nth is added, oldest one will be dropped.
    buffer = deque(maxlen=8)
   
    # Store trigger time in sec from time.time()
    # to calculate the difference.
    last_trigger_time = 0.0


    # pause / resume the input
    paused = False 

    with GestureRecognizer.create_from_options(options) as recognizer:

        start_time = time.time()
        while cap.isOpened():

            update_mouse_physics()
            
            ret, frame = cap.read()

            if not ret:
                print("Can't receive frame.Did you stop it? Exiting...")
                break
            
              
            rgb_img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_img)
            timestamp = int((time.time() - start_time) * 1000)
            result = recognizer.recognize_for_video(mp_image, timestamp)
            

            gesture,last_trigger_time =  filter_gesture(
                    result=result, buffer=buffer,
                    last_trigger_time=last_trigger_time,
            )

            # Pause / active the input, left + right dislike
            if isinstance(gesture, tuple) and gesture == ("dislike", "dislike"):
                paused = not paused  # Toggle state
                state = "PAUSED" if paused else "RESUMED"
                print(f"SYSTEM {state}")
                continue # skip any gesture except dislike.

            if paused:
                continue # skip all processing during pause

            # cursor movement  
            if isinstance(gesture, tuple):
                
                left, right = gesture

                # Use left-hand as mouse mode/modifier
                # Right hand to perform cursor movements
                if left == "fist" and right in MOUSE_MOVES:
                    mouse_move_accelerated(right)
                    continue  # Skip other commands during movement
            
                
            if gesture:

                if isinstance(gesture, tuple):
                    # detected gesture is combo 
                    cmd = COMBO_COMMANDS.get(gesture)
                    label = f"{gesture[0]} + {gesture[1]}"

                    #detected gesture is right hand.
                else:
                    cmd = GESTURE_COMMANDS.get(gesture)
                    label = gesture

                if cmd:
                    cmd()
                    print("EXECUTED:", label)
                else:
                    print("UNMAPPED:", label)

            if show_skeleton:
                draw_landmarks(result,frame)
            # cv.imshow('frame', frame)
            
            if cv.waitKey(1) == ord('q'):
                break


        cap.release()
        cv.destroyAllWindows()

main(show_skeleton=True)
