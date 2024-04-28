import requests
import os
from dotenv import load_dotenv

load_dotenv()

AUTHORIZATION_TOKEN = os.getenv(
    "AUTHORIZATION_TOKEN"
)  # Authorization token resets every 24 hours
ITEM_ID = 16204
MAX_COST_PER_ITEM = 50000  # Copper
FETCH_URL = "https://eu.api.blizzard.com/data/wow/connected-realm/5828/auctions/2"  # SOD Crusader Strike(EU) Alliance AH
FETCH_PARAMS = {"namespace": "dynamic-classic1x-eu", "locale": "en_US"}  # EU
FETCH_HEADERS = {"Authorization": f"Bearer {AUTHORIZATION_TOKEN}"}


def fetch_auctions():
    url = FETCH_URL
    params = FETCH_PARAMS
    headers = FETCH_HEADERS

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Failed to fetch data: {response.status_code}"


def find_auctions_by_item_id(auctions_data):
    matching_auctions = []
    for auction in auctions_data.get("auctions", []):
        if (
            auction["item"]["id"] == ITEM_ID
            and (auction["buyout"] / auction["quantity"]) < MAX_COST_PER_ITEM
        ):
            matching_auctions.append(auction)
    return matching_auctions


def sum_bids_for_item(auctions):
    total_bid = sum(auction["buyout"] for auction in auctions)
    return total_bid


data = fetch_auctions()

if isinstance(data, dict):
    matching_auctions = find_auctions_by_item_id(data)

    if matching_auctions:
        total_bid_amount = sum_bids_for_item(matching_auctions)
        print(
            f"Total buyout amount for item ID {ITEM_ID} (gold): {total_bid_amount / 10000}"
        )
    else:
        print(
            f"No auctions found for item ID {ITEM_ID} below {MAX_COST_PER_ITEM} copper."
        )
else:
    print(data)
