import requests
from bs4 import BeautifulSoup
import barcode
from barcode.writer import ImageWriter

def get_auction_history(username, password):
    # Login to Yahoo!オークション and retrieve the auction history
    login_url = 'https://auctions.yahoo.co.jp/mypage/login'
    session = requests.Session()
    login_data = {
        'username': username,
        'password': password
    }
    response = session.post(login_url, data=login_data)
    
    if response.status_code == 200:
        history_url = 'https://auctions.yahoo.co.jp/mypage/history'
        history_response = session.get(history_url)
        
        if history_response.status_code == 200:
            soup = BeautifulSoup(history_response.text, 'html.parser')
            # Extract auction details from the HTML
            auctions = []
            for item in soup.find_all('div', class_='item'):
                title = item.find('a', class_='title').text.strip()
                price = item.find('span', class_='price').text.strip()
                auctions.append({'title': title, 'price': price})
            
            return auctions
        else:
            print("Failed to retrieve auction history")
    else:
        print("Login failed")

def generate_barcode(auction):
    # Generate a barcode for each auction item
    EAN = barcode.get('ean13')
    ean = EAN(auction['price'], writer=ImageWriter())
    filename = f"{auction['title'].replace(' ', '_')}.png"
    ean.save(filename)
    return filename

def save_receipts(auctions):
    # Save the auction history and barcodes as receipts
    with open('receipts.txt', 'w') as file:
        for auction in auctions:
            file.write(f"Title: {auction['title']}\n")
            file.write(f"Price: {auction['price']}\n")
            barcode_filename = generate_barcode(auction)
            file.write(f"Barcode saved as {barcode_filename}\n\n")

# Example usage
username = 'your_username'
password = 'your_password'
auctions = get_auction_history(username, password)
if auctions:
    save_receipts(auctions)
else:
    print("No auction history found")