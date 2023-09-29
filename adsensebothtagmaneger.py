import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# Function to extract AdSense and GTM IDs from a URL
def extract_adsense_and_gtm_ids(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Initialize variables to store AdSense and GTM IDs
        adsense_id = None
        gtm_id = None

        # Search for the AdSense client ID pattern
        adsense_script = soup.find('script', {'src': re.compile(r'https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js.*')})
        if adsense_script:
            # Extract the client ID using regular expressions
            match = re.search(r'client=(ca-pub-\d+)', adsense_script['src'])
            if match:
                adsense_id = match.group(1)

        # Search for the Google Tag Manager ID pattern
        gtm_script = soup.find('script', {'src': re.compile(r'https://www\.googletagmanager\.com/gtag/js\?id=UA-\d+-\d+')})
        if gtm_script:
            # Extract the GTM ID using regular expressions
            match = re.search(r'id=UA-(\d+-\d+)', gtm_script['src'])
            if match:
                gtm_id = match.group(1)

        return adsense_id, gtm_id

    except Exception as e:
        return None, None

# Streamlit app
st.title("AdSense and GTM ID Extractor")

# User input: URL
url = st.text_input("Enter the URL of the website:")
if st.button("Extract IDs"):
    if url:
        adsense_id, gtm_id = extract_adsense_and_gtm_ids(url)

        if adsense_id:
            st.write(f"The AdSense client ID for the website is: {adsense_id}")
        else:
            st.write("AdSense ID not found on the website.")

        if gtm_id:
            st.write(f"The Google Tag Manager ID for the website is: UA-{gtm_id}")
        else:
            st.write("Google Tag Manager ID not found on the website.")
    else:
        st.warning("Please enter a URL.")

# Provide an example URL
st.sidebar.markdown("### Example URL")
st.sidebar.text("https://example.com/")

# Optional: Add more instructions or explanations here

