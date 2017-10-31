import cv2
import numpy as np
import pytesseract
import tesserocr
from PIL import Image
import tabula
from matplotlib import pyplot as plt

#img = cv2.imread('BMW_GB16_en_Finanzbericht26.jpg',cv2.IMREAD_GRAYSCALE)
#img = cv2.imread('../PDFkit/data/3_Kloeckner_IAS12.jpeg',cv2.IMREAD_GRAYSCALE)

page = 27

img = cv2.imread('./tmp/BMW_GB16_en_Finanzbericht{}.jpg'.format(page),cv2.IMREAD_GRAYSCALE)
img_size = img.shape
target_y = 1024
target_x = int(img_size[0]*target_y/img_size[1])


img = cv2.resize(img,(target_y,target_x),Image.ANTIALIAS)
#ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

thresh1 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

cv2.imshow('test',thresh1)
cv2.waitKey(0)
cv2.destroyAllWindows()

img = thresh1

img_blurred = cv2.blur(img,(17,27))



#img_blurred = cv2.dilate(img_blurred,kernel,iterations =5)

#img_blurred = cv2.GaussianBlur(img,(21,21),0)
cv2.imshow('test',img_blurred)
cv2.waitKey(0)
cv2.destroyAllWindows()

ret, mask = cv2.threshold(img_blurred, 253,255, cv2.THRESH_BINARY)
cv2.imshow('mask',mask)
cv2.waitKey(0)
cv2.destroyAllWindows()
dims = [0, 0, 637.795, 793.701]


img2, contours, hierarchy = cv2.findContours(255-mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)


#dilation = cv2.dilate(thresh, kernel, iterations=4)
#img2, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cont = cv2.drawContours(img, contours, -1, (0,255,0), 3)
cv2.imshow('test',cont)
cv2.waitKey(0)
cv2.destroyAllWindows()


for i,c in enumerate(contours):
    x, y, w, h = cv2.boundingRect(c)
    #cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    scale_x = dims[3]/target_x
    scale_y = dims[2]/target_y


    box = [ y*scale_y,x*scale_x, (y + h)*scale_y,(x + w)*scale_x]

    print(box)

    df = tabula.read_pdf('./tmp/report.pdf', guess=False, pages=page, area=box)

    if(len(df.columns)>1):
        print(df)

    #first_guess = tabula.read_pdf('/home/peter/Downloads/test_pdf/BMW_GB16_en_Finanzbericht.pdf',guess=True,pages=page,area=box)



    if df is not None:
        cv2.imshow('Features', img[y:y + h, x:x + w])
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        #plt.hist(img[y:y + h, x:x + w].ravel(), 3, [0, 256]); plt.show()
        #kernel = np.ones((5, 5), np.uint8)
        #portion = cv2.erode(img[y:y + h, x:x + w], kernel, iterations=3)
        #area = portion.shape[0]*portion.shape[1]

        #print(portion.mean())
        cv2.imshow('Features', img[y:y + h, x:x + w])
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    #str = pytesseract.image_to_string(Image.fromarray(img[y:y + h, x:x + w]))
    #print("\nCountour Nr. {}: \n {}".format(i,str))



