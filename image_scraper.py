# import csv
import os

# from tkinter import image_names
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import urllib
import urllib.request

# import scrapy
import requests

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


class image_scrape:
    """
    Collect NFT images from OPENSEA.IO, based on the ranking of collections.
    """

    def __init__(self, df, url="https://opensea.io/rankings"):
        self.url = url
        self.second_url = ""
        self.df = df

    def Web_driver(self):

        """
        Preparing selenium chrome webdriver
        """

        options = Options()
        options.headless = False
        options.add_experimental_option("detach", True)
        s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=s, options=options)

        return self.driver.get(self.url)

    def get_collection_title(self, index):

        """
        Get collections from previous collected ranking data table.
        """

        return self.df.iat[index, 1]  # Using .iat attribute

    def get_image_addresses_of_the_collection(self, collection):

        """
        Click and open collection page, maximise the window, scroll the page to an appropriate level,
        and get corresponding images addresses

        """
        try:
            self.driver.find_element(
                By.XPATH,
                "//*[@id='__next']/div/div[1]/nav/div[2]/div/div/div[1]/div[2]/button/i",
            ).click()
        except:
            pass

        time.sleep(2)
        elem = self.driver.find_element(
            By.CSS_SELECTOR,
            "#__next > div > div.Navbarreact__DivContainer-sc-d040ow-1.iiAfil > nav > div.Blockreact__Block-sc-1xf18x6-0.Flexreact__Flex-sc-1twd32i-0.eAPuiF.jYqxGr.fresnel-greaterThanOrEqual-sm > div > div > div > input[type=text]",
        )

        elem.send_keys(collection)

        time.sleep(2)

        self.driver.find_element(
            By.XPATH, "//*[@id='NavSearch--results']/li[2]/a/div[2]/span"
        ).click()

        # scroll the page to an appropriate level
        self.driver.maximize_window()
        time.sleep(2)
        level = self.driver.find_element(
            By.CSS_SELECTOR,
            "#main > div > div > div.Blockreact__Block-sc-1xf18x6-0.elqhCm > div > div > div > div.AssetSearchView--results.collection--results > div.Blockreact__Block-sc-1xf18x6-0.elqhCm.AssetsSearchView--assets > div.fresnel-container.fresnel-greaterThanOrEqual-sm > div > div",
        )

        self.driver.execute_script("arguments[0].scrollIntoView(true);", level)

        # d = self.driver.find_elements(
        #     By.CSS_SELECTOR,
        #     "#main > div > div > div.Blockreact__Block-sc-1xf18x6-0.elqhCm > div > div > div > div.AssetSearchView--results.collection--results > div.Blockreact__Block-sc-1xf18x6-0.elqhCm.AssetsSearchView--assets > div.fresnel-container.fresnel-greaterThanOrEqual-sm > div > div > div:nth-child(1) > div > article > a > div.Blockreact__Block-sc-1xf18x6-0.AssetCardContentreact__StyledContainer-sc-a8q9zx-0.dNtdmG.egubqN > div > div > div > img",
        # )
        time.sleep(2)
        d = self.driver.find_elements(By.XPATH, '//div[@role = "gridcell"]')

        d = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'assets')]")

        links = [i.get_attribute("href") for i in d]

        return links

    def collect_images(self, links, path):
        """
        Open another window for each NFT item, get the image and save to drive.
        The reason for doing this way is because the iamge quality on the item own page better than on
        the collection page.
        """
        # open seconf window/tag,
        # self.driver.execute_script("window.open('');")
        # Switch to the new window
        self.driver.switch_to.window(self.driver.window_handles[1])

        # self.second_url = self.driver.current_window_handle

        for i in range(len(links) - 1):
            try:

                self.driver.get(links[i + 1])
                # switch to the link in a new tab by sending key strokes on the element
                # d = self.driver.find_elements(By.XPATH, '//div[@role = "gridcell"]')
                time.sleep(1)
                image = self.driver.find_element(
                    By.XPATH,
                    "//*[@id='main']/div/div/div/div[1]/div/div[1]/div[1]/article/div/div/div/div/img",
                )
                r = requests.get(image.get_attribute("src"))
                with open(path + str(i + 1) + ".jpg", "wb") as f:
                    f.write(r.content)
            except:
                continue

        self.driver.switch_to.window(self.driver.window_handles[0])

        # image_addresses = self.driver.find_elements(By.TAG_NAME, "img")


if __name__ == "__main__":

    df = pd.read_csv(
        "nft_ranking1.csv", index_col=0
    )  # this is going introduce from rds or inter memory.
    image_scraper = image_scrape(df)
    driver = image_scraper.Web_driver()
    image_scraper.driver.execute_script("window.open('');")
    image_scraper.driver.switch_to.window(image_scraper.driver.window_handles[0])

    for i in range(25):
        collection_path = (
            "/home/h1m1w1/Documents/AiCore-project/scraper_cloud/images/" + df.iat[i, 8]
        )
        os.mkdir(collection_path)
        collection = image_scraper.get_collection_title(i)

        links = image_scraper.get_image_addresses_of_the_collection(collection)

        path = collection_path + "/" + df.iat[i, 8]
        image_scraper.collect_images(links, path)

    image_scraper.driver.quit()
