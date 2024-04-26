import requests
import os
from dotenv import load_dotenv

load_dotenv()

AUTHORIZATION_TOKEN = os.getenv('AUTHORIZATION_TOKEN')

def fetch_auctions(auth_token):
    url = "https://eu.api.blizzard.com/data/wow/connected-realm/5828/auctions/2"
    params = {
        "namespace": "dynamic-classic1x-eu",
        "locale": "en_US"
    }
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json() 
    else:
        return f"Failed to fetch data: {response.status_code}"

def find_auctions_by_item_id(auctions_data, item_id):
    matching_auctions = []
    for auction in auctions_data.get('auctions', []):
        if auction['item']['id'] == item_id and (auction['buyout'] / auction['quantity'])  < 50000:
        # if auction['item']['id'] == item_id :
            matching_auctions.append(auction)
    matching_auctionz = sorted(matching_auctions, key=lambda x: x['buyout'])
    return matching_auctions

def sum_bids_for_item(auctions):
    total_bid = sum(auction['buyout'] for auction in auctions)
    return total_bid

auth_token = AUTHORIZATION_TOKEN
data = fetch_auctions(auth_token)

if isinstance(data, dict): 
    item_id = 16204 
    matching_auctions = find_auctions_by_item_id(data, item_id)
    if matching_auctions:
        total_bid_amount = sum_bids_for_item(matching_auctions)
        print(f"Total buyout amount for item ID {item_id} (gold): {total_bid_amount / 10000}")
    else:
        print(f"No auctions found for item ID {item_id}.")
else:
    print(data)
