from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch
import torchaudio

def transcribe_audio(audio_path):
    model_path = "my_models/whisper-finetuned-custom/latest"

    # Модель ба токенизер ачаалах
    processor = WhisperProcessor.from_pretrained(model_path)
    model = WhisperForConditionalGeneration.from_pretrained(model_path)

    # Аудио файл унших
    speech_array, sampling_rate = torchaudio.load(audio_path)

    # 16kHz руу хувиргах (шаардлагатай бол)
    if sampling_rate != 16000:
        resampler = torchaudio.transforms.Resample(sampling_rate, 16000)
        speech_array = resampler(speech_array)

    # Tokenize
    inputs = processor(speech_array[0], sampling_rate=16000, return_tensors="pt")

    # Хөрвүүлэлт
    with torch.no_grad():
        predicted_ids = model.generate(inputs["input_features"])

    # Текст рүү хөрвүүлэх
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

    return transcription
