import subprocess

"""
The logic behind the cursor movement,
needs some knowledge and search in physics of motion.
"""


gesture_hold_frames = 0
last_gesture = None


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# velocity (speed and direction) of the cursor 
VEL_X = 0.0
VEL_Y = 0.0


# how fast the cursor slows down when no force is applied
# in simple words, this controls how smooth the cursor slows down.
FRICTION = 0.82 # velocity reduced by 18% each frame

# how much force the gesture applies to push the cursor each frame. 
ACCEL_FORCE = 18.4      

# top speed of the cursor 
MAX_VEL = 45.0

# store the current position of the cursor on the screen.
# default position middle of the screen.
CURSOR_X = 960  
CURSOR_Y = 540

# Base movement step for gestures (before acceleration)
MOUSE_SPEED = 2       


# Gesture to direction mapping
MOUSE_MOVES = {
    "one":    (0, -MOUSE_SPEED),  # up
    "two_up": (0, MOUSE_SPEED),   # down
    "three":  (-MOUSE_SPEED, 0),  # left
    "four":   (MOUSE_SPEED, 0),   # right

    # diagonals
    "stop": ( MOUSE_SPEED, -MOUSE_SPEED), # right up
    "stop_inverted": (-MOUSE_SPEED, -MOUSE_SPEED), # left up
    "dislike":( MOUSE_SPEED, MOUSE_SPEED), # right down
    "like": (-MOUSE_SPEED, MOUSE_SPEED), # left down
}



def mouse_move_accelerated(gesture):

    global VEL_X, VEL_Y, gesture_hold_frames, last_gesture, last_move_time



    # Reset ramp if gesture changes
    if gesture != last_gesture:
        gesture_hold_frames = 0
        last_gesture = gesture

    gesture_hold_frames += 1

    dx, dy = MOUSE_MOVES[gesture]

    # Normalize direction
    length = (dx**2 + dy**2) ** 0.5
    if length == 0:
        return

    ndx = dx / length
    ndy = dy / length

    # --- Acceleration ramp (IMPORTANT PART) ---
    # Starts small, ramps smoothly, caps naturally
    ramp = min(1.0, gesture_hold_frames / 6.0)
    ramp = ramp * ramp   # ease-in curve

    force = ACCEL_FORCE * ramp

    # Apply force
    VEL_X += ndx * force
    VEL_Y += ndy * force

    # Clamp velocity
    VEL_X = max(-MAX_VEL, min(MAX_VEL, VEL_X))
    VEL_Y = max(-MAX_VEL, min(MAX_VEL, VEL_Y))





def update_mouse_physics():
    global CURSOR_X, CURSOR_Y, VEL_X, VEL_Y

    # Apply velocity
    CURSOR_X += VEL_X
    CURSOR_Y += VEL_Y

    # Apply friction (smooth stop)
    VEL_X *= FRICTION
    VEL_Y *= FRICTION

    # Kill tiny jitter
    if abs(VEL_X) < 0.01: VEL_X = 0
    if abs(VEL_Y) < 0.01: VEL_Y = 0

    # Clamp to screen
    CURSOR_X = max(0, min(SCREEN_WIDTH, CURSOR_X))
    CURSOR_Y = max(0, min(SCREEN_HEIGHT, CURSOR_Y))

    subprocess.run(
        ["hyprctl", "dispatch", "movecursor",
         str(int(CURSOR_X)), str(int(CURSOR_Y))],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )





def click_mouse(button: str):
    """
    Simulate mouse Left, Right and Middle.
    Receive command based on the gesture, then
    send it to dotool to execute it.
    """
    subprocess.run(
        ["dotool"],
        input=f"click {button}\n",
        text=True,
        check=False
    )

def scroll_mouse(speed: int):
    """
    Simulate mouse wheel to scroll up or down.
    Receive command based on the gesture, then
    send it to dotool to execute it.
    
    Positive speed = scroll up.
    Negative speed = scroll down.
    """
    subprocess.run(
        ["dotool"],input=f"wheel {speed}\n",text=True,check=False)
           


def double_click_left_mouse():
    """
    Simulate mouse double click left.
    Receive command based on the gesture, then
    send it to dotool to execute it.
    """
    subprocess.run(
        ["dotool"],
        input=(
            "buttondown left\n"
            "buttonup left\n"
            "buttondown left\n"
            "buttonup left\n"
        ),
        text=True,
        check=False
    )







