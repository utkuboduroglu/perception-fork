import cv2 as cv
import numpy as np

src = cv.imread(r'C:\Users\ereni\Desktop\deneme.png')

s = 416

def resize2Square(img, size, interpolation):
  h, w = img.shape[:2]
  c = None if len(img.shape) < 3 else img.shape[2]
  if h == w: return cv.resize(img, (size, size), interpolation)
  if h > w: dif = h
  else:     dif = w
  x_pos = int((dif - w)/2.)
  y_pos = int((dif - h)/2.)
  if c is None:
    mask = np.zeros((dif, dif), dtype=img.dtype)
    mask[y_pos:y_pos+h, x_pos:x_pos+w] = img[:h, :w]
  else:
    mask = np.zeros((dif, dif, c), dtype=img.dtype)
    mask[y_pos:y_pos+h, x_pos:x_pos+w, :] = img[:h, :w, :]
  return cv.resize(mask, (size, size), interpolation)

resized = resize2Square(src, s, cv.INTER_AREA)

#CLAHE (Contrast Limited Adaptive Histogram Equalization)
clahe = cv.createCLAHE(clipLimit=1., tileGridSize=(8,8))

lab = cv.cvtColor(resized, cv.COLOR_BGR2LAB) 
l, a, b = cv.split(lab)

l2 = clahe.apply(l)

lab = cv.merge((l2,a,b)) 
final = cv.cvtColor(lab, cv.COLOR_LAB2BGR) 

#denoising
den = cv.fastNlMeansDenoisingColored(final, None, 4, 4, 7, 21)

#standardization
imgg = den.astype('float32')
std = (imgg - imgg.mean(axis=(0, 1, 2), keepdims=True)) / imgg.std(axis=(0, 1, 2), keepdims=True)

#normalization
norm = (std - np.min(std)) / (np.max(std) - np.min(std))

cv.imshow('source', src)
cv.imshow('norm', norm)
cv.waitKey(0)
cv.destroyAllWindows()
