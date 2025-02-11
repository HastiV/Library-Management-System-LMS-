import time
import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Setup Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

#  1. Scrape Data from "Books to Scrape" using Selenium
def scrape_books_to_scrape():
    print("Scraping Books to Scrape...")
    books = []
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"

    for page in range(1, 3):  # Scrape first 2 pages (change as needed)
        driver.get(base_url.format(page))
        time.sleep(2)  # Allow time for page to load
        
        # Find all books
        book_elements = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")
        
        for book in book_elements:
            title = book.find_element(By.TAG_NAME, "h3").text
            price = book.find_element(By.CSS_SELECTOR, "p.price_color").text
            availability = book.find_element(By.CSS_SELECTOR, "p.instock.availability").text.strip()
            books.append([title, price, availability])

    return books

#  2. Scrape Data from "Open Library" using BeautifulSoup
def scrape_open_library():
    print("Scraping Open Library...")
    url = "https://openlibrary.org/subjects/programming"  # Change category as needed
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    books = []
    book_elements = soup.select("div.bookcover")[:10]  # Get first 10 books
    
    for book in book_elements:
        title = book.find("img")["alt"]
        author = book.find_next("p", class_="by").text.strip() if book.find_next("p", class_="by") else "Unknown"
        books.append([title, author])

    return books

#  3. Save Data to CSV
def save_to_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Price/Author", "Availability/Category"])
        writer.writerows(data)
    print(f"Data saved to {filename}")

# Execute the scraping functions
books_data1 = scrape_books_to_scrape()
books_data2 = scrape_open_library()

# Save results
save_to_csv(books_data1, "books_to_scrape.csv")
save_to_csv(books_data2, "open_library_books.csv")

# Close WebDriver
driver.quit()
print("Scraping Completed!")
