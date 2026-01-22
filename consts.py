import subprocess
from r_keyboard import type_char, press_func_key,toggle_capslock
from mouse import click_mouse, scroll_mouse, double_click_left_mouse
from helper import hypr



"""
Right hand only.
Execute command once the gesture is detected.
"""

GESTURE_COMMANDS = {

                # """ All gestures """
#     "palm[x]", "ok", "fist[x]", "one[x]", "two_up[x]", "three[x]", "three2[x]", 
#     "four[x]", "like", "mute[x]", "rock", "call[x]", "dislike[x]", "peace[x]", 
#     "inverted[x]", "stop[x]", "stop_inverted[x]", "two_up_inverted[x]"



    #  >>>>>>>> { main system/hyprland control } <<<<<<<<<<<<
    
    # press escape button
    "fist": lambda: press_func_key("esc"),
    

    # move window focus (right/left)
    "three2": lambda: hypr("movefocus", "r"),

    # resize window left 
    "stop_inverted": lambda: hypr("resizeactive", "-20","0"),
    # resize window right 
    "two_up_inverted": lambda: hypr("resizeactive", "20","0"),
    

    # Close the current active window
    "dislike":  lambda: press_func_key("SUPER+q"),

    # toggle fullscreen 
    "palm": lambda: hypr("fullscreen"),

    # App menu wofi 
    "call": lambda: subprocess.Popen(
    ["wofi"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
    ),


    #  >>>>>>>> { media control } <<<<<<<<<<<<

    # play/pause
    "stop": lambda: subprocess.run(
        ["playerctl", "play-pause"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ),

    # Volume up
    "one": lambda: subprocess.run(
        ["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", "10%+"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ),

    # Volume down
    "two_up": lambda: subprocess.run(
        ["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", "10%-"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ),

    # Mute
    "mute": lambda: subprocess.run(
    ["wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "toggle"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
    ),

    # next track
    "peace": lambda: subprocess.run(
    ["playerctl", "next"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
),
    
    # previous track
    "inverted": lambda: subprocess.run(
    ["playerctl", "previous"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
),
    
    # skip forward
    "three": lambda: subprocess.run(
    ["playerctl", "position", "10+"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
),

    # skip backward
    "four": lambda: subprocess.run(
    ["playerctl", "position", "10-"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
),

}



"""
Combo: Left + Right.
Where left hand works as Mode/Modifier, 
and Right hand executes the action.
"""
COMBO_COMMANDS = {
    
                # """ All gestures """
#     "palm[x]", "ok[x]", "fist[x]", "one", "two_up", "three", "three2", 
#     "four", "like[x]", "mute", "rock", "call", "dislike", "peace[x]", 
#     "inverted[x]", "stop", "stop_inverted[x]", "two_up_inverted"


    
    #  >>>>>>>>>>>> { Keyboard } <<<<<<<<<<<<<

    # STOP group (letters a–o)

    ("stop", "palm"):   lambda: type_char("a"),
    ("stop", "fist"):   lambda: type_char("b"),
    ("stop", "ok"):     lambda: type_char("c"),
    ("stop", "one"):    lambda: type_char("d"),
    ("stop", "two_up"): lambda: type_char("e"),
    ("stop", "peace"):  lambda: type_char("f"),
    ("stop", "like"):   lambda: type_char("g"),
    ("stop", "four"):   lambda: type_char("h"),
    ("stop", "three"):  lambda: type_char("i"),
    ("stop", "three2"): lambda: type_char("j"),
    ("stop", "rock"):   lambda: type_char("k"),
    ("stop", "call"):   lambda: type_char("l"),
    ("stop", "mute"):   lambda: type_char("m"),
    ("stop", "dislike"):lambda: type_char("n"),
    ("stop", "two_up_inverted"): lambda: type_char("o"),


    # STOP_INVERTED group (letters p–z + space, . ?)

    ("stop_inverted", "palm"):  lambda: type_char("p"),
    ("stop_inverted", "fist"):  lambda: type_char("q"),
    ("stop_inverted", "ok"):    lambda: type_char("r"),
    ("stop_inverted", "one"):   lambda: type_char("s"),
    ("stop_inverted", "two_up"):lambda: type_char("t"),
    ("stop_inverted", "peace"): lambda: type_char("u"),
    ("stop_inverted", "like"):  lambda: type_char("v"),
    ("stop_inverted", "four"):  lambda: type_char("w"),
    ("stop_inverted", "three"): lambda: type_char("x"),
    ("stop_inverted", "three2"):lambda: type_char("y"),
    ("stop_inverted", "rock"):  lambda: type_char("z"),
    ("stop_inverted", "call"):  lambda: type_char(" "),
    ("stop_inverted", "mute"):  lambda: type_char("."),
    ("stop_inverted", "dislike"):lambda: type_char("?"),

    
   # PEACE group (numbers 1–9 + 0 + special chars)

    ("peace", "palm"):           lambda: type_char("1"),
    ("peace", "fist"):           lambda: type_char("2"),
    ("peace", "ok"):             lambda: type_char("3"),
    ("peace", "one"):            lambda: type_char("4"),
    ("peace", "two_up"):         lambda: type_char("5"),
    ("peace", "peace"):          lambda: type_char("6"),
    ("peace", "like"):           lambda: type_char("7"),
    ("peace", "four"):           lambda: type_char("8"),
    ("peace", "three"):          lambda: type_char("9"),
    ("peace", "three2"):         lambda: type_char("0"),
    ("peace", "rock"):           lambda: type_char("@"),
    ("peace", "call"):           lambda: type_char("#"),
    ("peace", "mute"):           lambda: type_char("%"),
    ("peace", "dislike"):        lambda: type_char("&"),
    ("peace", "stop"):           lambda: type_char('"'),
    ("peace", "stop_inverted"):  lambda: type_char("'"),


    # PEACE_INVERTED group (special characters for programming)

    ("inverted", "palm"):           lambda: type_char("("),
    ("inverted", "fist"):           lambda: type_char(")"),
    ("inverted", "ok"):             lambda: type_char("{"),
    ("inverted", "one"):            lambda: type_char("}"),
    ("inverted", "two_up"):         lambda: type_char("["),
    ("inverted", "peace"):          lambda: type_char("]"),
    ("inverted", "like"):           lambda: type_char(";"),
    ("inverted", "four"):           lambda: type_char(":"),
    ("inverted", "three"):          lambda: type_char(","),
    ("inverted", "three2"):         lambda: type_char("!"),
    ("inverted", "rock"):           lambda: type_char("+"),
    ("inverted", "call"):           lambda: type_char("-"),
    ("inverted", "mute"):           lambda: type_char("*"),
    ("inverted", "dislike"):        lambda: type_char("/"),
    ("inverted", "stop"):           lambda: type_char("="),
    ("inverted", "stop_inverted"):  lambda: type_char("<"),
    ("inverted", "two_up_inverted"):lambda: type_char(">"),
    

    # >>>>>>>>>> Function keys 

    # LIKE group (CTRL)
    ("like", "like"): toggle_capslock, #Capital/small letters
    ("like", "palm"): lambda: press_func_key("CTRL+a"), # select all
    ("like", "fist"): lambda: press_func_key("CTRL+c"), # copy
    ("like", "ok"):   lambda: press_func_key("CTRL+v"), #paste
    ("like", "one"):  lambda: press_func_key("CTRL+SHIFT+c"), # copy terminal Linux
    ("like", "two_up"): lambda: press_func_key("CTRL+SHIFT+v"), #paste terminal Linux
    ("like", "stop"): lambda: press_func_key("CTRL+z"), # Undo
    ("like", "stop_inverted"): lambda: press_func_key("CTRL+SHIFT+z"), #Redo
     

    # TWO_UP group (SHIFT)
    ("two_up", "one"):       lambda: press_func_key("SHIFT+up"),
    ("two_up", "two_up"):    lambda: press_func_key("SHIFT+down"),
    ("two_up", "three"):     lambda: press_func_key("SHIFT+left"),
    ("two_up", "four"):    lambda: press_func_key("SHIFT+right"),
 
    
    # OK group (MAIN KEYS)
    ("ok", "ok"): lambda: press_func_key("enter"),
    ("ok", "palm"): lambda: press_func_key("backspace"),
    ("ok", "fist"): lambda: press_func_key("tab"),
    ("ok", "stop"): lambda: press_func_key("esc"),

    # Arrow keys
    ("ok", "one"):       lambda: press_func_key("up"),
    ("ok", "two_up"):    lambda: press_func_key("down"),
    ("ok", "three"):     lambda: press_func_key("left"),
    ("ok", "four"):    lambda: press_func_key("right"),
    
    

    # PALM group (SUPER/Window)
    ("palm", "one"):  lambda: press_func_key("SUPER+1"),
    ("palm", "two_up"):    lambda: press_func_key("SUPER+2"),
    ("palm", "three"):   lambda: press_func_key("SUPER+3"),
    ("palm", "four"):lambda: press_func_key("SUPER+4"),
    ("palm", "palm"): lambda: press_func_key("SUPER+5"),
    ("palm", "fist"):lambda: press_func_key("SUPER+6"),
    ("palm", "three2"):  lambda: press_func_key("SUPER+7"),
    ("palm", "like"):  lambda: press_func_key("SUPER+8"),

    

    #  >>>>>>>>>>>> { Mouse } <<<<<<<<<<<<<

    # FIST group

    # Clicks
    ("fist", "ok"):lambda: click_mouse("left"),
    ("fist", "three2"): lambda: click_mouse("right"),
    ("fist", "palm"):lambda: click_mouse("middle"),
    ("fist", "fist"):lambda:double_click_left_mouse(),

    # Cursor
    # Note: cursor move gestures are in mouse.py
    # below is their combo gestures 
    
    # Main 
    # ("fist", "one") =>  up
    # ("fist", "two_up") =>  down
    # ("fist", "three") =>  left
    # ("fist", "four") =>  right

    # diagonals
    # ("fist", "stop") =>  right up
    # ("stop_inverted") =>  left up
    # (fist", "dislike") => right down
    # ("fist", "like") => left down


    # Scroll
    ("fist", "peace"): lambda:  scroll_mouse(3), # scroll up
    ("fist", "inverted"):lambda: scroll_mouse(-3), # scroll down

    }




""" 
    Note: you can do auto key mapping using the code below.
    For me, it is not convenient because it lacks clarity.
"""
#
# RIGHT_HAND_GESTURES = [
#     "palm", "ok", "fist", "one", "two_up", "three", "three2", 
#     "four", "like", "mute", "rock", "call", "dislike", "peace", 
#     "peace_inverted", "stop", "stop_inverted", "two_up_inverted"
# ]
#
# # ====== Key groups ======
# STOP_KEYS = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o"]
# STOP_INV_KEYS = ["p","q","r","s","t","u","v","w","x","y","z","space",".","?"]
#
# # ====== Add STOP group letters ======
# for i, letter in enumerate(STOP_KEYS):
#     print(f"i: {i} | letter {letter}")
#     right_gesture = RIGHT_HAND_GESTURES[i]  # match gesture with letter
#     COMBO_COMMANDS[("stop", right_gesture)] = lambda l=letter: type_char(l)
#
# # ====== Add STOP_INVERTED group letters ======
# for i, letter in enumerate(STOP_INV_KEYS):
#
#     print(f"i: {i} | letter {letter}")
#     right_gesture = RIGHT_HAND_GESTURES[i % len(RIGHT_HAND_GESTURES)]  # wrap around if more letters than gestures
#     COMBO_COMMANDS[("stop_inverted", right_gesture)] = lambda l=letter: type_char(l)
