#!/bin/bash

gpu_list="${CUDA_VISIBLE_DEVICES:-0}"
IFS=',' read -ra GPULIST <<< "$gpu_list"

CHUNKS=${#GPULIST[@]}

MODEL_PATH="/home/kjh/dev/CAD/TinyLLaVA_Factory/newoutputs/Gemma-2.4B-quarter/checkpoint-2035"
MODEL_NAME="checkpoint-2035"
EVAL_IMG_DIR="/home/kjh/dev/CAD/TinyLLaVA_Factory/dataset/10k_dataset/10k_images"
EVAL_TEXT_PATH="/home/kjh/dev/CAD/TinyLLaVA_Factory/dataset/10k_dataset/10k_test_data.jsonl"
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

output_file=$MODEL_PATH/generated/merge_full.jsonl

# Clear out the output file if it exists.
> "$output_file"

# Loop through the indices and concatenate each file.
for IDX in $(seq 0 $((CHUNKS-1))); do
    cat $MODEL_PATH/generated/${CHUNKS}_${IDX}.jsonl >> "$output_file"
done