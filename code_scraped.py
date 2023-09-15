import streamlit as st
import requests
from bs4 import BeautifulSoup

# Define a function to scrape and display facility information
def scrape_facility_info(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find all divs with class "city_browse_con_total"
        facility_divs = soup.find_all("div", class_="city_browse_con_total")
        
        if facility_divs:
            # Loop through each facility div and extract information
            for facility_div in facility_divs:
                facility_name = facility_div.find("h3").text.strip()
                facility_address = facility_div.find_all("p")[1].text.strip()
                facility_county = facility_div.find_all("p")[2].text.strip()
                capacity = facility_div.find_all("p")[3].text.strip()
                phone_number = facility_div.find("p", class_="citcontph").text.strip()

                # Display the extracted information for each facility
                st.write("Facility Name:", facility_name)
                st.write("Address:", facility_address)
                st.write("County:", facility_county)
                st.write("Capacity:", capacity)
                st.write("Phone Number:", phone_number)
                st.write("-" * 30)  # Separator between facilities
        else:
            st.write("Facility information not found on the page.")
    else:
        st.write("Failed to retrieve the web page. Status code:", response.status_code)

# Streamlit app
st.title("Senior Facility Scraper")

# Input field for entering the URL
url_input = st.text_input("Enter the URL of the website:")

# Button to trigger the scraping process
if st.button("Scrape Facility Information"):
    if url_input:
        scrape_facility_info(url_input)
    else:
        st.write("Please enter a valid URL.")

