from functions import WebScraper # Clase para el WebScraping

import time

from credentials import credentials_dict # Importa el diccionario de credentials

from correo import EmailSender # Importa el sender para enviar ficheros por correo

from url_to_image import Image # Importa el descargador de imágenes a partir de una URL

from message_inicial import MensajeAutodestructivo

from BBDD_OOP import DatabaseManager, FileManager,main


MensajeAutodestructivo()  #Message inicial

chrome_driver_path = credentials_dict['chrome_driver_path'] # Ruta del ejecutable de Chrome en credentials
inicio=time.time()

# Ejecutar el proceso de scraping( todo completo )

WebScraper.run_web_scraping_process(chrome_driver_path)
time.sleep(5)

#Enviamos el excel por email

email_sender = EmailSender()
email_sender.send_email()

# Descargamos todas las imágenes de las noticias de la semana, y las guardamos en su subcarpeta corrrspondiente

Image=Image(credentials_dict['url']) # La URL no es importante, da igual cual pongamos
Image.download_all_images()


#PASAMOS TODOS LOS DATOS A LA BDD

main()

print('Fin del proceso')

final=time.time()

duración=final-inicio

print(f"Tiempo transcurrido: {int(duración//60)}'{int(duración%60)}''")
