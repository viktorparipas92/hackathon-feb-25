from datetime import timedelta

from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster, QueryOptions
from couchbase.exceptions import CouchbaseException
from couchbase.options import ClusterOptions
import getpass


COUCHBASE_CONNECTION_STRING = 'couchbases://cb.vjrdlbmc3no71q9.cloud.couchbase.com'
DB_USERNAME = 'general-access'
# DB_PASSWORD = getpass.getpass(f'Password for {DB_USERNAME}')
# read password from assets/cb_pass.txt
with open('../assets/cb_pass.txt', 'r') as f:
    DB_PASSWORD = f.read().strip()

BUCKET_NAME = 'travel-sample'
SCOPE_NAME = '_default'
COLLECTION_NAME = 'footway'
SEARCH_INDEX_NAME = 'footway-incoming-email'

auth = PasswordAuthenticator(DB_USERNAME, DB_PASSWORD)
options = ClusterOptions(auth)
cluster = Cluster(COUCHBASE_CONNECTION_STRING, options)
cluster.wait_until_ready(timedelta(seconds=5))
assert cluster.connected
# print(cluster.connected)

bucket = cluster.bucket(BUCKET_NAME)
scope = bucket.scope(SCOPE_NAME)
collection = scope.collection(COLLECTION_NAME)


# # Sample query to fetch a document
# document_id = '000983b6-a898-481a-ae83-cf8db80e89cb'
# try:
#     result = collection.get(document_id)
#     print(result.content_as[dict])
# except CouchbaseException as e:
#     print(f"Query failed: {e}")
    
# # Fetch all unique categories
# query = f"SELECT category FROM `{BUCKET_NAME}`.`{SCOPE_NAME}`.`{COLLECTION_NAME}`"
# try:
#     result = cluster.query(query, QueryOptions(timeout=timedelta(seconds=75)))
#     categories = set()
#     for row in result:
#         categories.add(row['category'])
#     print("Unique Categories:", list(categories)) # total 952
# except CouchbaseException as e:
#     print(f"Query failed: {e}")  

Unique_Categories = ['RETURN', 'NO_PROOF', 'PROFORMA_INVOICE', 'OTHER', 'RECEIPT', 'STATUS_RETURN', 'UNSUBSCRIBE', 'EXCHANGE', 'CANCEL_REQUEST', 'CANCEL', 'PROOF_COMPLAINT', 'MISSING', 'WRONG_ADDRESS', 'SHIPPING', 'HOW_TO_RETURN', 'DISCOUNT_CODE', '3F2', 'WRONG_PRODUCT', 'COMPLAINT', 'PRODUCT', 'PRICE_MATCH', 'UNCLEAR_C_REQUEST', 'FW_SHIPPING_PROCESS', 'PRICE', 'STATUS_SHIPPING']
converted_cat_text = ', '.join(Unique_Categories)

categories= {
    "Software",
    "Damaged_Product",
    "Automotive",
    "Smart_Home",
   "Medical_Equipment"
}     

Questions = {
    "Software": "I can't log into my account—each time I try, I get an error message that I do not understand.",
    "Damaged_Product": "I just received my order, but the product seems to be damaged.",
    "Automotive": "My car’s dashboard suddenly lit up with a warning. I'm not sure what it means.",
    "Smart_Home": "My smart security camera isn't connecting to the network and shows an error message in the app.",
    "Medical_Equipment": "Our medical monitor has displayed an error code and isn’t functioning properly. This is urgent."
}

tmp_Initial_response = {
    "Software": "Thanks for reaching out. To help diagnose the issue, could you please attach a screenshot of the error message?",
    "Damaged_Product": "I'm sorry to hear that. Could you please attach a photo of the damaged product so we can assess the issue more closely?",
    "Automotive": "To better understand the situation, could you attach a photo of the dashboard showing the warning light?",
    "Smart_Home": "Could you please attach a screenshot of the error message from the app? This will help us determine the root cause.",
    "Medical_Equipment": "For clarity, could you attach an image of the monitor displaying the error code? That will help us quickly identify the problem."
}
tmp_Final_response = {
    "Software": "Looking at your screenshot, it appears that a network timeout might be causing the error. Please try clearing your browser cache and restarting your network connection. Let us know if the problem persists.",
    "Damaged_Product": "Thank you for the photo. It looks like the damage occurred during shipping. We apologize for the inconvenience. Please send us your order number, and we will arrange for a replacement or refund immediately.",
    "Automotive": "Thanks for the image. The warning light seems to indicate a coolant system issue. Please check your coolant levels immediately. If the light remains on, we recommend taking your car to a service center for a detailed inspection.",
    "Smart_Home": "Based on the screenshot, it appears that your camera is encountering a network connectivity issue. Please try rebooting both your camera and your router, and ensure that the camera is within the optimal range of your Wi-Fi signal. Let us know if you need further assistance.",
    "Medical_Equipment": "Thank you for the image. The error code suggests a calibration issue with the monitor. Please try recalibrating it according to the user manual. If the error persists, contact our technical support immediately to arrange for a service visit."
}

image_requests = [
    "Could you please attach a picture of the issue so we can better diagnose the problem?",
    "Would you mind sending a picture of what you're seeing to help us troubleshoot more accurately?",
    "To assist you further, could you provide a photo of the error you're encountering?",
    "Please attach an image of the error so we can understand the issue better.",
    "Can you share a image of the problem you're experiencing?",
    "A photo of the issue would be really helpful in identifying the problem.",
    "For us to better assist you, could you attach an image showing the error?",
    "Would you please send a picture of what’s happening on your end?",
    "Please provide an image of  the problematic area so we can diagnose the issue.",
    "Could you capture and send a screenshot of the issue you're facing?",
    "To help us pinpoint the problem, could you attach a picture of the error message?",
    "Can you please upload an image that illustrates the issue you’re encountering?",
    "We’d appreciate it if you could send a photo of the problem to help us resolve it.",
    "For better clarity, please share an image of the error or issue you're seeing.",
    "Could you attach a picture that clearly shows the problem?",
    "A visual reference would be very useful—could you please upload a photo of the error?",
    "Would you be able to provide an image of the issue? It will help us diagnose it more accurately.",
    "Please send us an image of the error so we can understand what's happening.",
    "Attaching a photo of the issue would greatly assist us in troubleshooting.",
    "For a faster resolution, could you attach a picture of the problem you're experiencing?"
]



def fetch_relevant_document(question, stage):
    # This is a placeholder function. You need to implement a method to fetch the most relevant document based on the question.
    # For simplicity, let's assume we fetch a document with a specific ID.
    document_id = '000983b6-a898-481a-ae83-cf8db80e89cb'  # Replace with logic to find the most relevant document
    try:
        result = collection.get(document_id)
        # return result.content_as[dict]
    except CouchbaseException as e:
        pass
    
    if stage == "Initial":
        return f"Q: {Questions[question]}"
    # elif stage == "Final":
    #     return f"Rephrase: {Final_response[question]}"