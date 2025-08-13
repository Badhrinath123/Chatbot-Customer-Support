import os
import uuid
from google.cloud import dialogflow_v2 as dialogflow

# Path to your Dialogflow service account key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account.json"

# Your Dialogflow project ID
PROJECT_ID = "customersupportbot-dvha"

def detect_intent_texts(project_id, session_id, text, language_code='en'):
    """Send text to Dialogflow and return detailed bot reply info."""
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)
    result = response.query_result

    return {
        "intent_name": result.intent.display_name,
        "confidence": result.intent_detection_confidence,
        "fulfillment_text": result.fulfillment_text,
        "parameters": dict(result.parameters)
    }

if __name__ == "__main__":
    session_id = str(uuid.uuid4())  # Unique session ID for conversation
    print("💬 Customer Support Bot is ready! Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Bot: Thank you for chatting. Goodbye!")
            break

        bot_data = detect_intent_texts(PROJECT_ID, session_id, user_input)

        # Show intent name & confidence
        print(f"Bot ({bot_data['intent_name']} - {bot_data['confidence']:.2f}): {bot_data['fulfillment_text']}")

        # Show entities if detected
        if bot_data['parameters']:
            print("🔍 Detected Entities:", bot_data['parameters'])
