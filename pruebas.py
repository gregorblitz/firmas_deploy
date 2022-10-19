from tkinter import *
from PIL import ImageTk,Image,ImageDraw,ImageFont
from tkinter import messagebox
from tkinter import filedialog

import datetime

import sys
import os



#---------FUNCIONES-----------

def abrirFirma():
    root.filename = filedialog.askopenfilename(initialdir = "C:",title = "Seleccionar Firma", filetypes =( ('image files', ('*.png', '*.jpg')),("all files","*.*")))
    ubicacionFirma.set(root.filename)
    
    
def tipodeFirma(tipoFirmaobt):
    
    if tipoFirmaobt=="Nombre":
        cargarFirma(entradaNombre.get(),entradaApellido.get(),"Nombre","")
    elif tipoFirmaobt=="Manuscrito":
        
        Label(ConfigInicial, text="Cargar Firma: ", font=(fuente, 14)).grid(row=3, column=0, sticky=W, pady=10)
        botonCargar = Button(ConfigInicial, text="  Abrir archivo..  ",command = abrirFirma,font=(fuente, 14)).grid(row=3, column=1, sticky=W, pady=10,padx=10)
        botonMostrar = Button(ConfigInicial, text="Cargar",command = lambda: cargarFirma(entradaNombre.get(),entradaApellido.get(),Firmado.get(),ubicacionFirma.get()),font=(fuente, 14)).grid(row=3, column=2, sticky=W, pady=10,padx=10)


def carpEntrada():
    filename = filedialog.askdirectory()
    EntCarpeta.set(filename)
    
def carpSalida():
    filename = filedialog.askdirectory()
    SalCarpeta.set(filename)
    
def comenzar():
    print('Hola')
    
def resumen(nombre,apellido,tipofirma,carpetaentrada,carpetasalida):
    
    if nombre == "":
        errorNombre = messagebox.showerror("Error","No ingresó el campo Nombre")
    if nombre.isalpha()== False:
            errorNombre = messagebox.showerror("Error","Ingreso un caracter no valido en el campo nombre")
    if apellido.isalpha()== False:
            errorApellido = messagebox.showerror("Error","Ingreso un caracter no valido en el campo apellido")
    if apellido == "":
        errorApellido = messagebox.showerror("Error","No ingresó el campo Apellido")
    
    if tipofirma == "Seleccionar...":
        errorFirma = messagebox.showerror("Error","No ingresó el campo Tipo de Firma")
        
    if carpetaentrada == "":
        errorCarpEnt = messagebox.showerror("Error","No ingresó el campo Carpeta de Entrada")
        
    if carpetasalida == "":
        errorCarpSal = messagebox.showerror("Error","No ingresó el campo Carpeta de Salida")
    
    if nombre != "" and apellido != "" and tipofirma != "Seleccionar..." and carpetaentrada != "" and carpetasalida != "":
        
        response = messagebox.askyesno("Verifique los datos "
                                       ,"Nombre: "+nombre+"\n\nApellido: "+apellido
                                       +"\n\nTipo de Firma: "+tipofirma
                                       +"\n\nCarpeta de Entrada: "+carpetaentrada
                                       +"\n\nCarpeta de Salida: "+carpetasalida)
        #Label(root, text=response).pack()
        
        if response == 1:
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
            import img2pdf
    
            name_doc=[]
            name_pages=[]
            last_page=[]
            number_pages=[]
            packtopdf=[]
            cont=0
            aux1=0
            aux2=0
            contenido = os.listdir(EntCarpeta.get())
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
                a=entradaNombre.get()
                a=a.split()
                bloque=0
                i=0
                total=n_boxes
                
                newdata=[5000,5000]
                while (i<total-1):
                    bloque=bloque+1
                    i=i+1
                    if(data_image['text'][i].casefold()==a[0].casefold()  ):
                        newdata=[0,0]
                        newdata=[data_image['left'][bloque],data_image['top'][bloque]]
                print(newdata)
                newx=newdata[0]
                newy=newdata[1]
        
                

                ##Conociendo el tamaño de la firma  
                img = Image.open('firmafinal.png') 
                
                width = img.width 
                height = img.height +3
                
    
                ##Poniendo la firma en la ubicacion correcta
                firmado=[]  
                Image1 = Image.open(last_page[j]) 
                Image1copy = Image1.copy() 
                Image2 = Image.open('firmafinal.png') 
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
    
            for i in name_doc:
                name_file=(EntCarpeta.get()+'/'+i)
                shutil.move(name_file,SalCarpeta.get())
            for i in name_pages:
                 os.remove(i) 
        
def cargarFirma(nombre,apellido,opcion,ubicFirma):
    
    if opcion=="Manuscrito":
        firmapuesta = Image.open(ubicFirma)
        firmapuesta = firmapuesta.resize((220,80))
  
        img1 = Image.open(r"Base_m.png") 
        img1=img1.resize((240,110))
        img2 = firmapuesta
  
        img1.paste(img2,(10,0)) 
  
        #img1.show() 
      
        fecha_hora = datetime.datetime.now()
        h = fecha_hora.strftime("%d/%m/%Y, %H:%M:%S")
        #base=Image.open("img2.png").convert("RGBA")
        base=img1.convert("RGBA")
        txt=Image.new("RGBA",base.size,(255,255,255,0))
        fnt1=ImageFont.truetype("times.ttf",12)
        Nombres=ImageDraw.Draw(txt)
        fecha = f'Firmado {h}'
        Nombres.text((30,80),fecha ,font=fnt1,fill=(0,0,0))
        out=Image.alpha_composite(base,txt)
        out.save("Manuscrito_fecha.png")
        
        firmapuesta=out
        firmapuestaimg = ImageTk.PhotoImage(firmapuesta)

                              
        firmafinal = Label(firmamos,image=firmapuestaimg) 
        firmafinal.image = firmapuestaimg
        firmafinal.grid(row=1, column=0,padx=80)
        
        
        firmafecha = Image.open("Manuscrito_fecha.png")
        firmafecha = firmafecha.resize((220,80))
        firmafecha.save("firmafinal.png")
        
    else:

        Tamaño_N=len(str(nombre)+str(apellido))

        

        fecha_hora = datetime.datetime.now()
        h = fecha_hora.strftime("%d/%m/%Y, %H:%M:%S")
        base=Image.open("base.png").convert("RGBA")
        txt=Image.new("RGBA",base.size,(255,255,255,0))
        if Tamaño_N <19 :
         fnt=ImageFont.truetype("times.ttf",20)
         fnt1=ImageFont.truetype("times.ttf",12)
        else:
                fnt=ImageFont.truetype("times.ttf",14)
                fnt1=ImageFont.truetype("times.ttf",11)
        

        Nombres=ImageDraw.Draw(txt)
        fecha = f'Firmado {h}'
        Nombres.text((2,7),str(nombre)+" "+str(apellido),font=fnt,fill=(0,0,0))
        Nombres.text((2,28),fecha ,font=fnt1,fill=(0,0,0))
        out=Image.alpha_composite(base,txt)
        out.save("Nombres.png")
        
        firmapuesta = Image.open("Nombres.png")
        firmapuesta = firmapuesta.resize((220,80))
        firmapuestaimg = ImageTk.PhotoImage(firmapuesta)
                              
        firmafinal = Label(firmamos,image=firmapuestaimg) 
        firmafinal.image = firmapuestaimg
        firmafinal.grid(row=1, column=0,padx=80)
        
        firmafecha = Image.open("Nombres.png")
        firmafecha = firmafecha.resize((220,80))
        firmafecha.save("firmafinal.png")

#----------------------------------------



#------Configuraciones Iniciales---------------
#Inicializa el tkinter
root = Tk()

#Tamaño de la ventana
root.geometry("1000x600")
root.resizable(False,False) #No permite hacer la ventana mas grande

#Permite colocarle un titulo al programa
root.title("Firmas Gen XXI")

#Permite colocarle el logo al programa
root.iconbitmap("clarocirculo.ico")

#----------------------------------------------

fuente = "DIN Alternate"

#-----------------LOGOS------------------------
#Permite Poner el texto del proyecto
FirmaTexto = "                            Firmas Gen XXI                           "
FirmaTxt = Label(root,text=FirmaTexto,font=(fuente,18)).grid(row=1,column=1)#Puede marcar error si no se tiene el font instalado

#Permite Poner el Logo de Claro
LogoClaro = Image.open("claroplano.png")
LogoClaro = LogoClaro.resize((220,80))
LogoImg = ImageTk.PhotoImage(LogoClaro)
                      
LogoPoner = Label(image=LogoImg) 
LogoPoner.image = LogoImg
LogoPoner.grid(row=1, column=0)


#Permite Poner el Logo de Gen XXI
LogoGen = Image.open("genlogo2.png")
LogoGen = LogoGen.resize((200,100))
LogoGImg = ImageTk.PhotoImage(LogoGen)
                      
LogoGPoner = Label(image=LogoGImg)
LogoGPoner.image = LogoGImg
LogoGPoner.grid(row=1, column=2)
#----------------------------------------------


#------------Hacer los frames--------------
ConfigInicial = Frame(root, bd=2, relief=SOLID, padx=10, pady=10)
archivos = Frame(root, bd=2, relief=SOLID, padx=10, pady=10)
firmamos = Frame(root, bd=2, relief=SOLID, padx=10, pady=10)
progreso = Frame(root, bd=2, relief=SOLID, padx=10, pady=10)
#----------------------------------------------

#------------------Para ingresar Nombre--------
Label(ConfigInicial, text="Ingrese Nombre: ", font=(fuente, 14)).grid(row=0, column=0, sticky=W, pady=10)
entradaNombre = Entry(ConfigInicial, font=(fuente, 14))
entradaNombre.grid(row=0, column=1, pady=10, padx=20)

#---------------------------------------------

#------------------Para ingresar Apellido--------
Label(ConfigInicial, text="Ingrese Apellido: ", font=(fuente, 14)).grid(row=1, column=0, pady=10)
entradaApellido = Entry(ConfigInicial, font=(fuente, 14))
entradaApellido.grid(row=1, column=1, pady=10, padx=20)
#---------------------------------------------


#---------Menu desplegable tipo de firma--------
Label(ConfigInicial, text="Tipo de Firma: ", font=(fuente, 14)).grid(row=2, column=0, sticky=W, pady=10)
opcionesFirma = ["Seleccionar...","Manuscrito","Nombre"]
Firmado = StringVar()
Firmado.set(opcionesFirma[0])
menuFirma = OptionMenu(ConfigInicial, Firmado,*opcionesFirma)
menuFirma.grid(row=2, column=1, pady=10, padx=0)
menuFirma.config(width=15, font=(fuente, 14))

botonAceptar = Button(ConfigInicial, text="Aceptar",command =lambda: tipodeFirma(Firmado.get()),font=(fuente, 14)).grid(row=2, column=2, sticky=W, pady=10,padx=10)
#-----------------------------------------------

#------------Cargar Firma---------------------
ubicacionFirma = StringVar()

#Label(ConfigInicial, text="...", textvariable = ubicacionFirma, font=(fuente, 14)).grid(row=4, column=0, sticky=W, pady=10) #Para probar nada mas
#--------------------------------------------

ConfigInicial.place(x=50, y=150)


Label(firmamos, text="Firma ingresada: ", font=(fuente, 14)).grid(row=0, column=0, sticky=W, pady=10)
firmamos.place(x=50,y=400)

Label(progreso, text="Progreso ", font=(fuente, 14)).grid(row=0, column=0, sticky=W, pady=10)
progreso.place(x=580,y=370)



#--------Frame Derecho-------------------
EntCarpeta = StringVar()
SalCarpeta = StringVar()

Label(archivos, text="Entrada Carpeta: ", font=(fuente, 14)).grid(row=0, column=0, sticky=W, pady=10)
botonEntCarpeta = Button(archivos, text="  Abrir carpeta..  ",command = carpEntrada,font=(fuente, 14)).grid(row=0, column=1, sticky=W, pady=10,padx=20)
Label(archivos, text="Salida Carpeta: ", font=(fuente, 14)).grid(row=1, column=0, sticky=W, pady=10)
botonSalCarpeta = Button(archivos, text="  Abrir carpeta..  ",command = carpSalida,font=(fuente, 14)).grid(row=1, column=1, sticky=W, pady=10,padx=20)

#Label(archivos, text="...", textvariable = EntCarpeta, font=(fuente, 14)).grid(row=3, column=0, sticky=W, pady=10) #Para probar nada mas
#Label(archivos, text="...", textvariable = SalCarpeta, font=(fuente, 14)).grid(row=4, column=0, sticky=W, pady=10) #Para probar nada mas

botonComenzar = Button(archivos, width=15, text='Verificar', font=(fuente, 14)
                       , command=lambda: resumen(entradaNombre.get(),entradaApellido.get(),Firmado.get(),EntCarpeta.get(),SalCarpeta.get()))
botonComenzar.grid(row=7, column=1, pady=10, padx=20)

#-------------------------------------------
archivos.place(x=580, y=150)


root.mainloop()
