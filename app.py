import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
# import time
import datetime
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
    now = datetime.datetime.now()
    st.write(now)

    # amazon_url = st.text_input('Copy & Paste the complete amazon.com url from the browser, And press enter')
    url1 = "https://www.amazon.com/s?k=Galaxy+Watch4+40mm+BLK+WiFi&crid=3G7NA8NLDS2HM&sprefix=galaxy+watch4+40mm+blk+wifi%2Caps%2C289&ref=nb_sb_noss"
    url2 = "https://www.amazon.com/s?k=Galaxy+Watch4+40mm+BLK+Cellular&crid=168J5HMA65GND&sprefix=galaxy+watch4+40mm+blk+cellular%2Caps%2C295&ref=nb_sb_noss"
    url3 = "https://www.amazon.com/s?k=Galaxy+Watch4+44mm+BLK+WiFI&crid=1NPN9URTX7M3L&sprefix=galaxy+watch4+44mm+blk+wifi%2Caps%2C295&ref=nb_sb_noss"
    url4 = "https://www.amazon.com/s?k=Galaxy+Watch4+44mm+BLK+Cellular&crid=3QTYCEHPISHN3&sprefix=galaxy+watch4+44mm+blk+cellular%2Caps%2C291&ref=nb_sb_noss"
    url5 = "https://www.amazon.com/s?k=Apple+Watch+SE+40mm+GPS+Starlight+Aluminum+Sport+Band+M+L&crid=2ZSAJCIFSFFGB&sprefix=apple+watch+se+40mm+gps+starlight+aluminum+sport+band+m+l%2Caps%2C288&ref=nb_sb_noss"
    url6 = "https://www.amazon.com/s?k=Apple+Watch+SE+44mm+GPS+Midnight+Aluminum+Sport+Band+S+M&crid=3AI82WFWKSUIY&sprefix=apple+watch+se+44mm+gps+midnight+aluminum+sport+band+s+m%2Caps%2C298&ref=nb_sb_noss"
    url7 = "https://www.amazon.com/s?k=Apple+Watch+SE+40mm+GPS+Cellular+Starlight+Aluminum+Sport+Band+M+L&crid=G5A7JICFJGMD&sprefix=apple+watch+se+40mm+gps+cellular+starlight+aluminum+sport+band+m+l%2Caps%2C298&ref=nb_sb_noss"
    url8 = "https://www.amazon.com/s?k=Apple+Watch+SE+44mm+GPS+Cellular+Midnight+Aluminum+Sport+Band+S+M&crid=3EQJY8IJ7G5MV&sprefix=apple+watch+se+44mm+gps+cellular+midnight+aluminum+sport+band+s+m%2Caps%2C299&ref=nb_sb_noss"
    url9 = "https://www.amazon.com/s?k=Apple+Watch+Series+8+GPS+41mm+Starlight+Aluminum+Sport+Band+M+L&crid=2I7YJKP56O07J&sprefix=apple+watch+series+8+gps+41mm+starlight+aluminum+sport+band+m+l%2Caps%2C305&ref=nb_sb_noss"
    url10 = "https://www.amazon.com/s?k=Apple+Watch+Series+8+GPS+45mm+Midnight+Aluminum+Sport+Band+S+M&crid=2CKL4AR9XSOQS&sprefix=apple+watch+series+8+gps+45mm+midnight+aluminum+sport+band+s+m%2Caps%2C289&ref=nb_sb_noss"
    url11 = "https://www.amazon.com/s?k=Apple+Watch+Series+8+GPS+Cellular+41mm+Midnight+Aluminum+Sport+Band+M+L&crid=1DH26VN7JQE37&sprefix=apple+watch+series+8+gps+cellular+41mm+midnight+aluminum+sport+band+m+l%2Caps%2C293&ref=nb_sb_noss"
    url12 = "https://www.amazon.com/s?k=Apple+Watch+Series+8+GPS+Cellular+45mm+Midnight+Aluminum+Sports+Band+M+L&crid=177XM9XEKKBIY&sprefix=apple+watch+series+8+gps+cellular+45mm+midnight+aluminum+sports+band+m+l%2Caps%2C305&ref=nb_sb_noss"
    url13 = "https://www.amazon.com/s?k=AirPods+with+charging+case+%282nd+Gen%29&crid=3P63RN8MBXFPP&sprefix=airpods+with+charging+case+2nd+gen+%2Caps%2C376&ref=nb_sb_noss_2"
    url14 = "https://www.amazon.com/s?k=AirPods+Wireless+charging+case+3rd+Gen&crid=2CXBMS7AOR3O&sprefix=airpods+wireless+charging+case+3rd+gen%2Caps%2C643&ref=nb_sb_noss_2"
    url15 = "https://www.amazon.com/s?k=AirPods+Pro+2nd+Gen&crid=2US1DZ5YEY6CS&sprefix=airpods+pro+2nd+gen%2Caps%2C303&ref=nb_sb_noss_1"
    url16 = "https://www.amazon.com/s?k=Fitbit+Inspire+3+Midnight+Zen+Black&crid=SPQ0MGXFY565&sprefix=fitbit+inspire+3+midnight+zen+black%2Caps%2C327&ref=nb_sb_noss_2"
    url17 = "https://www.amazon.com/s?k=Fitbit+Versa+4+Black&crid=35OLY2ZNYKAER&sprefix=fitbit+versa+4+black%2Caps%2C324&ref=nb_sb_noss_1"
    url18 = "https://www.amazon.com/s?k=Fitbit+Sense+2+Gray&crid=O9CTIJJ83R21&sprefix=fitbit+sense+2+gray%2Caps%2C301&ref=nb_sb_noss_2"
    url19 = "https://www.amazon.com/s?k=Fitbit+Versa+2+Black&crid=K1UBZ8CLXB87&sprefix=fitbit+versa+2+black%2Caps%2C315&ref=nb_sb_noss_1"





    url = st.radio("Select the product", (
        "Galaxy Watch4 40mm BLK WiFi",
        "Galaxy Watch4 40mm BLK Cellular",
        "Galaxy Watch4 44mm BLK WiFI",
        "Galaxy Watch4 44mm BLK Cellular",
        "Apple Watch SE 40mm GPS Starlight/Aluminum Sport Band M/L",
        "Apple Watch SE 44mm GPS Midnight/Aluminum Sport Band S/M",
        "Apple Watch SE 40mm GPS + Cellular Starlight/Aluminum Sport Band M/L",
        "Apple Watch SE 44mm GPS + Cellular Midnight/Aluminum Sport Band S/M",
        "Apple Watch Series 8 GPS 41mm Starlight/Aluminum Sport Band M/L",
        "Apple Watch Series 8 GPS 45mm Midnight/Aluminum Sport Band S/M",
        "Apple Watch Series 8 GPS + Cellular 41mm Midnight/Aluminum Sport Band M/L",
        "Apple Watch Series 8 GPS + Cellular 45mm Midnight/Aluminum Sports Band M/L",
        "AirPods with charging case (2nd Gen)",
        "AirPods Wireless charging case (3rd Gen)",
        "AirPods Pro (2nd Gen)",
        "Fitbit Inspire 3 Midnight Zen Black",
        "Fitbit Versa 4 Black",
        "Fitbit Sense 2 Gray",
        "Fitbit Versa 2 Black"
        )
    )

    if url == "Galaxy Watch4 40mm BLK WiFi":
        amazon_url = url1
    elif url == "Galaxy Watch4 40mm BLK Cellular":
        amazon_url = url2
    elif url == "Galaxy Watch4 44mm BLK WiFI":
        amazon_url = url3
    elif url == "Galaxy Watch4 44mm BLK Cellular":
        amazon_url = url4
    elif url == "Apple Watch SE 40mm GPS Starlight/Aluminum Sport Band M/L":
        amazon_url = url5
    elif url == "Apple Watch SE 44mm GPS Midnight/Aluminum Sport Band S/M":
        amazon_url = url6
    elif url == "Apple Watch SE 40mm GPS + Cellular Starlight/Aluminum Sport Band M/L":
        amazon_url = url7
    elif url == "Apple Watch SE 44mm GPS + Cellular Midnight/Aluminum Sport Band S/M":
        amazon_url = url8
    elif url == "Apple Watch Series 8 GPS 41mm Starlight/Aluminum Sport Band M/L":
        amazon_url = url9
    elif url == "Apple Watch Series 8 GPS 45mm Midnight/Aluminum Sport Band S/M":
        amazon_url = url10
    elif url == "Apple Watch Series 8 GPS + Cellular 41mm Midnight/Aluminum Sport Band M/L":
        amazon_url = url11
    elif url == "Apple Watch Series 8 GPS + Cellular 45mm Midnight/Aluminum Sports Band M/L":
        amazon_url = url12
    if url == "AirPods with charging case (2nd Gen)":
        amazon_url = url13
    elif url == "AirPods Wireless charging case (3rd Gen)":
        amazon_url = url14
    elif url == "AirPods Pro (2nd Gen)":
        amazon_url = url15
    elif url == "Fitbit Inspire 3 Midnight Zen Black":
        amazon_url = url16
    elif url == "Fitbit Versa 4 Black":
        amazon_url = url17
    elif url == "Fitbit Sense 2 Gray":
        amazon_url = url18
    else:
        amazon_url = url19

    
    if st.button('Search Amazon'):

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

            d = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[], "date":[]}
                
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
                d['date'].append(now)

            
            amazon_df = pd.DataFrame.from_dict(d)
            amazon_df['title'].replace('', np.nan, inplace=True)
            amazon_df = amazon_df.dropna(subset=['title'])
            #amazon_df.to_csv("amazon_data.csv", header=True, index=False)

            # Display the dataframe
            st.dataframe(amazon_df)

        # Add a button to download the dataframe as a CSV file
        csv = convert_df(amazon_df)
        st.download_button("Press to Download",csv, "amazon_{}_{}.csv".format(url, now), "text/csv", key='download-csv')
    
    hide_streamlit_style = """
            <style>
                MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    st.markdown('-----')
    st.write("(c) testing program by djslash9 - 03.06.2023")