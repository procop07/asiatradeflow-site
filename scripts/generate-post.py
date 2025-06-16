# scripts/generate-post.py
import json
import os
import requests

print("--- Starting generate-post.py ---")

workspace = os.getenv('GITHUB_WORKSPACE', '.')
file_path = os.path.join(workspace, 'products/products.json')
print(f"Constructed file path: {file_path}")

try:
    print(f"Attempting to open and read: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print("Successfully loaded products.json")
except FileNotFoundError:
    print(f"Error: products.json not found at {file_path}")
    exit(1)
except json.JSONDecodeError as e:
    print(f"Error: Could not decode JSON from {file_path}. Details: {e}")
    exit(1)
except Exception as e:
    print(f"An unexpected error occurred while reading or parsing products.json: {e}")
    exit(1)

latest_product = None
# Check if 'products' key exists and if it's a non-empty list
if data and 'products' in data and isinstance(data['products'], list) and len(data['products']) > 0:
    latest_product = data['products'][-1]
    print(f"Latest product identified: {latest_product.get('name', 'N/A')}")
else:
    print("No products found in products.json, or 'products' key is missing/empty.")
    # Script will continue and print a post with N/A values, rather than exiting.
    # If failing the workflow is desired here, uncomment exit(1)
    # exit(1)
    latest_product = {
        "name": "N/A (No products found or list empty)",
        "price_thb": "N/A",
        "price_usd": "N/A", // Added this for consistency
        "shipping_pallet": "N/A",
        "margin": "N/A",
        "origin": "N/A", // Added this for consistency
        "photo": "N/A" // Added this for consistency
    }
    print(f"Proceeding with N/A product data: {latest_product}")


# Using .get for safer access to dictionary keys
post_text = f'''
NEW FIND IN THAILAND (Emoji removed for compatibility)

Product: {latest_product.get('name', 'N/A')}
Price THB: {latest_product.get('price_thb_per_kg', latest_product.get('price_thb', 'N/A'))}
Price USD: {latest_product.get('price_usd_per_kg', latest_product.get('price_usd', 'N/A'))}
Logistics: ${latest_product.get('shipping_cost_per_pallet_usd', latest_product.get('shipping_pallet', 'N/A'))}
Margin: {latest_product.get('margin_percentage', latest_product.get('margin', 'N/A'))}
Origin: {latest_product.get('origin', 'N/A')}

Details: asiatradeflow.com

#AsiaTradeFlow #ThailandImport
'''
# Adjusted keys in post_text to match the detailed structure in products.json if available,
# falling back to simpler keys for compatibility with the N/A structure.

print("--- Generated Post Content: ---")
print(post_text)
print("-------------------------------")

# Placeholder for actual API call to LinkedIn or other social media
linkedin_api_url = os.getenv("LINKEDIN_API_URL")
linkedin_access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
linkedin_person_urn = os.getenv("LINKEDIN_PERSON_URN")

if linkedin_api_url and linkedin_access_token and linkedin_person_urn:
    print("LinkedIn API credentials found. Attempting to post...")
    headers = {
        "Authorization": f"Bearer {linkedin_access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    payload = {
        "author": f"urn:li:person:{linkedin_person_urn}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": post_text
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    try:
        response = requests.post(linkedin_api_url, json=payload, headers=headers)
        response.raise_for_status()
        print("Successfully posted to LinkedIn.")
    except requests.exceptions.RequestException as e:
        print(f"Error posting to LinkedIn: {e}")
        if response is not None:
            print(f"Response status: {response.status_code}")
            print(f"Response text: {response.text}")
        print("Workflow will NOT fail due to LinkedIn posting error based on current script logic.")
        # If workflow should fail on post error, uncomment:
        # exit(1)
else:
    print("LinkedIn API URL, Access Token, or Person URN not configured in secrets. Skipping actual post.")

print("--- generate-post.py finished successfully ---")
