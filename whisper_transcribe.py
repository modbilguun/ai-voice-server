# whisper_transcribe.py

import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from scipy.io import wavfile
from huggingface_hub import login
import os
from dotenv import load_dotenv

# ✅ .env файл ачаалж, токен авах
load_dotenv()
token = os.getenv("HUGGINGFACE_HUB_TOKEN")

# ✅ Hugging Face-д нэвтрэх (локал хөгжүүлэлтийн үед)
if token:
    login(token)

# ✅ Hugging Face дээрх моделийн нэр
MODEL_REPO = "modbilguun/whisper-finetuned-custom"
SAMPLE_RATE = 16000

def transcribe_audio(audio):
    processor = WhisperProcessor.from_pretrained(MODEL_REPO, token=token)
    model = WhisperForConditionalGeneration.from_pretrained(MODEL_REPO, token=token)

    model.eval()
    model.generation_config.forced_decoder_ids = None
    if torch.cuda.is_available():
        model.to("cuda")

    inputs = processor(audio, sampling_rate=SAMPLE_RATE, return_tensors="pt")
    if torch.cuda.is_available():
        inputs = {k: v.to("cuda") for k, v in inputs.items()}

    output = model.generate(
        inputs["input_features"],
        max_length=448,
        pad_token_id=processor.tokenizer.pad_token_id,
        decoder_start_token_id=processor.tokenizer.bos_token_id
    )
    text = processor.batch_decode(output, skip_special_tokens=True)[0]
    return text

def transcribe_audio_from_file(file_path):
    rate, audio = wavfile.read(file_path)
    audio = audio / 32768.0  # 16-bit WAV
    return transcribe_audio(audio)
