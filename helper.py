import subprocess
import cv2 as cv
import time


def hypr(cmd, *args):

    """
    receive and execute hyprlnad commands 
    """
    subprocess.run(
        ["hyprctl", "dispatch", cmd, *args],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def extract_hand_gestures(result):

    """
    Identify  hands (left, right).
    Detect gestures,then assign them the correct hand (Left, Right).
    Finally return result as Dictionary.
        {
            "left": ("palm", 0.91),
            "right": ("ok", 0.95)
        }
    """ 

    # store left/right gestures or both, and return them.
    # If not exist return none.
    hands = {"left": None, "right": None}

    # result.gestures = the detected gesture.
    # result.handedness = which hand left or right.
    if not result.gestures or not result.handedness:
        return hands
    
    
    for i, handedness in enumerate(result.handedness):

        # store which hand is detected (L/R). Based on the highest confidence level
        label = handedness[0].category_name.lower() 
        
        # store the detected gesture based on the highest score, for each hand.
        gesture = result.gestures[i][0]

        # assign the gesture name and confidence score to the hand.
        hands[label] = (gesture.category_name, gesture.score)

    return hands


def filter_gesture(result, buffer, last_trigger_time, cooldown_sec=1.0):
    """
    Filter detected gestures.
    Check if the right hand is present.
    Check if the gesture is stable enough to be executed.
    Check if left hand is present to make combo with the right hand.
    Finally return:
    1 gesture name for right hand or for both hands, if 
    left's hand gesture is detected and stable.
    note: if right hand only returned value is str. if both hands it will be tuple.
    2 updated_last_trigger_time
    """

    hands = extract_hand_gestures(result)

    right = hands["right"]
    left = hands["left"]

    # No right hand detected, no action will be executed
    if not right:
        return None, last_trigger_time

    now = time.time()

    r_name, r_score = right
    buffer.append(r_name)

    # classifiy detected gesture as stable.
    # avoid rapid execution.
    # A gesture must appear at least 4 times,
    # and score more than N% confidence level.
    # And waiting time must be at least -0.n secs.
    stable = (
        buffer.count(r_name) >= 4
        and r_score > 0.70 # 70 to 80 is good, more is strict, less is messy.
        and now - last_trigger_time >= cooldown_sec
    )
    
    if not stable:
        return None, last_trigger_time

    # if left hand is detected and stable.
    # use it with the right hand to create combination.
    if left:
        l_name, _ = left
        return (l_name, r_name), now

    # right hand gesture
    return r_name, now


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

            # draw a circle (point) for each landmark.
            cv.circle(frame, (x,y), 4, (0, 255, 0), -1)
        
        # draw lines between points 
        for start, end in HAND_CONNECTIONS:
            cv.line(frame, points[start], points[end], (255, 0, 0), 2)


