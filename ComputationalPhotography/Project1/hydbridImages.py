import cv2

import numpy as np
from matplotlib.colors import LogNorm
from scipy import signal
import matplotlib.pyplot as plt

import utils

print("Hybrid Images.. go go")

im1_file = './Nutmeg.jpg'
im2_file = './DerekPicture.jpg'

im1 = cv2.imread(im1_file, cv2.IMREAD_GRAYSCALE)
im2 = cv2.imread(im2_file, cv2.IMREAD_GRAYSCALE)

pts_im1 = utils.prompt_eye_selection(im1)

utils.endofProgram()