from dotenv import load_dotenv
import os
from huggingface_hub import InferenceClient

load_dotenv()
client = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta", token=os.getenv("HF_TOKEN"))

resp = client.chat_completion(
    messages=[{"role": "user", "content": "Say hello in one word."}],
    max_tokens=20,
)
print(resp)
