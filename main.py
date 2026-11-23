import os
import json
import urllib.request
import urllib.parse

# This script demonstrates integrating Azure AI services, a key skill for the Microsoft AB-650 exam.
# Specifically, it uses Azure AI Language (Text Analytics) for sentiment analysis.
# In a real-world scenario, the 'text_to_analyze' could come from a Microsoft 365 source
# like a SharePoint document, an Exchange Online email, or a Teams message.

# --- Configuration (replace with your Azure AI Language service details) ---
# You need an Azure AI Language resource.
# Set these as environment variables or replace the placeholders.
# Example:
# export AZURE_AI_LANGUAGE_ENDPOINT="https://YOUR_RESOURCE_NAME.cognitiveservices.azure.com/"
# export AZURE_AI_LANGUAGE_KEY="YOUR_SUBSCRIPTION_KEY"

AZURE_AI_LANGUAGE_ENDPOINT = os.getenv("AZURE_AI_LANGUAGE_ENDPOINT")
AZURE_AI_LANGUAGE_KEY = os.getenv("AZURE_AI_LANGUAGE_KEY")

if not AZURE_AI_LANGUAGE_ENDPOINT or not AZURE_AI_LANGUAGE_KEY:
    print("Error: Please set AZURE_AI_LANGUAGE_ENDPOINT and AZURE_AI_LANGUAGE_KEY environment variables.")
    print("You can get these from your Azure AI Language resource in the Azure portal.")
    exit(1)

# Ensure the endpoint ends with /text/analytics/v3.1/sentiment
# Or adjust based on the specific API version you intend to use.
# For sentiment analysis, the path is typically /text/analytics/v3.1/sentiment
# The base endpoint from Azure portal might be just "https://YOUR_RESOURCE_NAME.cognitiveservices.azure.com/"
# We need to append the specific API path.
API_PATH = "text/analytics/v3.1/sentiment"
if not AZURE_AI_LANGUAGE_ENDPOINT.endswith("/"):
    AZURE_AI_LANGUAGE_ENDPOINT += "/"
FULL_API_URL = f"{AZURE_AI_LANGUAGE_ENDPOINT}{API_PATH}"

# --- Sample Data ---
# This text could represent content from a Microsoft 365 document, email, or chat.
text_to_analyze = "Microsoft 365 hizmetleri ve yapay zeka çözümleri, şirketlerin rekabet gücünü artırıyor. Bu sertifika kariyeriniz için çok önemli."
# Another example: "Bu ürün beklentilerimi karşılamadı, çok hayal kırıklığına uğradım."

# --- Prepare Request ---
documents = {
    "documents": [
        {
            "id": "1",
            "language": "tr", # Specify language (Turkish in this case, matching the article)
            "text": text_to_analyze
        }
    ]
}

headers = {
    "Content-Type": "application/json",
    "Ocp-Apim-Subscription-Key": AZURE_AI_LANGUAGE_KEY
}

data = json.dumps(documents).encode("utf-8")

# --- Make API Call ---
try:
    req = urllib.request.Request(FULL_API_URL, data=data, headers=headers, method='POST')
    with urllib.request.urlopen(req) as response:
        response_data = json.load(response)

    # --- Process Response ---
    if response_data and "documents" in response_data:
        for doc in response_data["documents"]:
            if doc["id"] == "1":
                sentiment = doc.get("sentiment")
                confidence_scores = doc.get("confidenceScores")
                print(f"Original Text: '{text_to_analyze}'")
                print(f"Detected Sentiment: {sentiment.upper()}") # AB-650 focus: AI integration
                if confidence_scores:
                    print(f"Confidence Scores:")
                    for key, value in confidence_scores.items():
                        print(f"  {key.capitalize()}: {value:.2f}")
                break
    elif "error" in response_data:
        print(f"API Error: {response_data['error']['message']}")
    else:
        print("Unexpected API response format.")

except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code} - {e.reason}")
    try:
        error_details = json.load(e)
        if "error" in error_details:
            print(f"Details: {error_details['error']['message']}")
    except json.JSONDecodeError:
        print("Error: Could not decode error details from response.")
except urllib.error.URLError as e:
    print(f"URL Error: {e.reason}")
except json.JSONDecodeError:
    print("Error: Could not decode JSON response.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
