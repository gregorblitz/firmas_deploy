"""import os
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
import img2pdf

name_doc=[]
name_pages=[]
last_page=[]
number_pages=[]
packtopdf=[]
docsf=[]
cont=0
aux1=0
aux2=0
contenido = os.listdir('C:/Users/USUARIO/OneDrive/Escritorio/desarrolladores_claro/firma-pdf')
for i in contenido:
    if i.endswith('.pdf'):
            name_doc.append(i)
            images = convert_from_path(i)
            number_pages.append(len(images))
            for j in range(len(images)):
                
                images[j].save( i + str(j) +'.jpg')
                name_pages.append(( i + str(j) +'.jpg'))
                ultima_pag=(( i + str(j) +'.jpg'))
            last_page.append(ultima_pag)
            
for j in range(0,len(last_page)):

    path_Example = last_page[j]
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
    a='acevedo'
    b='torres'
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
    filepath = 'signature.png'
    img = Image.open(filepath) 
    
    width = img.width 
    height = img.height +3
    

    ##Poniendo la firma en la ubicacion correcta
    firmado=[]  
    Image1 = Image.open(last_page[j]) 
    Image1copy = Image1.copy() 
    Image2 = Image.open(filepath) 
    Image2copy = Image2.copy() 
    Image1copy.paste(Image2copy,(newx, newy-height)) 
    Image1copy.save(last_page[j])


for i in number_pages:
    aux2=aux1+i
    for j in range(aux1,aux2):
        packtopdf.append(name_pages[j])
    a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297))
    layout_fun = img2pdf.get_layout_fun(a4inpt)
    with open(name_doc[cont], "wb") as documento:
        documento.write(img2pdf.convert(packtopdf,layout_fun=layout_fun))

    cont+=1
    aux1=aux2
    packtopdf=[]
"""