#!/bin/bash

gpu_list="${CUDA_VISIBLE_DEVICES:-0}"
IFS=',' read -ra GPULIST <<< "$gpu_list"

CHUNKS=${#GPULIST[@]}

MODEL_PATH="/home/kjh/TinyLLaVA_Factory/FinetuneOutput/TinyLLaVA-Phi-2-SigLIP-3.1B"
MODEL_NAME="TinyLLaVA-Phi-2-SigLIP-3.1B"
EVAL_IMG_DIR="/home/kjh/TinyLLaVA_Factory/dataset/v2Dataset/3k"
EVAL_TEXT_PATH="/home/kjh/TinyLLaVA_Factory/dataset/v2text_files/smtest3k.jsonl"
MAX_TOKENS=2048

for IDX in $(seq 0 $((CHUNKS-1))); do
    CUDA_VISIBLE_DEVICES=${GPULIST[$IDX]} python -m tinyllava.eval.model_vqa_loader \
        --model-path $MODEL_PATH \
        --question-file $EVAL_TEXT_PATH \
        --image-folder $EVAL_IMG_DIR \
        --answers-file $MODEL_PATH/generated/${CHUNKS}_${IDX}.jsonl \
        --num-chunks $CHUNKS \
        --chunk-idx $IDX \
        --temperature 0 \
        --max_new_tokens $MAX_TOKENS \
        --conv-mode gemma &
done

wait

output_file=$MODEL_PATH/generated/merge_full2.jsonl

# Clear out the output file if it exists.
> "$output_file"

# Loop through the indices and concatenate each file.
for IDX in $(seq 0 $((CHUNKS-1))); do
    cat $MODEL_PATH/generated/${CHUNKS}_${IDX}.jsonl >> "$output_file"
done