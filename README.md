# Uniovi News Scraper Pipeline 📰

A Python automation pipeline that scrapes weekly news from the University of Oviedo website, compiles them into Excel, emails the report, downloads associated images, and stores everything in a MySQL database.

## 📋 Table of Contents

* [🚀 Project Overview](#-project-overview)
* [📂 Repository Structure](#-repository-structure)
* [⚙️ Installation & Setup](#️-installation--setup)
* [🛠️ Configuration](#️-configuration)
* [▶️ Usage](#️-usage)
* [📦 Module Descriptions](#-module-descriptions)
* [🔄 Data Flow](#-data-flow)
* [📜 License](#-license)
* [✉️ Contact](#️-contact)

---

## 🚀 Project Overview

This project automates end-to-end news collection from the University of Oviedo site:

* Scrape the latest week’s articles
* Export them to an Excel file
* Email the report to stakeholders
* Download all inline images
* Store both text data and images in a MySQL database

---

## 📂 Repository Structure

```plaintext
uniovi-news-scraper-pipeline/
├── credentials.py        # Configuration variables: paths, DB & email creds
├── functions.py          # WebScraper class: scrape & export to Excel
├── main.py               # Orchestrator: runs the full pipeline
├── message_inicial.py    # Initial GUI confirmation
├── url_to_image.py       # Image downloading module
├── BBDD.py               # MySQL database interaction (procedural)
├── BBDD_OOP.py           # MySQL database interaction (object-oriented)
├── correo.py             # Email sending module
└── README.md             # Project documentation
```

---

## ⚙️ Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/alejandromorislara/uniovi-news-scraper.git
   cd uniovi-news-scraper
   ```

2. **Create & activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies**

   ```bash
   pip install selenium beautifulsoup4 pandas openpyxl mysql-connector-python
   ```

4. **Download ChromeDriver**

   * Ensure the ChromeDriver binary matches your Chrome version.
   * Place it somewhere on your `PATH` or note its full path for configuration.

---

## 🛠️ Configuration

Edit `credentials.py` and set the following variables:

```python
# Path to your ChromeDriver binary
chrome_driver_path = "/path/to/chromedriver"

# Base URL of the University of Oviedo news site
url = "https://uniovi.es/noticias"

# Email settings
smtp_server = "smtp.example.com"
smtp_port = 587
sender_email = "sender@example.com"
sender_password = "yourpassword"
recipient_list = ["recipient1@example.com", "recipient2@example.com"]

# MySQL settings
mysql_host = "localhost"
mysql_port = 3306
mysql_user = "dbuser"
mysql_password = "dbpassword"
mysql_database = "uniovi_news"

# Output paths
path_excel_noticias = "/path/to/output/excels"
directory_images = "/path/to/output/images"
```

---

## ▶️ Usage

Simply run the orchestrator to execute the full pipeline:

```bash
python main.py
```

The pipeline will:

1. Show an initial confirmation dialog (`message_inicial.py`).
2. Scrape the last 7 days of news (`functions.py`).
3. Save an Excel file named `noticias_DD_MM_YYYY.xlsx`.
4. Email that file to configured recipients (`correo.py`).
5. Download each article’s images to `directory_images/YYYYMMDD/` (`url_to_image.py`).
6. Insert records and blob-store images into MySQL (`BBDD.py` or `BBDD_OOP.py`).

---

## 📦 Module Descriptions

* **`credentials.py`**: Holds all configurable parameters and secrets (paths, URLs, credentials).
* **`functions.py`**: Defines the `WebScraper` class to navigate pages with Selenium, parse with BeautifulSoup, build a DataFrame, and export to Excel.
* **`main.py`**: Imports all modules, runs each step in sequence, and handles errors/logging.
* **`message_inicial.py`**: Pops up a simple GUI window (Tkinter) to confirm whether to start scraping.
* **`url_to_image.py`**: Reads the Excel report, iterates over image URLs, downloads each, and renames files for DB insertion.
* **`BBDD.py` & `BBDD_OOP.py`**: Two approaches to load data into MySQL: procedural vs. object-oriented.
* **`correo.py`**: Finds the most recent Excel report, composes an email with attachment, and sends via SMTP.

---

## 🔄 Data Flow

```plaintext
Scrape → Excel:          functions.WebScraper.scrape() → DataFrame → to_excel()
Excel → Email:           correo.send_latest_report()
Excel → Images:          url_to_image.download_all()
Excel & Images → MySQL:  Text data: INSERT rows
                        Blob data: LOAD_FILE or parameterized BLOB upload
```

---

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## ✉️ Contact

**Author**: Alejandro Morís Lara
**Email**: [alejandrgi2g@gmail.com](mailto:alejandrgi2g@gmail.com)
