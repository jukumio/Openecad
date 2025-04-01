from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer

# 모델 및 토크나이저 로드
model = AutoModelForCausalLM.from_pretrained("/home/kjh/dev/CAD/TinyLLaVA_Factory/newoutputs/Gemma-2.4B-3epoch")
tokenizer = AutoTokenizer.from_pretrained("/home/kjh/dev/CAD/TinyLLaVA_Factory/newoutputs/Gemma-2.4B-3epoch")

# 모델에 입력할 CAD 시퀀스
input_text = "여기에 학습할 CAD 시퀀스 일부 입력"
input_ids = tokenizer(input_text, return_tensors="pt").input_ids

# 모델 예측 실행
output_ids = model.generate(input_ids, max_length=200)  # 적절한 max_length 설정

# 결과 디코딩
generated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
print("Generated CAD Sequence:", generated_text)
