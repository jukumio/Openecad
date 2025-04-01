import json

# 두 개의 JSONL 파일을 읽고 합치기
file1 = "/home/kjh/dev/CAD/TinyLLaVA_Factory/newoutputs/Gemma-2.4B-3epoch/generated/2_0.jsonl"
file2 = "/home/kjh/dev/CAD/TinyLLaVA_Factory/newoutputs/Gemma-2.4B-3epoch/generated/2_1.jsonl"
output_file = "/home/kjh/dev/CAD/TinyLLaVA_Factory/newoutputs/Gemma-2.4B-3epoch/generated/self_merge.jsonl"

with open(file1, "r", encoding="utf-8") as f1, open(file2, "r", encoding="utf-8") as f2:
    lines1 = f1.readlines()
    lines2 = f2.readlines()

# 합쳐서 새로운 JSONL 파일로 저장
with open(output_file, "w", encoding="utf-8") as out_f:
    for line in lines1 + lines2:  # 두 리스트를 합쳐서 저장
        out_f.write(line)

print(f"Merged {file1} and {file2} into {output_file}")
