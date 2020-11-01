from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time


def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # visit mars new site
    url = "https://mars.nasa.gov/news"
    browser.visit(url)

    time.sleep(2)

    html = browser.html
    soup = bs(html, "html.parser")

    # get news title
    headline = soup.find_all("div", class_="content_title")
    news_headline = headline[1].text

    # get paragraph text
    pargs = soup.find_all("div", class_="article_teaser_body")
    parg_text = pargs[0].text

    # visit image url
    pic_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(pic_url)

    time.sleep(1)

    # click through links to find image
    browser.links.find_by_partial_text("FULL IMAGE")
    time.sleep(2)
    browser.links.find_by_partial_text("more info")
    time.sleep(2)

    html = browser.html
    soup = bs(html, "html.parser")

    # extract image link
    image = soup.find("figure", class_="lede")
    image_url = image.find("a")["href"]
    featured_image_url = "https://www.jpl.nasa.gov" + image_url

    # get mars facts
    facts_url = "https://space-facts.com/mars/"
    tables = pd.read_html(facts_url)

    # visit mars hemispheres html
    mars_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_url)

    browser.links.find_by_partial_text("Cerberus")

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    base_url = "https://astrogeology.usgs.gov"

    # extract image links
    cerberus = soup.find("div", class_="downloads")
    cerberus_link = cerberus.find("img")["src"]
    cerberus_url = base_url + cerberus_link

    browser.back()
    time.sleep(1)

    browser.links.find_by_partial_text("Schiaparelli")
    time.sleep(2)

    schiaparelli = soup.find("div", class_="downloads")
    schiaparelli_link = schiaparelli.find("img")["src"]
    schiaparelli_url = base_url + schiaparelli_link

    browser.back()
    time.sleep(2)

    browser.links.find_by_partial_text("Syrtis")
    time.sleep(2)

    syrtis = soup.find("div", class_="downloads")
    syrtis_link = syrtis.find("img")["src"]
    syrtis_url = base_url + syrtis_link

    browser.links.find_by_partial_text("Valles")
    time.sleep(2)

    valles = soup.find("div", class_="downloads")
    valles_link = valles.find("img")["src"]
    valles_url = base_url + valles_link

    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": {"valles_url"}},
        {"title": "Cerberus Hemisphere", "img_url": {"cerberus_url"}},
        {"title": "Schiaparelli Hemisphere", "img_url": {"schiaparelli_url"}},
        {"title": "Syrtis Major Hemisphere", "img_url": {"syrtis_url"}},
    ]

    mars_data = {
        "Headline": news_headline,
        "Paragraph Text": parg_text,
        "Featured Image": featured_image_url,
        "Mars Facts": tables,
        "Hemispheres": hemisphere_image_urls,
    }

    browser.quit()

    return mars_data
