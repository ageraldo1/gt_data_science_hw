from bs4 import BeautifulSoup
from splinter import Browser
from urllib.parse import urlparse
import requests
import pandas as pd

executable_path = {'executable_path': '../resources/webdrivers/chromedriver.exe'}
driver_name = 'chrome'

def scrape_mars_news():

    mars_news = []
    url = 'https://mars.nasa.gov/news/'
    has_found = False

    try:        
        with Browser(driver_name, **executable_path, headless=True) as browser:
            browser.visit(url)
            response = browser.html
        
            soup = BeautifulSoup(response, 'html.parser')
            nasa_news = soup.body.find_all('li', class_='slide')

            for item in nasa_news:
                has_found = True
                news_title = item.find('div', class_='content_title').get_text()
                news_p = item.find('div', class_='article_teaser_body').get_text()

                mars_news.append({'news_title' : news_title, 'news_p': news_p})

            if has_found == False:
                with open ('debug_html.txt') as f:
                    f.write(response)

                    print ("debug file created")
                                   
    except Exception as e:
        mars_news.append({'error' : f'Error scraping url : {url}', 'details' : e})

    return mars_news

def scrape_jpl_mars_images():
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    featured_image = {}

    try:
        with Browser(driver_name, **executable_path, headless=True) as browser:
            browser.visit(url)
            response = browser.html
        
            soup = BeautifulSoup(response, 'html.parser')
        
            parsed_url = urlparse(url)
            image_path = soup.body.find('div', class_='carousel_container').find('a').get('data-fancybox-href')
            featured_image_url  = parsed_url.scheme + '://' + parsed_url.netloc + image_path
                    
            featured_image = {'featured_image_url' : featured_image_url} 

    except Exception as e:
        featured_image = {'error' : f'Error scraping url : {url}', 'details' : e}
    
    return featured_image

def scrape_mars_weather():
    url = 'https://twitter.com/marswxreport?lang=en'

    tweet = {}

    try:
        with Browser(driver_name, **executable_path, headless=True) as browser:
            browser.visit(url)
            response = browser.html
            
            soup = BeautifulSoup(response, 'html.parser')
            tweet_elem = soup.body.find('div', class_='js-tweet-text-container').find('p')
            tweet_elem.a.decompose()
            
            mars_weather = tweet_elem.get_text().replace('\n','')
            
            tweet = {'mars_weather' : mars_weather}

    except Exception as e:
        tweet = {'error' : f'Error scraping url : {url}', 'details' : e}        

    return tweet

def scrape_mars_facts():
    url = 'https://space-facts.com/mars/'

    html_table = {}

    try:
        mars_df = pd.read_html(url)[0]
        mars_df.columns = ['Description','Value']

        html_table = {'table_content' : mars_df.to_html(index=False)}

    except Exception as e:
        html_table = {'error' : f'Error scraping url : {url}', 'details' : e}

    return html_table

def scrape_mars_hemispheres():
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    parsed_url = urlparse(url)
    base_url = parsed_url.scheme + '://' + parsed_url.netloc

    hemisphere_image_urls = []

    try:
        with Browser(driver_name, **executable_path, headless=True) as browser:
            browser.visit(url)
            response = browser.html
            soup = BeautifulSoup(response, 'html.parser')

            for item in soup.body.find('div', class_='collapsible results').find_all('div', class_='item'):
                with Browser(driver_name, **executable_path, headless=True) as b:
                    b.visit(base_url + item.a.get('href'))
                    img_soup = BeautifulSoup(b.html, 'html.parser')
                    
                    title = img_soup.body.find('h2', class_='title').get_text()
                    img = base_url + img_soup.body.find('img', class_='wide-image').get('src')
                    
                    hemisphere_image_urls.append({ 'title' : title, 'img_url' : img})

    except Exception as e:
        hemisphere_image_urls.append({'error' : f'Error scraping url : {url}', 'details' : e})
                
    return hemisphere_image_urls

def scrape():
    return { 'mars_news' : scrape_mars_news(),
             'jpl_mars_images' : scrape_jpl_mars_images(),
             'mars_weather' : scrape_mars_weather(),
             'mars_facts' : scrape_mars_facts(),
             'mars_hemispheres' : scrape_mars_hemispheres()
            }