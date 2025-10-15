# Speech-to-Image Generator using Replicate API

This Python script captures audio directly from your microphone, transcribes it into a text prompt using OpenAI's Whisper model, and then generates a high-quality image using Stability AI's Stable Diffusion model. The entire process is powered by the Replicate API and is automated to run with a single command.

## ✨ Features

-   🎤 Microphone Input: Captures live audio directly from your default microphone.
-   🗣️ Speech-to-Text: Utilizes the powerful Whisper model for accurate, multi-language transcription.
-   🎨 Text-to-Image: Leverages the Stable Diffusion model to generate creative and high-quality images from text prompts.
-   🔐 Secure API Key Handling: Uses a .env file to keep your Replicate API token safe and out of the source code.
-   🤖 Fully Automated: The entire pipeline—from recording your voice to displaying the final image—is handled by the script.

Technologies Used

-   Python 3.x
-   Replicate API
-   Libraries:
    -   replicate: The official Python client for the Replicate API.
    -   python-dotenv: To load environment variables from the .env file.
    -   sounddevice & scipy: For recording audio from the microphone and saving it as a WAV file.
    -   requests & Pillow: For downloading and handling the generated image.

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### 1. Prerequisites

-   Python 3.7 or higher
-   A working microphone connected to your computer
-   A Replicate API token
