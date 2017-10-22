import pytesseract
import tesserocr
from PIL import Image

print(tesserocr.tesseract_version())  # print tesseract-ocr version
#print(tesserocr.get_languages()) # prints tessdata path and list of available languages


str = pytesseract.image_to_string(Image.open('BMW_GB16_en_Finanzbericht9.jpg'),lang='eng')

print(str)
#print(str.split('\n'))

#print(pytesseract.image_to_string(Image.open('test-european.jpg'), lang='fra'))