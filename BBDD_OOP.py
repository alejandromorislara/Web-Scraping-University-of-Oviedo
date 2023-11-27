import os
import mysql.connector
from datetime import datetime
import pandas as pd
import locale
from credentials import credentials_dict

# Hora española
locale.setlocale(locale.LC_TIME, 'es_ES')


class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            if self.connection.is_connected():
                print("Connected to MySQL database")
                self.cursor = self.connection.cursor()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def close_connection(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Connection closed")

    def create_excel_table(self):
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS excel (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                url_image VARCHAR(255) NOT NULL,
                content TEXT,
                date DATE
            )
        '''
        self.cursor.execute(create_table_query)
        print("Table 'excel' created successfully")

    def insert_excel_data(self, df):
        for index, row in df.iterrows():
            fecha_str = row['date']
            fecha_datetime = datetime.strptime(fecha_str, '%d %B %Y')
            fecha_mysql = fecha_datetime.strftime('%Y-%m-%d')

            values = (row['title'], row['image'], row['content'], fecha_mysql)

            insert_query = '''
                INSERT INTO excel (title, url_image, content, date)
                VALUES (%s, %s, %s, %s)
            '''
            self.cursor.execute(insert_query, values)

        self.connection.commit()
        print("Data inserted successfully")

    def create_news_images_table(self):
        create_news_images_table_query = '''
            CREATE TABLE IF NOT EXISTS news_images (
                id_noticia INT AUTO_INCREMENT PRIMARY KEY,
                image_name VARCHAR(255),
                ruta TEXT,
                carpeta TEXT,
                FOREIGN KEY (id_noticia) REFERENCES excel(id)
            )
        '''
        self.cursor.execute(create_news_images_table_query)
        print("Table 'news_images' created successfully")

    def insert_news_images_data(self, folder_path_to_insert):
        if os.path.exists(folder_path_to_insert):
            for elemento in os.listdir(folder_path_to_insert):
                image_path = os.path.join(folder_path_to_insert, elemento)
                file_name = os.path.splitext(elemento)[0]
                values = (file_name, image_path, folder_path_to_insert)

                insert_query = '''
                    INSERT INTO news_images (image_name, ruta, carpeta)
                    VALUES (%s, %s, %s)
                '''
                self.cursor.execute(insert_query, values)

            self.connection.commit()
            print('Images inserted')
        else:
            print(f"No folder found for the current date: {current_date()}")


class FileManager:
    def __init__(self, directory_images):
        self.directory_images = directory_images

    def current_date(self):
        return datetime.now().strftime('%d_%m_%Y').replace(':', '_')

    def read_excel_file(self, file_path):
        return pd.read_excel(file_path)


def main():
    host = "localhost"
    user = credentials_dict['user']
    password = credentials_dict['sql_pass']
    database = credentials_dict['database_name']

    database_manager = DatabaseManager(host, user, password, database)
    file_manager = FileManager(credentials_dict['directory_images'])

    database_manager.connect()
    database_manager.create_excel_table()

    df = file_manager.read_excel_file(os.path.join(credentials_dict['path_excel_noticias'], f'noticias_{file_manager.current_date()}.xlsx'))

    database_manager.insert_excel_data(df)
    database_manager.create_news_images_table()

    folder_path_to_insert = os.path.join(credentials_dict['directory_images'], file_manager.current_date())
    database_manager.insert_news_images_data(folder_path_to_insert)

    database_manager.close_connection()


if __name__ == "__main__":
    main()
