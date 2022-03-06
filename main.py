import data_scraper, image_scraper
import pandas as pd
import time
import uuid
import os


# Collecting data
scraper = data_scraper.nft_scraper()
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


# Collecting images
df = pd.read_csv(
    "nft_ranking1.csv", index_col=0
)  # this is going introduce from rds or inter memory.
image_scraper = image_scraper.image_scrape(df)
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
