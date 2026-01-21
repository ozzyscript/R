
# Recognizer (R)

R is a simple program that tries to simulate Keyboard and Mouse input
using only hand gestures.

Note: this is the V2 of the project. I worked on V1 finished it and wrote the README file,
then the keyboard and mouse idea appeared, so I made great amount of change to the code base.

Worth mentioning :)
This is my first project in computer vision field.
The reason I created this program is that my mind kept telling me 
"we need to build something with that camera in computer vision field".

---

## What can you do with R so far

### Keyboard
- Type all alphabit A-Z/a-z capital and small 
- Type all number 0-9
- Type all punctuation 
- Type all char that programmer needs
- Simulate SHIFT, CTRL and SUPER(wind) keys
- Simulate arrow keys, enter, backspace, tab and esc

### Mouse
- Move cursor up, down , left and right
- Move cursor diagonally in 4 directions
- Simulate left , right and middle click (wheel)
- Simulate double click left
- Simulate wheel scrolling up/down

### Other things
- Control media
- Open app menu / close an app
- Resize window 
- toggle fullscreen

---

## How R works
receive a gesture from camera input using `opencv` recognize it via
`mediapipe gesture recognizer model`. Once it is recognized and stable 
the system execute it based on the action mapping system.
In may case I used `dotool` and `hyprland`.

Below is a high level over view.

Basically there are two modes:

### Right hand mode
this mode can perform up to 18 gestures

### Left + Right hand mode
this mode can perform +300 combo gestures.

Each left gesture is combined with 18 right hand gestures. 

Example:
`fist` gesture is used as "Mouse mode"
- `fist + fist` = double click left mouse button
- `fist + three2` = click right mouse button 

`stop` and `stop_inverted` are used for typing letters and symbols 
- `stop + ok` = type letter `c`
- `stop_inverted + rock` types letter `z`

In simple words: Left hand works as Mode/Modifier and right hand triggers the action

Note:
see `docs` dir(folder) for more details.
see `consts.py` file to adjust actions and their mapping.

---

## Grouping System
The idea here that each left hand gesture is assigned to a group of actions.

- `stop` and `stop_inverted` group used to type keyboard letters + "space", "." and "?".
- `peace` and `peace_inverted` group used to type keyboard chars/symbols.
- `like` grope used to simulate CTRL key.
- `two_up` group used to simulate SHIFT key.
- `ok` group used to simulate main keyboard key such "enter", "backspace", "arrow keys".
- `palm` group used to simulate SUPER/WIND key
- `fist` group used to simulate mouse keys and cursor movement.

---

## Default vs Custom Gestures
I fine-tuned the MediaPipe model to go beyond the default gestures.

The number of the default gestures were (7).
The custom (fine-tuned) gestures are (18).

---

## Installation and Use

Note: make sure to create a virtual env first.

- clone via 
```bash
git clone https://github.com/ozzyscript/R.git
```
- install `mediapipe` via. This version uses the new APIs
```bash
pip install mediapipe==0.10.31
```
I used it with python 3.13.10. you can install it with `pyenv` as
a separate python version. See `docs/version.txt`:
 

### Important Notes

- 1) Old VS New mediapip APIs (version)
Most tutorials and docs online use older version.
make sure to use the version that is compatable with your py version.

- 2) This project is devided into two parts. See `docs/version.txt`:
    - main where you run the program using `main.py` (uses the new APIs).
    - Training where the `train.py` (uses the old APIs) is used to train the model locally. 

- 3) Each part must be inside its own virtual env.
- 4) Use pyenv to install different versions of python.

---

# Training 

- create a separate virtual env.
- install `mediapipe-model-maker` via. This version uses the old APIs
```bash
pip install mediapipe-model-maker==0.2.1.4
```
### Dateset
- get dataset from (thanks to contributors)
https://www.kaggle.com/datasets/innominate817/hagrid-sample-30k-384p/data

note: 
- You only need the directory that contains subfolders with images
- Each subfolder name becomes a gesture label
- Folder name = gesture name

The dataset does not include a no_gesture "none" class.
Without it, the model tends to hallucinate gestures.
To fix this:

```bash
python3 download.py -d -t no_gesture
```
Then:
1. Rename the folder to none
2. Add it to the dataset
3. Remove hidden files or directories

I get the file from (thanks to them):
https://github.com/hukenovs/hagrid/blob/master/download.py


### Training Notes

- train.py is ready to use
- Dataset path is local (adjust as needed)
- Use Google Colab if hardware is limited

---

Note: message for you
- around 8 out of 18 groups are used, still too much to add if you want.
- code can be improved a lot more than as is.
- you can fine-tune the model to add more gestures.
- you can adjust it to suit someone can't used fingers for somewhat reason.
- the best you can do is to adjust it for someone "handless",
it will be good especially if combined with voice input system.



