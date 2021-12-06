# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager


# Import Pandas
import pandas as pd
import time

# Set executable path
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Set up HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# Visit mars images URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# Facts Table

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


df.to_html()


# D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# HTML object
html = browser.html
# Parse HTML with Beautiful Soup
hemi_soup = soup(html, 'html.parser')
hemispheres = hemi_soup.find_all('div', class_='item')

# Set up splinter variable to iterate through
# hemi_links = browser.find_by_tag('h3').links.find_by_partial_text('Enhanced')
# print(hemi_links)

for hemisphere in hemispheres:
    # Get link for the hemisphere page
    hemi_link = hemisphere.find('a')
    hemi_href = hemi_link.get('href')
    hemi_title = hemisphere.find('h3').get_text()
    # Open browser for each hemisphere
    browser.visit(f'https://marshemispheres.com/' + hemi_href)
    time.sleep(2)
    # Scrape images
    hemisphere_image_src = hemi_soup.find_all('img')[4]['src']
    # Add scraped image url to the parent
    hemisphere_image_url = f'https://marshemispheres.com/{hemisphere_image_src}'
    print(hemisphere_image_url)
    print(hemi_title)
    # Add images and titles to a dictionary
    hemi_dict = {'image_url':hemisphere_image_url, 'title':hemi_title}
    # Add dictionaries to the hemisphere_image_urls
    hemisphere_image_urls.append(hemi_dict)
    # Go to previous page
    browser.back()



# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()

