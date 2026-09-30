import os
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=API_KEY)


def generate_outline(
    story_prompt,
    character_name,
    setting,
    tone,
    art_style
):
    prompt = f"""
Create a simple 5-panel comic story.

Story idea: {story_prompt}
Character: {character_name}
Setting: {setting}
Tone: {tone}
Art style: {art_style}

For each panel provide:

Panel 1
Scene:
Narration:
Dialogue:

Panel 2
Scene:
Narration:
Dialogue:

Panel 3
Scene:
Narration:
Dialogue:

Panel 4
Scene:
Narration:
Dialogue:

Panel 5
Scene:
Narration:
Dialogue:

Keep the story simple, connected, and suitable for a comic.
Do not add extra explanation.
"""

    models = [
        "gemini-3.5-flash",
    ]

    last_error = None

    for model in models:
        for attempt in range(2):
            try:
                print(f"Trying Gemini model: {model}")

                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                print(f"Success: {model}")
                return response.text

            except Exception as error:
                last_error = error
                error_text = str(error)

                print(f"{model} failed: {error_text}")

                if "503" in error_text or "UNAVAILABLE" in error_text:
                    wait_time = 5 * (attempt + 1)
                    print(f"Gemini busy. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    raise

    raise RuntimeError(
        "Gemini is temporarily unavailable. "
        "Please try Generate Comic again after a few minutes."
    ) from last_error