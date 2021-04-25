import cv2, os, argparse
import numpy as np
from mylib import Config
from mylib.TesseractPython import tesseract_class
from mylib.LogData import logger_class
# from mylib.SpellChecker import correct_sentence
from mylib.Pre import preproc
from spellchecker import SpellChecker
from textblob import TextBlob
import enchant

dict_words = enchant.Dict("en_US")

spell = SpellChecker()

img = cv2.imread('tests/new_test_3.png', cv2.IMREAD_GRAYSCALE)
# img = cv2.resize(img,(1800,1000))
print(img.shape)
# increase contrast and reduce the background noise
pxmin = np.min(img)
pxmax = np.max(img)
# optimise the pixel values (255, 300, 350 etc) and check the output
# 400 value gave a better output on noisy 'handwritten.png' along with the thickness 1
# (iterations = 1), when tested seperately
imgContrast = (img - pxmin) / (pxmax - pxmin) * 400

# increase the text line width or thickness
kernel = np.ones((3, 3), np.uint8)
imgMorph = cv2.erode(imgContrast, kernel, iterations = 1)

# save the img
cv2.imwrite('data/processed image.png', imgMorph)

output = tesseract_class.extract_ocr('data/processed image.png')
print(output)

words = output.split(" ")

for i in range(len(words)):
    if "\n" in words[i]:
        words[i] = words[i].replace("\n"," ")
    if 'x0c' in words[i]:
        words[i] = ""



new_output = " ".join(words).split(" ")

# print(output.split(" "))


print(new_output)

print_this_1 = []
print_this_2 = []

for a in new_output:
    b = TextBlob(a.lower())
    print_this_1.append(str(b.correct()))
    print_this_2.append(spell.correction(a.lower()))
    # print(str(b.correct()))
    # print(spell.correction(a.lower()))

form_op = " ".join(print_this_1)
print(form_op)
form_op_2 = " ".join(print_this_2)
print(form_op_2)

# for word in new_output:
#     print("Suggestion for " + word + " : " + str(dict_words.suggest(word.lower())))