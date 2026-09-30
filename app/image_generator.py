import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(
    api_key=HF_TOKEN,
    provider="auto"
)

def generate_image(prompt, filename):
    folder = "static/generated"
    os.makedirs(folder, exist_ok=True)

    output_path = os.path.join(folder, filename)

    comic_prompt = f"""
High-quality colorful comic book illustration.

Scene:
{prompt}

Style:
professional comic artwork, clean detailed line art,
expressive character, cinematic composition,
vibrant colors, dramatic lighting,
anime-inspired comic style,
no watermark, no text in the image.
"""

    image = client.text_to_image(
        comic_prompt,
        model="black-forest-labs/FLUX.1-schnell"
    )

    image.save(output_path)

    return f"/static/generated/{filename}"