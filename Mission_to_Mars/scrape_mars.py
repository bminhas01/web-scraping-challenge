# Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped - NASA Mars News
    url_news = 'https://mars.nasa.gov/news/'
    browser.visit(url_news)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    time.sleep(10)

    # Save results that meet criteria in a variable
    results = news_soup.find_all('li', class_='slide')[0]

    # Identify and return latest news title and information
    news_title = results.find('div', class_="content_title").text
    news_p = results.find('div', class_="article_teaser_body").text

    # URL of page to be scraped - JPL Mars Space Images
    url_space_img = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url_space_img)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    space_img_soup = BeautifulSoup(html, 'html.parser')

    # Find desired data from soup
    image_src = space_img_soup.find(class_='headerimage fade-in')['src']

    # Edit website url to remove the path
    cropped_url = url_space_img.split('index')[0]

    # Create a new variable to hold path to the featured image
    featured_image_url = (f'{cropped_url}{image_src}')

    # URL of page to be scraped - Mars Facts webpage
    url_facts = 'https://space-facts.com/mars/'
    
    # Use read_html method to scrape tabular data from the page
    info_table = pd.read_html(url_facts)

    # Use indexing to retrieve only the required information
    info_df = info_table[0]
    info_df.rename(columns={0:'Attribute', 1: 'Value'}, inplace = True)

    # Generate a html table using the to_html method
    html_table = info_df.to_html(index = False)

    # Clean the html table by removing unwanted newlines
    info_html = html_table.replace('\n', '')

    # URL of page to be scraped - USGS Astrogeology webpage
    url_hemispheres = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemispheres)

    # Edit url to remove path
    modified_url = url_hemispheres.split('/search')[0]

    # Create a list of links to each hemisphere image
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    page_list = []
    count = 0

    # Create a loop to get information for each hemisphere by visiting the relevant pages - store information in a dictionary
    while count <=6:
        
        # Find a link to the page for the specific hemisphere
        page_link = soup.find_all('a', {'class':'itemLink product-item'})[count]['href']
        page_url = (f'{modified_url}{page_link}')
        page_list.append(page_url)
        count +=2
    
    # Find image_url and title for each hemisphere by visiting the page
    hemisphere_image_urls = []
    for page in page_list:
        hemisphere_info = {}
        browser.visit(page)
            
        # Create BeautifulSoup object; parse with 'html.parser'
        page_html = browser.html
        page_soup = BeautifulSoup(page_html, 'html.parser')
        
        # Find the link to the image and create a new variable to hold the complete path
        image_href = page_soup.find(class_='wide-image')['src']
        image_url = (f'{modified_url}{image_href}')

        # Find and save the title and image_url to the dictionary
        img_title = page_soup.find('h2', class_='title').text
        hemisphere_info ['title'] = img_title
        hemisphere_info ['img_url'] = image_url
        hemisphere_image_urls.append(hemisphere_info)

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        'info_html': info_html,
        'hemisphere_image_urls': hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data










