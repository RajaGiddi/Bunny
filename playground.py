import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import base64

st.title("Web Scraping and DataFrame Viewer")

url = st.text_input("Enter the URL:", "https://www.seniorguidance.org/assisted-living/maryland/aberdeen.html")

if st.button("Scrape Data"):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        facility_divs = soup.find_all("div", class_="city_browse_con_total")

        if facility_divs:
            facility_data = []

            for facility_div in facility_divs:
                h3_tag = facility_div.find("h3")
                facility_info = {}
                facility_info["Facility Name"] = h3_tag.text.strip()
                facility_info["Address"] = facility_div.find_all("p")[0].text.strip()
                facility_info["County"] = facility_div.find_all("p")[1].text.strip()

                # Extract the capacity and remove the "Capacity:" prefix
                capacity_text = facility_div.find_all("p")[2].text.strip()
                facility_info["Capacity"] = capacity_text.replace("Capacity:", "").strip()

                facility_info["Phone Number"] = facility_div.find("p", class_="citcontph").text.strip()

                # Extract the image alt attribute
                img_tag = facility_div.find("img")
                if img_tag:
                    facility_info["Image Alt"] = img_tag.get("alt")
                else:
                    facility_info["Image Alt"] = ""

                facility_data.append(facility_info)

            df = pd.DataFrame(facility_data)

            # Display the DataFrame in the Streamlit app
            st.dataframe(df)

            # Create a link to download the CSV file
            csv_data = df.to_csv(index=False)
            b64 = base64.b64encode(csv_data.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="facility_data.csv">Download CSV</a>'
            st.markdown(href, unsafe_allow_html=True)
        else:
            st.error("Facility information not found on the page.")
    else:
        st.error(f"Failed to retrieve the web page. Status code: {response.status_code}")
