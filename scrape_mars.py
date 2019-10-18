# %%
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time

# %%
def init_browser():
  executable_path = {"executable_path": "chromedriver.exe"}
  return Browser("chrome", **executable_path, headless=False)


def scrape_data():
  browser = init_browser()

  #NASA Mars News
  url = "https://mars.nasa.gov/news/"
  browser.visit(url)
  time.sleep(2)

  html = browser.html
  soup = BeautifulSoup(html, "html.parser")

  news_title = soup.find("div", class_="content_title").find("a").text
  news_p = soup.find("div", class_="article_teaser_body").text
      
  # print(news_title)
  # print(news_p)


  # %%
  #JPL Mars Space Images - Featured Image
  mars_images = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
  img_url = "https://www.jpl.nasa.gov"
  browser.visit(mars_images)

  html = browser.html

  soup = BeautifulSoup(html, "html.parser")

  # %%
  featured_image = soup.find("img", class_="thumb")["src"]
  # print(featured_image)

  # %%
  featured_image_url = img_url + featured_image

  # %%
  # print(featured_image_url)

  # %%
  #Mars Weather
  mw_twitter = "https://twitter.com/marswxreport?lang=en"
  browser.visit(mw_twitter)

  html = browser.html

  soup = BeautifulSoup(html, "html.parser")

  # %%
  mars_weather = soup.find("div", class_="js-tweet-text-container").text.strip()
  # mars_weather

  # %%
  #Mars Facts
  mars_facts_url = "https://space-facts.com/mars/"
  browser.visit(mars_facts_url)

  html = browser.html

  soup = BeautifulSoup(html, "html.parser")

  # %%
  table = pd.read_html(mars_facts_url)
  # table

  # %%
  mars_facts = table[0]
  mars_df = pd.DataFrame(mars_facts)
  # mars_df

  # %%
  del mars_df["Earth"]
  # mars_df

  # %%
  mars_html_table = mars_df.to_html()
  # mars_html_table

  # %%
  #Mars Hemisphere
  base_hemisphere_url = "https://astrogeology.usgs.gov"
  hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
  browser.visit(hemisphere_url)

  html = browser.html

  soup = BeautifulSoup(html, "html.parser")

  # %%
  hemispheres = []

  results = soup.find_all("div", class_="item")

  # %%
  print('Start results loop')
  for result in results:
      title = result.find("h3").text
      link = result.find('a')
      # Get sample image from page
      print(base_hemisphere_url + link['href'])
      browser.visit(base_hemisphere_url + link['href'])
      page_html = browser.html
      soup = BeautifulSoup(page_html, "html.parser")
      hemispheres.append({"title": title, "img_url": soup.find("div", class_="downloads").find('a')['href']})

  # %%
  # hemispheres


  mars_data = {
    "news_title": news_title,
    "news_p": news_p,
    "mars_images": mars_images,
    "featured_image_url": featured_image_url,
    "mars_weather": mars_weather,
    "mars_html_table": mars_html_table,
    "hemispheres": hemispheres
  }

  # print(mars_data)
  return mars_data
