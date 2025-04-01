from transformers import AutoTokenizer

# 토크나이저 로드
tokenizer = AutoTokenizer.from_pretrained("/home/kjh/dev/CAD/TinyLLaVA_Factory/newoutputs/Gemma-2.4B-3epoch")

# 확인할 문자열
input_text = ""

# 토큰화 수행
tokenized_output = tokenizer.tokenize(input_text)
token_ids = tokenizer.convert_tokens_to_ids(tokenized_output)

# 결과 출력
print("🔹 Original Text:", input_text)
print("🔹 Tokenized Output:", tokenized_output)
print("🔹 Token IDs:", token_ids)


from collections import Counter

# 생성된 토큰의 빈도수 분석
token_counts = Counter(token_ids)  # generated_token_ids는 모델이 생성한 토큰 ID 리스트

# "increase" 토큰의 반복 여부 확인
increase_count = token_counts[4740]

print(f"🔹 '▁increase' (ID: 4740) Count: {increase_count}")
