from transformers import AutoTokenizer

# Gemma SigLIP 모델의 토크나이저 불러오기
tokenizer = AutoTokenizer.from_pretrained("/home/kjh/dev/CAD/TinyLLaVA_Factory/newoutputs/Gemma-2.4B-3epoch")

# CAD 시퀀스를 토큰화하여 길이 확인
cad_sequence = "여기에 학습할 CAD 시퀀스 입력"
tokenized = tokenizer(cad_sequence, return_tensors="pt")

print(f"Total token length: {tokenized.input_ids.shape[1]}")
print(f"Model max length: {tokenizer.model_max_length}")
