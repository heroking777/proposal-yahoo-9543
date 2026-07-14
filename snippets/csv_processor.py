import csv
import requests
from datetime import datetime

# Define the URL for the Yahoo!オークション API
API_URL = "https://api.auction.yahoo.co.jp/AuctionWebService/V1/getAuctionResultList"

# Define your API key and secret
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"

# Define the headers for the API request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}:{API_SECRET}"
}

# Define the parameters for the API request
params = {
    "auctionId": "123456789",  # Replace with your auction ID
    "startDate": "2023-01-01",
    "endDate": "2023-12-31"
}

# Make the API request to get the auction result list
response = requests.get(API_URL, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    
    # Extract the auction results
    auction_results = data["auctionResultList"]["item"]
    
    # Define the CSV file name
    csv_file_name = "auction_results.csv"
    
    # Open the CSV file for writing
    with open(csv_file_name, mode="w", newline="", encoding="utf-8") as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)
        
        # Write the header row to the CSV file
        csv_writer.writerow(["Auction ID", "Item ID", "Seller ID", "Bidder ID", "Bid Amount", "Bid Date"])
        
        # Write the auction results to the CSV file
        for result in auction_results:
            csv_writer.writerow([
                result["auctionId"],
                result["itemId"],
                result["sellerId"],
                result["bidderId"],
                result["bidAmount"],
                datetime.strptime(result["bidDate"], "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
            ])
    
    print(f"Auction results saved to {csv_file_name}")
else:
    print(f"Failed to retrieve auction results. Status code: {response.status_code}")