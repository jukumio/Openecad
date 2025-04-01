import json, os, argparse
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--file_path', type=str, default='outputs/OpenECAD-Gemma-SigLip-2.4B-lora-split/generated/merge.jsonl')
parser.add_argument('--save_dir', type=str, default='outputs/OpenECAD-Gemma-SigLip-2.4B-lora-split/generated/pyfiles')
args = parser.parse_args()

file_path = args.file_path
save_dir = args.save_dir

skipped_count = 0  # 스킵한 개수 카운트

def save_py(string, id):
    global skipped_count
    try:
        save_path = os.path.join(save_dir, id + '.py')
        with open(save_path, 'w') as f:
            str_li = string.split('\n')[2:-1]

            # 비정상적인 코드 필터링
            if not str_li or '`' in str_li[-1] or not str_li[-1].endswith(')'):
                skipped_count += 1
                return
            
            for s in str_li:
                f.write(s + '\n')
    except Exception:
        skipped_count += 1  # 예외 발생 시 스킵

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

with open(file_path) as f:
    if file_path.endswith('.jsonl'):
        for line in tqdm(f):
            try:
                data = json.loads(line)
                text = data['text']
                id = data['question_id']
                save_py(text, id)
            except Exception:
                skipped_count += 1  # JSON 파싱 에러도 스킵
    elif file_path.endswith('.json'):
        data = json.load(f)
        for d in data:
            try:
                text = d['answer']
                id = d['question_id']
                save_py(text, id)
            except Exception:
                skipped_count += 1  # JSON 파싱 에러도 스킵

print(f"Skipped {skipped_count} files due to invalid text values or errors.")
