import csv
from tkinter import image_names
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import urllib
import urllib.request
import scrapy
import requests
from bs4 import BeautifulSoup
import time
import datetime
from botocore.errorfactory import ClientError
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
import json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pandas as pd


class image_scrape:
    def __init__(self):
        pass

    def Web_driver(self):
        url = "https://opensea.io/rankings"
        options = Options()
        options.headless = False
        options.add_experimental_option("detach", True)
        s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=s, options=options)

        return self.driver.get(url)

    def get_collection_title(self, df, index):
        # df = pd.read_csv('nft_ranking1.csv', index_col=0)

        return df.iat[index, 1]  # Using .iat attribute

    def get_images(self, collection):

        elem = self.driver.find_element(
            By.CSS_SELECTOR,
            "#__next > div > div.Navbarreact__DivContainer-sc-d040ow-1.iiAfil > nav > div.Blockreact__Block-sc-1xf18x6-0.Flexreact__Flex-sc-1twd32i-0.eAPuiF.jYqxGr.fresnel-greaterThanOrEqual-sm > div > div > div > input[type=text]",
        ).send_keys(collection)
        # elem.send_keys("Star Wolves")
        time.sleep(1)

        self.driver.find_element(
            By.XPATH, "//*[@id='NavSearch--results']/li[2]/a/div[2]/span"
        ).click()

        self.driver.maximize_window()
        l = self.driver.find_element(
            By.CSS_SELECTOR,
            "#main > div > div > div.Blockreact__Block-sc-1xf18x6-0.elqhCm > div > div > div > div.AssetSearchView--results.collection--results > div.Blockreact__Block-sc-1xf18x6-0.elqhCm.AssetsSearchView--assets > div.fresnel-container.fresnel-greaterThanOrEqual-sm > div > div",
        )

        self.driver.execute_script("arguments[0].scrollIntoView(true);", l)

        d = self.driver.find_elements(
            By.CSS_SELECTOR,
            "#main > div > div > div.Blockreact__Block-sc-1xf18x6-0.elqhCm > div > div > div > div.AssetSearchView--results.collection--results > div.Blockreact__Block-sc-1xf18x6-0.elqhCm.AssetsSearchView--assets > div.fresnel-container.fresnel-greaterThanOrEqual-sm > div > div > div:nth-child(1) > div > article > a > div.Blockreact__Block-sc-1xf18x6-0.AssetCardContentreact__StyledContainer-sc-a8q9zx-0.dNtdmG.egubqN > div > div > div > img",
        )

        d = self.driver.find_elements(
            By.CSS_SELECTOR,
            "#main > div > div > div.Blockreact__Block-sc-1xf18x6-0.elqhCm > div > div > div > div.AssetSearchView--results.collection--results > div.Blockreact__Block-sc-1xf18x6-0.elqhCm.AssetsSearchView--assets > div.fresnel-container.fresnel-greaterThanOrEqual-sm > div > div > div:nth-child(1) > div > article > a > div.Blockreact__Block-sc-1xf18x6-0.AssetCardContentreact__StyledContainer-sc-a8q9zx-0.dNtdmG.egubqN > div > div > div > img",
        )

        images = self.driver.find_elements_by_tag_name("img")

        return images

    def save_image(image_address, saving_path):

        # urllib.request.urlretrieve(d.get_attribute('src'), "/home/h1m1w1/Documents/AiCore-project/practice/web-scraping/screenshot.png")
        for image in image_address:
            urllib.request.urlretrieve(image, saving_path)


if __name__ == "__main__":

    image_scraper = image_scrape()
    driver = image_scraper.Web_driver()
    df = pd.read_csv(
        "nft_ranking1.csv", index_col=0
    )  # this is going introduce from rds.
    for i in range(2):
        collection = image_scraper.get_collection_title(df, i)
        images = image_scraper.get_images(collection)
        image_scraper.save_image(
            images, saving_path="/home/h1m1w1/Documents/AiCore-project/scraper_cloud/"
        )  # this is to be change to cloud address

    driver.close()
