
import os
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Archivos de programa\Tesseract-OCR\tesseract'
from pytesseract import Output
from matplotlib import pyplot as plt
import re
from pdf2image import convert_from_path
import time 
from PIL import ImageDraw 
from PIL import ImageFont 
from datetime import datetime, timezone
import datetime
from PIL import Image   
import random
import shutil

aux=[]
aux2=[]
contenido = os.listdir('C:/Users/USUARIO/OneDrive/Escritorio/desarrolladores_claro/firma-pdf')
for i in contenido:
      if i.endswith('.pdf'):
            images = convert_from_path(i)
            for j in range(len(images)):
                
                images[j].save( i + str(j) +'.jpg')
                aux.append(( i + str(j) +'.jpg'))
                ultima_pag=(( i + str(j) +'.jpg'))
            aux2.append(ultima_pag)

print(aux)
for j in range(0,len(aux2)):

    path_Example = aux2[j]
    img_color = cv2.imread(path_Example)
    plt.imshow(img_color)
    

    img_gris = cv2.cvtColor(img_color, cv2.COLOR_RGB2GRAY)
    plt.imshow(img_gris)
    

    thresh_img = cv2.threshold(img_gris, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    plt.imshow(thresh_img)
   

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,2))
    opening_image = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, kernel,iterations=1)
    plt.imshow(opening_image)
  

    invert_image = 255 - opening_image
    plt.imshow(invert_image)


    def ocr(image):

        custom_config = r'-l spa - psm 11'
        text = pytesseract.image_to_string(image,config=custom_config )
        return text

    ##Convirtiendo la imagen a datos
    data_image= pytesseract.image_to_data(invert_image, output_type=Output.DICT)

    ##Generacion de bloques
    imrectangulos=[]
    n_boxes = len(data_image['text'])
    for i in range(n_boxes):
      if int(data_image['conf'][i]) > -1:
        (x, y, w, h) = (data_image['left'][i], data_image['top'][i],data_image['width'][i], data_image['height'][i])
        img = cv2.rectangle(img_color, (x, y),(x + w, y + h),(255,0,0), 2)
    cv2.imwrite('rectangulos.jpg',img)

    ##Encontrar el Bloque al que pertenece la palabra deseada
    a='Mauricio'
    b='Carlos'
    bloque=0
    i=0
    total=n_boxes
    while (i<total-1):
      bloque=bloque+1
      i=i+1
      if(data_image['text'][i].casefold()==a.casefold() or data_image['text'][i].casefold()==b.casefold() ):
        newdata=[0,0]
        newdata=[data_image['left'][bloque],data_image['top'][bloque]]
    print(newdata)
    newx=newdata[0]
    newy=newdata[1]

    ##Conociendo el tamaño de la firma  
    filepath = "signature.png"
    img = Image.open(filepath) 
    
    width = img.width 
    height = img.height +3
    
    print("The height of the image is: ", height) 
    print("The width of the image is: ", width) 

    ##Agregando fecha
  
    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    td =time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    img = Image.open('signature.png') 
    I1 = ImageDraw.Draw(img) 
    I1.text((0, 0), td , fill =(255, 0, 0)) 
   
    img.save("signature.png") 

    ##Poniendo la firma en la ubicacion correcta

   
    firmado=[]  
    Image1 = Image.open(aux2[j]) 
    Image1copy = Image1.copy() 
    Image2 = Image.open('signature.png') 
    Image2copy = Image2.copy() 
    Image1copy.paste(Image2copy,(newx, newy-height)) 
    Image1copy.save(aux2[j])
