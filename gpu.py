# gpu.py

import torch

if torch.cuda.is_available():
    print("✅ GPU ашиглах боломжтой байна!")
    print("GPU нэр:", torch.cuda.get_device_name(0))
    print("Нийт GPU Memory:", torch.cuda.get_device_properties(0).total_memory / 1024**3, "GB")
else:
    print("❌ GPU ашиглах боломжгүй байна.")
