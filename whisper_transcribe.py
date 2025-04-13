# whisper_transcribe.py

import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from scipy.io import wavfile

SAMPLE_RATE = 16000
MODEL_DIR = "whisper-finetuned-custom/latest"
TOKENIZER_DIR = "whisper_bpe_tokenizer"

def transcribe_audio(audio):
    processor = WhisperProcessor.from_pretrained(MODEL_DIR, tokenizer_dir=TOKENIZER_DIR)
    model = WhisperForConditionalGeneration.from_pretrained(MODEL_DIR)
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
    audio = audio / 32768.0
    return transcribe_audio(audio)
