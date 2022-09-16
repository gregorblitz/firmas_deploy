# import module
from pdf2image import convert_from_path
 
 
# Store Pdf with convert_from_path function
images = convert_from_path('Respuesta Req Cantagallo GI2843.pdf')
#x=len(images)  
  
images[len(images)-1].save('last_page'+'.jpg', 'JPEG')

