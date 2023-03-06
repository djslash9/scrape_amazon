import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import time
from urllib.parse import urlparse

# Function to extract Product Title
def get_title(soup):

    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id":'productTitle'})
        
        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string

# Function to extract Product Price
def get_price(soup):

    try:
        price = soup.find("span", attrs={'id':'priceblock_ourprice'}).string.strip()

    except AttributeError:

        try:
            # If there is some deal price
            price = soup.find(attrs={"class":'a-section a-spacing-micro'}).find("span", attrs={"class": "a-offscreen"}).text

        except:
            price = ""

    return price

# Function to extract Product Rating
def get_rating(soup):

    try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
    
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""	

    return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""	

    return review_count

# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id':'availability'})
        available = available.find("span").string.strip()

    except AttributeError:
        available = "Not Available"	

    return available

def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

if __name__ == '__main__':

    # Title of the app
    st.header("Scrape the Amazon.com for product details")

    amazon_url = st.text_input('Copy & Paste the complete amazon.com url from the browser, And press enter')

    # Parse the input and check if it has a valid scheme
    parsed_url = urlparse(amazon_url)
    if not parsed_url.scheme:
        st.write("Please enter a valid URL")
    elif parsed_url.scheme not in ['http', 'https']:
        st.write("Only HTTP and HTTPS URLs are supported")
    else:
        st.write(f"You entered a valid URL: {amazon_url}")

        if amazon_url:

            with st.spinner('Scraping the website, Please wait, this will take some time ...'):

                # add your user agent 
                HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

                # The webpage URL
                # URL = "https://www.amazon.com/s?k=fitbit+inspire+2&crid=9XJAU0T9P5V6&sprefix=fitbit+inspire+2%2Caps%2C589&ref=nb_sb_noss_1"
                URL = amazon_url
                # HTTP Request
                webpage = requests.get(URL, headers=HEADERS)

                # Soup Object containing all data
                soup = BeautifulSoup(webpage.content, "html.parser")

                # Fetch links as List of Tag Objects
                links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})

                # Store the links
                links_list = []

                # Loop for extracting links from Tag Objects
                for link in links:
                        links_list.append(link.get('href'))

                d = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[]}
                
                # Loop for extracting product details from each link 
                for link in links_list:
                    new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)

                    new_soup = BeautifulSoup(new_webpage.content, "html.parser")

                    # Function calls to display all necessary product information
                    d['title'].append(get_title(new_soup))
                    d['price'].append(get_price(new_soup))
                    d['rating'].append(get_rating(new_soup))
                    d['reviews'].append(get_review_count(new_soup))
                    d['availability'].append(get_availability(new_soup))

            
                amazon_df = pd.DataFrame.from_dict(d)
                amazon_df['title'].replace('', np.nan, inplace=True)
                amazon_df = amazon_df.dropna(subset=['title'])
                #amazon_df.to_csv("amazon_data.csv", header=True, index=False)

                # Display the dataframe
                st.dataframe(amazon_df)

            # Add a button to download the dataframe as a CSV file
            csv = convert_df(amazon_df)

            st.download_button("Press to Download",csv, "amazon_data.csv", "text/csv", key='download-csv')
    
    hide_streamlit_style = """
            <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    st.markdown('-----')
    st.write("(c) testing program by djslash9 - 03.06.2023")
