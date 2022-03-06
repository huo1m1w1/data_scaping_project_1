# import requirements

import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import uuid

# import urllib

# import urllib.request
# import scrapy
# import requests
# from bs4 import BeautifulSoup
import time

# import datetime
# from botocore.errorfactory import ClientError
# from bs4 import BeautifulSoup
# from urllib.request import Request, urlopen
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service

# import json
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pandas as pd


class nft_scraper:
    """
    Collect NFT data based on ranking.
    """

    def __init__(self):

        """
        Initialise the NFT collections' table.
        """
        self.table = pd.DataFrame(
            columns=[
                "Rank",
                "Collection",
                "Volume",
                "24h %",
                "7d %",
                "Floor Price",
                "Owners",
                "Items",
            ]
        )

    def Web_driver(self):

        """
        Prepare selenium chrome webdriver for scraping, set appropriate zoom of window,
         which is able to get all data of the page in two screen, initial screen and bottom screen.

        """
        url = "https://opensea.io/rankings"
        options = Options()
        options.headless = False
        options.add_experimental_option("detach", True)
        s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=s, options=options)
        self.driver.get("chrome://settings/")
        self.driver.execute_script("chrome.settingsPrivate.setDefaultZoom(0.25);")

        return self.driver.get(url)

    def collect_screen_data(self):

        """
        Collect dynamic website data from current screen
        """
        time.sleep(2)
        a = self.driver.find_elements(By.XPATH, '//*[@id="main"]/div/div[2]/div/div[2]')

        b = [i.text for i in a][0].split("\n")
        c = [b[i * 8 : (i + 1) * 8] for i in range(int(len(b) / 8))]

        df = pd.DataFrame(
            c,
            columns=[
                "Rank",
                "Collection",
                "Volume",
                "24h %",
                "7d %",
                "Floor Price",
                "Owners",
                "Items",
            ],
        )
        return df

    def scrolling_down_to_bottom(self):
        """
        scrolling down the page to bottom

        """

        html = self.driver.find_element_by_tag_name("html")
        html.send_keys(Keys.END)
        time.sleep(1)

    def merging_table(self, df, df2):
        df = pd.concat([df, df2], ignore_index=False)
        df = df.drop_duplicates()
        df["Rank"] = df["Rank"].astype(str).astype(int)
        self.table = df.sort_values(by=["Rank"])
        return self.table

    def click_to_next_page(self):
        next = self.driver.find_element(
            By.XPATH, "//*[@id='main']/div/div[3]/button[2]"
        )
        self.driver.execute_script("arguments[0].click();", next)

    def save_table(self):
        self.table.to_csv("nft_ranking1.csv")


if __name__ == "__main__":

    scraper = nft_scraper()
    scraper.table = pd.DataFrame(
        columns=[
            "Rank",
            "Collection",
            "Volume",
            "24h %",
            "7d %",
            "Floor Price",
            "Owners",
            "Items",
        ]
    )
    driver = scraper.Web_driver()

    for i in range(10):
        time.sleep(2)
        data = scraper.collect_screen_data()
        scraper.merging_table(scraper.table, data)
        scraper.scrolling_down_to_bottom()
        data = scraper.collect_screen_data()
        scraper.merging_table(scraper.table, data)
        scraper.click_to_next_page()

    unique_ids = [uuid.uuid4() for i in range(len(scraper.table))]
    scraper.table["uuid"] = unique_ids
    scraper.table.to_csv(
        "/home/h1m1w1/Documents/AiCore-project/scraper_cloud/nft_ranking1.csv"
    )
    scraper.driver.quit()
