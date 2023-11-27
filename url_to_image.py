import os
import requests
import pandas as pd
from datetime import datetime
from credentials import credentials_dict

class Image:
    def __init__(self, url):
        self.url = url
        self.output_directory = credentials_dict.get('directory_images', 'images')

    def download_image(self, index):
        os.makedirs(self.output_directory, exist_ok=True)

        response = requests.get(self.url)

        if response.status_code == 200:
            # Crear la subcarpeta con el nombre de la fecha actual
            subfolder_name = self.current_date()
            subfolder_path = os.path.join(self.output_directory, subfolder_name)
            os.makedirs(subfolder_path, exist_ok=True)

            # Obtener el nombre del archivo de la URL
            file_name = os.path.join(subfolder_path, f"image{index}.jpg")

            # Guardar la imagen en la ruta especificada
            with open(file_name, "wb") as f:
                f.write(response.content)
            print(f"La imagen se ha descargado correctamente en: {file_name}")
        else:
            print(f"Error al descargar la imagen. Código de estado HTTP {response.status_code}")
    
    def current_date(self):
        return datetime.now().strftime('%d_%m_%Y').replace(':', '_')

    def download_all_images(self):
        df = pd.read_excel(os.path.join(credentials_dict['path_excel_noticias'], f'noticias_{self.current_date()}.xlsx'))
        all_urls = df['image']

        for index, url in enumerate(all_urls):
            self.url = url  # Configurar la URL para cada iteración
            self.download_image(index)


