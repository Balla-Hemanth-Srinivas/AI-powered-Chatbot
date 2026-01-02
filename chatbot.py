import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatBot:
    def __init__(self):
        self.chatbot_pipeline = None
        try:
            from transformers import pipeline, Conversation
            logger.info("Loading NLP model...")
            # Using a small model for faster download and inference on local machine
            self.chatbot_pipeline = pipeline("conversational", model="microsoft/DialoGPT-small")
            logger.info("Model loaded successfully.")
        except ImportError:
            logger.warning("Transformers not installed. Using fallback echo bot.")
        except Exception as e:
            logger.error(f"Error loading model: {e}. Using fallback echo bot.")

    def get_response(self, message: str) -> str:
        if self.chatbot_pipeline:
            try:
                from transformers import Conversation
                conversation = Conversation(message)
                result = self.chatbot_pipeline(conversation)
                return result.messages[-1]["content"]
            except Exception as e:
                logger.error(f"Error generating response: {e}")
                return "I'm sorry, I'm having trouble thinking right now."
        else:
            return f"Echo (Transformers not available): {message}"

# Create a global instance
chatbot = ChatBot()
