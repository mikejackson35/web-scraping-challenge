# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo
from flask import Flask, render_template, redirect
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")

    news_title = soup.find_all('div', class_='content_title')[0].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text


    browser.visit('https://spaceimages-mars.com/')
    browser.find_by_css("button.btn")[0].click()
    feature_image_url = browser.find_by_css("img.fancybox-image")[0]["src"]
    
    
    # pandas scrape

    url = 'https://galaxyfacts-mars.com/'

    table = pd.read_html(url)
    table = pd.DataFrame(table[0])
    html_table = table.to_html(classes=["table", "table-dark", "table-responsive"])


    url = 'https://marshemispheres.com/'

    browser.visit(url)
    num_thumbs = len(browser.find_by_css("img.thumb"))
    
    browser.find_by_css("img.thumb")
    hemispheres = []

    for i in range(num_thumbs):
        browser.find_by_css("img.thumb")[i].click()
        img_url = browser.find_by_text("Sample")[0]["href"]
        title = browser.find_by_css("h2.title")[0].text
        hemispheres.append({
            "img_url":img_url,
            "title": title
        })
        browser.back()
    
    browser.quit()

    return {
        "news_p": news_p,
        "news_title": news_title,
        "featured_image": feature_image_url,
        "html_table": html_table,
        "hemispheres":hemispheres
    }

if __name__ == "__main__":
    print(scrape())