"""
Here is where you can fine-tune the model.
All you need to do is provide the path of your dataset.

NOTE: This model is trained only for one hand.

Things you need to know IMPORTANT:
1 the dataset dir must include "none" dir and this dir must
include samples that are not gestures, so your model does not hallucinate.

2 if your pc/laptop is not capable enough use google Colab.

3 dir names will be used as labels, so name them carefully. 
    label is the "name of gesture"

4 The python version used for training is 3.10.13
if your system has a newer version, or even an older. It's recommended 
to use pyenv and install this version, to avoid compatibility issues.

5 the only lib you need to install is "mediapipe_model_maker"
it will download, all necessary libs/framworks (size is decent) 
version used for this project is 0.2.1.4.  

Check Notes.txt for more info.
"""


import os
import tensorflow as tf
assert tf.__version__.startswith('2')
from mediapipe_model_maker import gesture_recognizer

import matplotlib.pyplot as plt

# Assuming the dataset dir is inside the same PRJ dir.
dataset_path = "gs_dataset"


""" Uncomment if you want to see labels"""
# print(dataset_path)
# labels = []
# for i in os.listdir(dataset_path):
#   if os.path.isdir(os.path.join(dataset_path, i)):
#     labels.append(i)
# print(labels)
#

"""Ucomment if you want to see examples of images"""
# NUM_EXAMPLES = 5
#
# for label in labels:
#   label_dir = os.path.join(dataset_path, label)
#   example_filenames = os.listdir(label_dir)[:NUM_EXAMPLES]
#   fig, axs = plt.subplots(1, NUM_EXAMPLES, figsize=(10,2))
#   for i in range(NUM_EXAMPLES):
#     axs[i].imshow(plt.imread(os.path.join(label_dir, example_filenames[i])))
#     axs[i].get_xaxis().set_visible(False)
#     axs[i].get_yaxis().set_visible(False)
#   fig.suptitle(f'Showing {NUM_EXAMPLES} examples for {label}')
#
# plt.show()


# loading the dataset  
data = gesture_recognizer.Dataset.from_folder(
    dirname=dataset_path,
    hparams=gesture_recognizer.HandDataPreprocessingParams(),
)

# Splitting the dataset
# train 80% of the data
train_data, rest_data = data.split(0.8)
# Split the remaining 20%. 50%/50%. 10% validation/ 10% test
validation_data, test_data = rest_data.split(0.5)

# training (training rules.)
# Note: search more about this.
hparams = gesture_recognizer.HParams(
    batch_size=8, # number of samples model looks at before update.
    epochs=25, # how many times to pass the entire dataset to model.
    export_dir="exported_model" # where to save the trained model 
)

# 4. Model options
model_options = gesture_recognizer.ModelOptions(

    # drop 10% of neurons per batch to prevent overfitting.
    # "overfitting" means model be so good at data trained on
    # ,but weak when it comes to unseen data.
    # by dropping 10% you encourage the model to have a general rule.
    dropout_rate=0.1
)

# Combinn model options and training hyperparameters
# in one var so it will be easier to pass it later.
options = gesture_recognizer.GestureRecognizerOptions(
model_options=model_options,
hparams=hparams
)

# create and train the model.
model = gesture_recognizer.GestureRecognizer.create(
    train_data=train_data,
    validation_data=validation_data,
    options=options
)

# Evaluate the model. a test to see its performance.
# Loss: how wrong the model is.
# Accuracy: N% of correct prediction.
loss, acc = model.evaluate(test_data, batch_size=1)
print(f"Test loss:{loss}, Test accuracy:{acc}")

# save the trained mode on the system to use it later.
model.export_model()


