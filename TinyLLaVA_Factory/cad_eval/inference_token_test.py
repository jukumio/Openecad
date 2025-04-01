from transformers import AutoTokenizer
from collections import Counter

# 모델의 토크나이저 로드
tokenizer = AutoTokenizer.from_pretrained("/home/kjh/dev/CAD/TinyLLaVA_Factory/newoutputs/Gemma-2.4B-3epoch/checkpoint-6512")

# 파일 경로 설정
input_file_path = "/home/kjh/dev/CAD/TinyLLaVA_Factory/newoutputs/Gemma-2.4B-3epoch/checkpoint-6512/generated/merge_full.jsonl"  # Inference 파일 경로
output_file_path = "/home/kjh/dev/CAD/TinyLLaVA_Factory/newoutputs/Gemma-2.4B-3epoch/checkpoint-6512/generated/output_token_count.txt"  # 출력 파일 경로
import json

# 토큰 빈도 계산 함수
def count_tokens_from_file(file_path):
    token_counter = Counter()
    
    # 파일 읽기
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # JSON 라인 파싱 (예: JSONL 형식)
            try:
                # 'null'을 'None'으로 변환하여 처리
                entry = json.loads(line.strip(), object_hook=lambda d: {k: None if v is None else v for k, v in d.items()})
                
                prompt = entry.get('prompt', '')
                text = entry.get('text', '')
                
                # 텍스트 합치기
                full_text = prompt + " " + text
                
                # 텍스트 토큰화
                tokens = tokenizer.tokenize(full_text)
                
                # 각 토큰의 빈도 카운트
                token_counter.update(tokens)
                
            except Exception as e:
                print(f"Error processing line: {line}\n{e}")
    
    return token_counter

# 토큰 빈도 계산
token_counter = count_tokens_from_file(input_file_path)

# 가장 많이 나온 토큰 10개를 확인
most_common_tokens = token_counter.most_common(10)

# 결과 파일에 저장
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.write("Most common tokens:\n")
    for token, count in most_common_tokens:
        output_file.write(f"{token}: {count}\n")

print("Token frequency counting complete. Results saved to:", output_file_path)
