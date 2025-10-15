
import os
import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import replicate
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

# Load API Token from .env file
load_dotenv()
API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

# Script Settings
RECORD_SECONDS = 5
TEMP_AUDIO_FILENAME = "temp_audio_recording.wav"
OUTPUT_IMAGE_NAME = 'generated_image_from_voice.png'

# --- FUNCTIONS ---

def record_audio(duration, filename):
    """
    Records audio from the microphone and saves it correctly.
    THIS FUNCTION IS NOW FIXED.
    """
    print("Recording function ke andar...")
    try:
        sample_rate = 44100  # Samples per second
        # Start recording and store the data in a variable
        recording_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.int16)
        sd.wait()  # Wait until the recording is finished
        
        # Save the recorded data from the variable into a WAV file
        write(filename, sample_rate, recording_data)
        return True
    except Exception as e:
        print(f"ERROR: Audio record nahi ho payi. Details: {e}")
        return False

def transcribe_audio(file_path):
    """Sends the audio file to Replicate and returns the transcribed text."""
    print("Transcribing function ke andar...")
    try:
        with open(file_path, 'rb') as audio_file:
            output = replicate.run(
                "openai/whisper:4d50797290df275329f8522a081811a841918a46257506c8f8b98f7db187fe59",
                input={"audio": audio_file}
            )
        transcribed_text = output.get('transcription')
        if not transcribed_text:
            raise ValueError("API did not return a transcription.")
        return transcribed_text.strip()
    except Exception as e:
        print(f"ERROR: Transcription fail ho gayi. Details: {e}")
        return None

def generate_image(prompt):
    """Generates an image from a text prompt."""
    print("Generating image function ke andar...")
    try:
        output = replicate.run(
            "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
            input={"prompt": prompt}
        )
        return output[0]
    except Exception as e:
        print(f"ERROR: Image generate nahi ho payi. Details: {e}")
        return None

def save_and_show_image(image_url, output_filename):
    """Downloads and saves the image."""
    print("Saving image function ke andar...")
    try:
        response = requests.get(image_url, timeout=60)
        img = Image.open(BytesIO(response.content))
        img.save(output_filename)
        img.show()
    except Exception as e:
        print(f"ERROR: Image save nahi ho payi. Details: {e}")


# --- MAIN EXECUTION ---

if __name__ == "__main__":
    print(">>> CHECKPOINT 1: Program shuru ho gaya hai.")

    if not API_TOKEN:
        print(">>> ERROR at CHECKPOINT 2: REPLICATE_API_TOKEN nahi mila! .env file check karein.")
    else:
        print(">>> CHECKPOINT 2: API Token mil gaya hai.")
        
        print(">>> CHECKPOINT 3: Ab audio record karne ja rahe hain...")
        print(f"{RECORD_SECONDS} seconds ke liye bolna shuru karein...")
        
        if record_audio(RECORD_SECONDS, TEMP_AUDIO_FILENAME):
            print(">>> CHECKPOINT 4: Audio recording successful.")
            
            text_prompt = transcribe_audio(TEMP_AUDIO_FILENAME)
            if text_prompt:
                print(">>> CHECKPOINT 5: Transcription successful.")
                print(f"   Transcribed Text: \"{text_prompt}\"")
                
                generated_image_url = generate_image(text_prompt)
                if generated_image_url:
                    print(">>> CHECKPOINT 6: Image generation successful.")
                    
                    save_and_show_image(generated_image_url, OUTPUT_IMAGE_NAME)
                    print("\n>>> PROGRAM FINISHED SUCCESSFULLY!")
            
            # Clean up the temporary audio file
            try:
                os.remove(TEMP_AUDIO_FILENAME)
            except:
                pass
 
