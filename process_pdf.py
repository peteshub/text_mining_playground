import cv2
import numpy as np
import pytesseract
import tesserocr
from PIL import Image
import tabula
from matplotlib import pyplot as plt
import os
from PyPDF2 import PdfFileReader

report = './tmp/report.pdf'

img_path = './tmp/report{}.jpg'

os.system('java -jar ./lib/pdfbox-app-2.0.7.jar PDFToImage {} -dpi 100'.format(report))

pdf = PdfFileReader(report)
num_pages = pdf.getNumPages()

dims = list(pdf.getPage(0).mediaBox)

print(num_pages)

for i in range(num_pages):
    img = cv2.imread(img_path.format(i+1), cv2.IMREAD_GRAYSCALE)
    img_size = img.shape
    target_y = 1024
    target_x = int(img_size[0] * target_y / img_size[1])
    img = cv2.resize(img, (target_y, target_x), Image.ANTIALIAS)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    img_blurred = cv2.blur(img, (11, 25))

    kernel = np.ones((5, 5), np.uint8)

    img_blurred = cv2.dilate(img_blurred,kernel,iterations=2)

    ret, mask = cv2.threshold(img_blurred, 253, 255, cv2.THRESH_BINARY)

    img2, contours, hierarchy = cv2.findContours(255 - mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)

    #cont = cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
    #cv2.imshow('test', cont)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    areas = ""

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        scale_x = dims[3] / target_x
        scale_y = dims[2] / target_y

        box = [y * scale_y-5, x * scale_x-5, (y + h) * scale_y+5, (x + w) * scale_x+5]
        area = [x * scale_x-5,y * scale_y-5,w * scale_x+5,h * scale_y+5]


        df = tabula.read_pdf('./tmp/report.pdf', guess=False, pages=i+1, area=box)
	#test if it is a table (i.e. when columns>1)
        if df is None or len(df.columns)<=1:
            areas += ",".join([str(int(a)) for a in area]) + ";"
        else:
            print(df)
            #cv2.imshow('Features', img[y:y + h, x:x + w])
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()

    #extract paragraphs
    os.system('java -jar ./lib/ExtractParagraphsByArea_v0.1.jar {} {} "{}"'.format(report,i,areas))
