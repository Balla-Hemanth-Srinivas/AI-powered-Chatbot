import logging
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("Attempting to import transformers...")
try:
    from transformers import pipeline, Conversation
    print("Transformers imported successfully.")
except ImportError as e:
    print(f"FAILED to import transformers: {e}")
    exit(1)

print("Attempting to import torch...")
try:
    import torch
    print(f"Torch imported successfully. Version: {torch.__version__}")
except ImportError as e:
    print(f"FAILED to import torch: {e}")
    exit(1)

print("Attempting to load model 'microsoft/DialoGPT-small'...")
try:
    chatbot_pipeline = pipeline("conversational", model="microsoft/DialoGPT-small")
    print("SUCCESS: Model loaded successfully.")
except Exception as e:
    print("FAILED to load model.")
    traceback.print_exc()
