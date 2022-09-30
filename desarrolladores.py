import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Archivos de programa\Tesseract-OCR\tesseract'
from pytesseract import Output
from matplotlib import pyplot as plt
import re
from pdf2image import convert_from_path
import time
from PIL import Image 
from PIL import ImageDraw 
from PIL import ImageFont 
from datetime import datetime, timezone
import datetime
from PIL import Image 
# Parte de covertir 1 pdf a imagen 




#Parte de coordenadas para la correcta firma
path_Example= 'last_page.png'
img_color = cv2.imread(path_Example)
plt.imshow(img_color)
##plt.show()
img_gris = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
plt.imshow(img_gris)
##plt.show()
thresh_img = cv2.threshold(img_gris, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
plt.imshow(thresh_img)
##plt.show()
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,2))
opening_image = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, kernel,iterations=1)
plt.imshow(opening_image)
##plt.show()
invert_image = 255 - opening_image

def ocr(image):
    custom_config = r'-l spa - psm 11'
    text = pytesseract.image_to_string(image,config=custom_config )
    return text
data_image= pytesseract.image_to_data(invert_image, output_type=Output.DICT)

n_boxes = len(data_image['text'])
for i in range(n_boxes):
  if int(data_image['conf'][i]) > 50:
    (x, y, w, h) = (data_image['left'][i], data_image['top'][i],data_image['width'][i], data_image['height'][i])
    img = cv2.rectangle(img_color, (x, y),(x + w, y + h),(255,0,0), 2)

cv2.imwrite('ImagenRectangulos.jpg',img)

##Encontrar el Bloque al que pertenece la palabra deseada
a='MAURICIO'
bloque=0
i=0
total=n_boxes
while (i<total-1):
  bloque=bloque+1
  i=i+1
  if(data_image['text'][i].casefold()==a.casefold()):
    newdata=[0,0]
    newdata=[data_image['left'][bloque],data_image['top'][bloque]]
print(newdata)
newx=newdata[0]
newy=newdata[1]

filepath = "signature.png"
img = Image.open(filepath) 
  
width = img.width 
height = img.height +3
  
print("The height of the image is: ", height) 
print("The width of the image is: ", width) 


td =time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
img = Image.open('signature.png') 
I1 = ImageDraw.Draw(img) 
I1.text((0, 0), td , fill =(255, 0, 0)) 
img.show() 
img.save("signature.png") 

Image1 = Image.open('last_page.png') 
Image1copy = Image1.copy() 
Image2 = Image.open('signature.png') 
Image2copy = Image2.copy() 
Image1copy.paste(Image2copy,(newx, newy-height)) 
Image1copy.save('pasted2.png')

pdf = pytesseract.image_to_pdf_or_hocr('pasted2.png', extension='pdf')
with open('Doc_firmado.pdf', 'w+b') as f:
    f.write(pdf) # pdf type is bytes by default
