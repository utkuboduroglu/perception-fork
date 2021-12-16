import cv2 as cv
import numpy as np

img = cv.imread(r'C:\Users\ereni\Desktop\deneme4.png')

img = cv.resize(img, (300, 300), interpolation = cv.INTER_AREA)

#denoising
den = cv.fastNlMeansDenoisingColored(img, None, 5, 5, 7, 21)

#standardization
imgg = den.astype('float32')
std = (imgg - imgg.mean(axis=(0, 1, 2), keepdims=True)) / imgg.std(axis=(0, 1, 2), keepdims=True)

#normalization
norm = (std - np.min(std)) / (np.max(std) - np.min(std))

cv.imshow('source', img)
cv.imshow('denoised', den)
cv.imshow('standardization', std)
cv.imshow('normalization', norm)
cv.waitKey(0)
