from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
import locale
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd
import os
from credentials import credentials_dict



# Establece la localización a español
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

class WebScraper:
    def __init__(self, chrome_driver_path):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.binary_location = chrome_driver_path
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.maximize_window()
    
    def navigate_to_url(self):
        self.driver.get('https://www.uniovi.es/')

    def accept_cookies(self):
        button_agree = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "cc_b_ok"))
        )
        button_agree.click()
        print('Acepté las cookies')

    def toggle_webmap(self):
        button_toggler = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'webmapToggler'))
        )
        button_toggler.click()
        print('Web Toggler')

    def go_to_actualidad(self):
        button_actualidad = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@data-id="#child-layouts-166"]'))
        )
        button_actualidad.click()
        print('Actualidad')

    def go_to_noticias(self):
        button_noticias = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "https://www.uniovi.es/actualidad/noticias")]'))
        )
        button_noticias.click()
        print('Cliqué noticias')

    def scroll_down(self, scrolls,sleep=False):
        for i in range(scrolls):
            self.driver.execute_script("window.scrollBy(0, 500);")
            
            if sleep:
                time.sleep(1)

    def set_articles_per_page(self):
        time.sleep(1)
        button_per_page = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, '_com_liferay_asset_publisher_web_portlet_AssetPublisherPortlet_INSTANCE_Ru0cAJNPrm1m_tiym_column2_0_menu'))
        )
        button_per_page.click()
        per_page = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@class='taglib-text-icon' and text()='60']"))
        )
        per_page.click()

    def scrape_news(self):
        my_news = []
        x = True
        while x:
            self.scroll_down(20)
            current_date = datetime.now()
            one_week_ago = current_date - timedelta(days=7)

            article_selector = ".col-index-X"
            total_articles = 25

            articles = []
            for i in range(0, total_articles):
                current_article_selector = f'.col-index-{i}'
                time.sleep(1) # darle tiempo a buscar
                article_i = self.driver.find_elements(By.CSS_SELECTOR, current_article_selector)
                articles.append(article_i[0])
                
            
            
            for article in articles:
                time.sleep(3)
                date_element = article.find_element(By.CSS_SELECTOR, ".date")
                date_text = date_element.text

                try:
                    article_date = datetime.strptime(date_text, '%d %B %Y')
                except ValueError as e:
                    print(f"Error parsing date: {date_text}")
                    print(f"Exception: {e}")
                    raise ValueError

                if str(one_week_ago) <= str(article_date) <= str(current_date):
                    title_element = article.find_element(By.CSS_SELECTOR, ".card-title")
                    title = title_element.text

                    image_element = article.find_element(By.CSS_SELECTOR, ".card-image img")
                    image_url = image_element.get_attribute("src")

                    content_element = article.find_element(By.CSS_SELECTOR, ".card-text")
                    content = content_element.text

                    my_dict = {
                        'title': title,
                        'image': image_url,
                        'content': content,
                        'date': date_text
                    }

                    my_news.append(my_dict)

                else:
                    x = False
        time.sleep(1)
        
        return my_news # retornamos la lista de diccionarios con las últimas noticias

    def number_news(self, my_news:list):

        print(len(my_news))
        self.driver.quit()

    def print_news(self,my_news:list):

        print(my_news)
        self.driver.quit()

    def data_to_excel(self,my_news:list,fecha:str):
            
        df = pd.DataFrame(my_news)
        
        output_directory = credentials_dict['path_excel_noticias']# Carpeta de salida

        
        excel_path = os.path.join(output_directory, f'noticias_{fecha}.xlsx')# Crear la ruta a la carpeta

        # Guardar el DataFrame como un archivo Excel en la ubicación especificada
        df.to_excel(excel_path, index=False)
        print(f"Se ha creado el archivo Excel en {excel_path}")

    def current_date(self):
        return datetime.now().strftime('%d_%m_%Y').replace(':', '_')

    

    def run_web_scraping_process(chrome_driver_path):
        # Crear instancia del scraper
        scraper = WebScraper(chrome_driver_path)

        # Ejecutar pasos
        scraper.navigate_to_url()
        scraper.accept_cookies()
        scraper.toggle_webmap()
        scraper.go_to_actualidad()
        scraper.go_to_noticias()
        scraper.scroll_down(4)  # si queremos pausa-> sleep=True
        scraper.set_articles_per_page()
        scraper.scroll_down(20)  # si queremos pausa-> sleep=True
        my_news = scraper.scrape_news()
        # Llamar a la función data_to_excel y pasarle la lista de noticias
        scraper.data_to_excel(my_news, scraper.current_date())# Pasarle la lista de noticias

        
        





