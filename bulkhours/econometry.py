import matplotlib as mpl
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import collections
import random
import sys


def init_env(ip):
    """Use pip from the current kernel"""
    import tensorflow as tf

    runrealcmd("apt-get install -y xvfb python-opengl", verbose=True)
    runrealcmd("pip install gymnasium pyvirtualdisplay array2gif", verbose=True)
    runrealcmd("pip install gymnasium[atari,toy_text,box2d,classic_control,accept-rom-license]", verbose=True)

    if not tf.config.list_physical_devices("GPU"):
        print("No GPU was detected. Neural nets can be very slow without a GPU.")
        if "google.colab" in sys.modules:
            print("Go to Runtime > Change runtime and select a GPU hardware accelerator.")
        if "kaggle_secrets" in sys.modules:
            print("Go to Settings > Accelerator and select GPU.")

    plt.rc("font", size=14)
    plt.rc("axes", labelsize=14, titlesize=14)
    plt.rc("legend", fontsize=14)
    plt.rc("xtick", labelsize=10)
    plt.rc("ytick", labelsize=10)
    plt.rc("animation", html="jshtml")


def plot_environment(env, figsize=(5, 4)):
    plt.figure(figsize=figsize)
    img = env.render()
    if type(img) == list:
        img = img[0]
    plt.imshow(img)
    plt.axis("off")
    plt.show()
    return img
