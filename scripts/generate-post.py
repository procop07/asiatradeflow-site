# scripts/generate-post.py
import json
import os
import requests

# Construct the path to products.json relative to the script's location
# GITHUB_WORKSPACE is the root of the repository in GitHub Actions
workspace = os.getenv('GITHUB_WORKSPACE', '.') # Default to current dir if not in Actions
file_path = os.path.join(workspace, 'products/products.json')

try:
    # Ensure UTF-8 encoding is used, as JSON files might contain non-ASCII characters
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: products.json not found at {file_path}")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {file_path}")
    exit(1)

if not data.get('products'):
    print("No products found in products.json. Cannot generate post.")
    # Exit cleanly if no products, as this might not be a failure
    # depending on desired workflow behavior.
    latest_product = {
        "name": "N/A",
        "price_thb": "N/A",
        "shipping_pallet": "N/A",
        "margin": "N/A"
    }
    # If no product, we might not want to "post" anything.
    # For now, it will print a post with N/A values.
else:
    latest_product = data['products'][-1]

# Using .get for safer access to dictionary keys
post_text = f'''
NEW FIND IN THAILAND (Emoji removed for compatibility)

Product: {latest_product.get('name', 'N/A')}
Price: {latest_product.get('price_thb', 'N/A')} THB
Logistics: ${latest_product.get('shipping_pallet', 'N/A')}
Margin: {latest_product.get('margin', 'N/A')}

Details: asiatradeflow.com

#AsiaTradeFlow #ThailandImport
'''

# Placeholder for actual API call to LinkedIn or other social media
print("Generated Post Content:")
print(post_text)

# Example for a LinkedIn API call (to be implemented by the user)
# linkedin_api_url = os.getenv("LINKEDIN_API_URL") # Store sensitive data as secrets
# linkedin_access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
#
# if linkedin_api_url and linkedin_access_token:
#     headers = {
#         "Authorization": f"Bearer {linkedin_access_token}",
#         "Content-Type": "application/json",
#         "X-Restli-Protocol-Version": "2.0.0" # Example header, check LinkedIn API docs
#     }
#     payload = {
#         "author": f"urn:li:person:{os.getenv('LINKEDIN_PERSON_URN')}", # URN of the author
#         "lifecycleState": "PUBLISHED",
#         "specificContent": {
#             "com.linkedin.ugc.ShareContent": {
#                 "shareCommentary": {
#                     "text": post_text
#                 },
#                 "shareMediaCategory": "NONE"
#             }
#         },
#         "visibility": {
#             "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
#         }
#     }
#     try:
#         response = requests.post(linkedin_api_url, json=payload, headers=headers)
#         response.raise_for_status()  # Raises an exception for 4XX/5XX errors
#         print("Successfully posted to LinkedIn.")
#     except requests.exceptions.RequestException as e:
#         print(f"Error posting to LinkedIn: {e}")
#         if response is not None:
#             print(f"Response status: {response.status_code}")
#             print(f"Response text: {response.text}")
#         # Decide if this should fail the workflow
#         # exit(1)
# else:
#     print("LinkedIn API URL or Access Token not configured. Skipping post.")
