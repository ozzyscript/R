"""
A simple program (for learning) to detect a gesture, 
and perform an action upon it. (execute system command)

That was achieved by using OpenCV and MediaPipe.

MediaPipe provides (7) default gestures which are:

Closed_Fist, Open_Palm, Pointing_Up 
Thumb_Down Thumb_Up Victory ILoveYou.

I found that a bit limited, so I fine tuned the 
model to add more gestures.

Now number of gestures is 20 and they are: 

Closed_Fist, call, no_gesture, dislike, fist, four
like, mute, ok, one, palm, peace, peace_inverted,
rock, stop, stop_inverted, three, three2
two_up, two_up_inverted.

For more info check Notes.txt.
"""


import cv2 as cv
import mediapipe as mp
import subprocess
import time
from collections import deque


# ======== Initialization  =========

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a gesture recognizer instance with the video mode:
options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='gesture_recognizer.task'),
    running_mode=VisionRunningMode.VIDEO, num_hands=1)



# ======== Constants  =========

GESTURE_COMMANDS = {
    "ok": lambda: subprocess.run(
        ["playerctl", "play-pause"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ),

    "fist": lambda: subprocess.run(
        ["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", "10%-"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ),

    "palm": lambda: subprocess.run(
        ["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", "10%+"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ),
}



# ======== Helpers  =========

def filter_gesture(result, buffer, last_trigger_time, cooldown_sec=0.8):
    """Filter and store gestures using debouncing  and cooldown lgoic"""
    
    if not result.gestures:
        return None,last_trigger_time

    now = time.time() # how many sec since January 0, 1970, 00:00:00 UTC, up till now. 

    gesture = result.gestures[0][0] # get first hand gestures  
    g_name = gesture.category_name # gesture name
    g_score = gesture.score # confidence level
    buffer.append(g_name) #gesture name.

    # A gesture must appear at least 3 times,
    # and score more than N% confidence level.
    # And waiting time must be at least -1.n secs.
    if (
        buffer.count(g_name) >= 4
        and g_score > 0.70 # 70 to 80 is good, more is strict, less is messy.
        and now - last_trigger_time >= cooldown_sec
        ):
        return g_name,now

    return None, last_trigger_time



def draw_landmarks(result,frame):
    """
    Draw Points and Lines to show a full skeleton.
    """
    if not result.hand_landmarks:
        return False
    
    # for performance move this out.
    # for readability keep it here.
    HAND_CONNECTIONS = (
    (0, 1), (1, 2), (2, 3), (3, 4),       # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),       # Index
    (0, 9), (9,10), (10,11), (11,12),     # Middle
    (0,13), (13,14), (14,15), (15,16),    # Ring
    (0,17), (17,18), (18,19), (19,20),    # Pinky
    )

    # numpy array (height, width, channels)
    h,w,_ = frame.shape

    # detect the hands
    for hand_landmarks in result.hand_landmarks:
        points = []
        
        # draw circles 
        for landmark in hand_landmarks:
            # Mediapipe uses normalized coordinates x,y (0 to 1)
            # While OpenCV uses pixels coordinates (0, N-1)
            # we must convert from normalized coordinates to
            # pixels, so openCV can understand them.
            x = int(landmark.x * w)
            y = int(landmark.y * h)

            points.append((x,y))

            # draw a circle for each landmark.
            cv.circle(frame, (x,y), 4, (0, 255, 0), -1)
        
        # draw lines between points 
        for start, end in HAND_CONNECTIONS:
            cv.line(frame, points[start], points[end], (255, 0, 0), 2)


# confirm that we receive input from Cam device
cap = cv.VideoCapture("/dev/video2") # external cam on Linux
if not cap.isOpened():
    print("Can't open camera.")
    exit() 



# ========= Starting point =========

def main(show_skilton=False): 
    # Buffer to store only last 4 detected gestures.
    # when 5th is added, oldest one will be dropped.
    buffer = deque(maxlen=4)
   
    # Store trigger time in sec from time.time()
    # So we can calculate the difference.
    last_trigger_time = 0.0

    with GestureRecognizer.create_from_options(options) as recognizer:
        
        timestamp = 0

        while cap.isOpened():

            ret, frame = cap.read()

            if not ret:
                print("Can't receive frame.Did you stop it? Exiting...")
                break
            
              
            rgb_img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_img)
            result = recognizer.recognize_for_video(mp_image, timestamp)
            

            if show_skilton:
                draw_landmarks(result,frame)
            
            gesture, last_trigger_time =  filter_gesture(
                    result=result, buffer=buffer,
                    last_trigger_time=last_trigger_time,
                           )

            if gesture:
                cmd = GESTURE_COMMANDS.get(gesture)
                if cmd:
                    cmd()
                    print("EXECUTED:", gesture)
                else:
                    print("UNMAPPED GESTURE:", gesture)


            cv.imshow('frame', frame)
            
            if cv.waitKey(1) == ord('q'):
                break
            timestamp += 33
        
        cap.release()
        cv.destroyAllWindows()


main(show_skilton=True)









