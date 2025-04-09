from huggingface_hub import hf_hub_download
import os
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer


model_name = 'unsloth/gemma-3-1b-it-unsloth-bnb-4bit'
adapter_repo_id = 'davide710/pf_gemma_1b'
your_token = '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'

download_dir = 'gemma_files'
os.makedirs(download_dir, exist_ok=True)

hf_hub_download(repo_id=model_name, filename='added_tokens.json', token=your_token, local_dir=download_dir)
hf_hub_download(repo_id=model_name, filename='config.json', token=your_token, local_dir=download_dir)
hf_hub_download(repo_id=model_name, filename='generation_config.json', token=your_token, local_dir=download_dir)
hf_hub_download(repo_id=model_name, filename='model.safetensors', token=your_token, local_dir=download_dir)
hf_hub_download(repo_id=model_name, filename='special_tokens_map.json', token=your_token, local_dir=download_dir)
hf_hub_download(repo_id=model_name, filename='tokenizer.json', token=your_token, local_dir=download_dir)
hf_hub_download(repo_id=model_name, filename='tokenizer.model', token=your_token, local_dir=download_dir)
hf_hub_download(repo_id=model_name, filename='tokenizer_config.json', token=your_token, local_dir=download_dir)

adapter_filename = 'adapter_model.safetensors'
hf_hub_download(repo_id=adapter_repo_id, filename=adapter_filename, token=your_token, local_dir=download_dir)

print(f"Downloaded files to: {download_dir}")

base_model_name = 'unsloth/gemma-3-1b-it-unsloth-bnb-4bit'
adapter_repo_id = 'davide710/pf_gemma_1b'

base_model = AutoModelForCausalLM.from_pretrained(base_model_name, token=your_token, torch_dtype=torch.float16)
tokenizer = AutoTokenizer.from_pretrained(base_model_name, token=your_token)

merged_model = PeftModel.from_pretrained(base_model, adapter_repo_id, token=your_token)

merged_model = merged_model.merge_and_unload()
merged_model.eval()

merged_model_path = 'merged_gemma'
merged_model.save_pretrained(merged_model_path)
tokenizer.save_pretrained(merged_model_path)

print(f"Merged model saved to: {merged_model_path}")