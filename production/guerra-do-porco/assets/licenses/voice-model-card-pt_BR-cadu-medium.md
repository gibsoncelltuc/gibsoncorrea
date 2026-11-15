<!-- cópia literal da ficha do modelo (https://huggingface.co/rhasspy/piper-voices/blob/main/pt/pt_BR/cadu/medium/MODEL_CARD), lida em 2026-11-15 -->
# Model card for cadu (medium)

* Language: pt_BR (Portuguese, Brazil)
* Speakers: 1
* Quality: medium
* Samplerate: 22,050Hz

## Dataset

* URL: https://github.com/OHF-Voice/voice-datasets
* License: CC0

## Training

Finetuned from the rdh base model (medium quality; nl_BE, one Flemish speaker, CC0), with MRD and SDP.

Default inference settings are noise_scale 0.5 and noise_w 0.333.

Requires Piper 1.5 or higher.
