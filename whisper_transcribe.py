import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from scipy.io import wavfile
import numpy as np

# 🎯 Загварын байрлал (latest/ фолдер руу чиглүүлсэн байх ёстой)
MODEL_DIR = "/home/billy/ai_voice_server/my_models"
SAMPLE_RATE = 16000

# 📌 Аудионоос хөрвүүлэлт хийх функц
def transcribe_audio(audio):
    processor = WhisperProcessor.from_pretrained(MODEL_DIR)
    model = WhisperForConditionalGeneration.from_pretrained(MODEL_DIR)

    model.eval()
    model.generation_config.forced_decoder_ids = None

    if torch.cuda.is_available():
        model.to("cuda")

    # 🧠 Input features бэлтгэх
    inputs = processor(audio, sampling_rate=SAMPLE_RATE, return_tensors="pt")

    if torch.cuda.is_available():
        inputs = {k: v.to("cuda") for k, v in inputs.items()}

    # 🔍 No gradient
    with torch.no_grad():
        output = model.generate(
            inputs["input_features"],
            max_length=448,
            pad_token_id=processor.tokenizer.pad_token_id,
            decoder_start_token_id=processor.tokenizer.bos_token_id
        )

    text = processor.batch_decode(output, skip_special_tokens=True)[0]
    return text.strip()

# 📁 WAV файл хөрвүүлэх
def transcribe_audio_from_file(file_path):
    rate, audio = wavfile.read(file_path)

    # 🎧 WAV-г float руу хөрвүүлэх (16-bit WAV гэж үзнэ)
    if audio.dtype == np.int16:
        audio = audio.astype(np.float32) / 32768.0
    elif audio.dtype == np.float32:
        audio = np.clip(audio, -1.0, 1.0)  # аль хэдийн OK
    else:
        raise ValueError(f"Unsupported audio dtype: {audio.dtype}")

    return transcribe_audio(audio)
