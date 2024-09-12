import requests
from bs4 import BeautifulSoup

# Define the URL of the webpage
last_notice = "a"
url = 'https://www.dtu.ac.in/'
def fetch_notices():
    global last_notice
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful
        response.raise_for_status()

        # Parse the content of the request
        soup = BeautifulSoup(response.content, 'html.parser')
        div_tab4 = soup.find('div', id='tab4')
        latest_tab_divs = div_tab4.find('a')
        # Find the div with the class 'latest_tab'
        text = latest_tab_divs.get_text(strip=True)
        print(text)
        print(last_notice) 
        if (text!=last_notice):
            last_notice = text
            print(last_notice)
            print(text)
            lin = latest_tab_divs['href']
            pdf_link = f'{text} \n https://www.dtu.ac.in/{lin[1:]}'
            print(last_notice)
            return pdf_link
        

    except requests.exceptions.RequestException as e:
        return(f"Failed to retrieve the webpage: {e}")
# Call the function to fetch and print notices
