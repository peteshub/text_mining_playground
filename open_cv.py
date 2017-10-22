import cv2
import pytesseract
import tesserocr
from PIL import Image

img = cv2.imread('BMW_GB16_en_Finanzbericht30.jpg',cv2.IMREAD_GRAYSCALE)
img_blurred = cv2.blur(img,(35,35))

#img_blurred = cv2.GaussianBlur(img,(21,21),0)
cv2.imshow('test',img_blurred)
cv2.waitKey(0)


ret, mask = cv2.threshold(img_blurred, 254,255, cv2.THRESH_BINARY)
cv2.imshow('test',mask)
cv2.waitKey(0)

#cv2.destroyAllWindows()

img2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#cont = cv2.drawContours(img, contours, -1, (0,255,0), 3)

#cv2.imshow('test',cont)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

for i,c in enumerate(contours):
    x, y, w, h = cv2.boundingRect(c)
    #cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
    str = pytesseract.image_to_string(Image.fromarray(img[y:y + h, x:x + w]))
    print("\nCountour Nr. {}: \n {}".format(i,str))
    cv2.imshow('Features', img[y:y+h,x:x+w])
    cv2.waitKey(0)
    cv2.destroyAllWindows()


