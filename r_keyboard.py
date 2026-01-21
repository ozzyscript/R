import subprocess


CAPSLOCK_ACTIVE = False

def type_char(char):
    """
    send the given char to "dotool" to type it on the system
    Ex: terminal, text editor...etc
    if Capslock active, type char in capital case.
    """

    # modify/get status of the global
    # var instead of creating local one.
    global CAPSLOCK_ACTIVE 
    
    # if the global var is True(ON/Active)
    if CAPSLOCK_ACTIVE and char.isalpha():
        char = char.upper()
    subprocess.run(["dotool"], input=f"type {char}\n", text=True)


def press_func_key(key_name):
    """
    send function key to "dotool" to simulate keyboard key
    example of keys: Ctrl, Alt, Tab...
    """
    subprocess.run(["dotool"], input=f"key {key_name}\n", text=True)


def toggle_capslock():
    """
    Activate/Deactivate CapsLock 
    """
    global CAPSLOCK_ACTIVE
    CAPSLOCK_ACTIVE = not CAPSLOCK_ACTIVE
    print("CAPSLOCK:", "ON" if CAPSLOCK_ACTIVE else "OFF")


