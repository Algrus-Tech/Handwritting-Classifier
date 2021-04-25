import os
from flask import Flask, request
import cv2
import numpy as np
from mylib.TesseractPython import tesseract_class
from spellchecker import SpellChecker
from textblob import TextBlob

spell = SpellChecker()

app = Flask(__name__)

UPLOAD_FOLDER = f'{os.getcwd()}/UPLOAD_FOLDER'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/predict', methods=['POST'])
def predict():
    data = request.files
    imageContrast = 400
    if request.form['imageContrast']:
        imageContrast = request.form['imageContrast']
   

    print(imageContrast)
    if not data:
        return {
            'success': False,
            'data': None
        }
    else:
        file = request.files['file']
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        final_res = preprocess_image(f'UPLOAD_FOLDER/{filename}',filename,imageContrast)
        print('image preprocessed')
        
        return {
            'success': True,
            'data': final_res
        }


def preprocess_image(path,filename,imageContrast):
    
    ext = filename.split(".")[1]
    print(ext)
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    if img.shape[1]>1500 or img.shape[0]>1500:
        return 'image size is too big'
    

    print(f'before resize: {img.shape}')
    pxmin = np.min(img)
    pxmax = np.max(img)
    imgContrast = (img - pxmin) / (pxmax - pxmin) * int(imageContrast)
    kernel = np.ones((3, 3), np.uint8)
    imgMorph = cv2.erode(imgContrast, kernel, iterations = 1)
    cv2.imwrite(f'data/processed image.{ext}', imgMorph)

    output = tesseract_class.extract_ocr(f'data/processed image.{ext}')
    print(output)
    words = output.split(" ")
    for i in range(len(words)):
        if "\n" in words[i]:
            words[i] = words[i].replace("\n"," ")
        if 'x0c' in words[i]:
            words[i] = ""



    new_output = " ".join(words).split(" ")

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


    return [output,form_op,form_op_2]

if __name__ == '__main__':
    app.run()