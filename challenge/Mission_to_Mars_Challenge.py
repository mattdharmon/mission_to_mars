# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# %%
# # Path to chromedriver MAC ONLY
# !which chromedriver


# %%
# Set the executable path and initialize the chrome browser in splinter
# be sure to set YOUR path
executable_path = {'executable_path': '/usr/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=True)

# %% [markdown]
# ### Visit the NASA Mars News Site

# %%
# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# %%
# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')


# %%
slide_elem.find("div", class_='content_title')


# %%
# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# %%
# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

# %% [markdown]
# ### JPL Space Images Featured Image

# %%
# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# %%
# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# %%
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# %%
# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# %%
# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url

# %% [markdown]
# ### Mars Facts

# %%
df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()


# %%
df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df


# %%
df.to_html()

# %% [markdown]
# ### Mars Weather

# %%
# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# %%
# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# %%
# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())

# %% [markdown]
# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# %% [markdown]
# ### Hemispheres

# %%
# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# %%
# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
image_soup = soup(html, 'html.parser')
items = image_soup.find_all("div", class_="description")
for item in items:
    img = {}
    link = item.find('a', ).get('href')
    browser.visit(f"https://astrogeology.usgs.gov{link}")
    temp_soup = soup(browser.html, 'html.parser')
    img['img_url'] = temp_soup.find('div', class_='downloads').find('a').get('href')
    img['title'] = image_soup.find('h3').get_text()
    hemisphere_image_urls.append(img)


# %%
# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# %%
# 5. Quit the browser
browser.quit()


# %%



