DATA_PATH="/home/kjh/dev/CAD/TinyLLaVA_Factory/dataset/real_train/train_jh.json"
IMAGE_PATH="/home/kjh/dev/CAD/TinyLLaVA_Factory/dataset/real_train/train_images"
MODEL_MAX_LENGTH=2048
OUTPUT_DIR="/home/kjh/dev/CAD/TinyLLaVA_Factory/newoutputs/Gemma-2.4B-1epoch"

deepspeed --include localhost:2,3 --master_port 29501 /home/kjh/dev/CAD/TinyLLaVA_Factory/tinyllava/train/custom_finetune.py \
    --deepspeed /home/kjh/dev/CAD/TinyLLaVA_Factory/scripts/zero2.json \
    --data_path  $DATA_PATH \
    --image_folder $IMAGE_PATH \
    --is_multimodal True \
    --conv_version gemma \
    --mm_vision_select_layer -2 \
    --image_aspect_ratio square \
    --fp16 True \
    --training_recipe lora \
    --tune_type_llm lora \
    --tune_type_vision_tower frozen \
    --tune_vision_tower_from_layer 0 \
    --tune_type_connector full \
    --lora_r 128 \
    --lora_alpha 256 \
    --group_by_modality_length False \
    --pretrained_model_path "tinyllava/TinyLLaVA-Gemma-SigLIP-2.4B" \
    --output_dir $OUTPUT_DIR \
    --num_train_epochs 1 \
    --per_device_train_batch_size 1 \
    --per_device_eval_batch_size 1 \
    --gradient_accumulation_steps 8 \
    --evaluation_strategy "no" \
    --save_strategy "steps" \
    --save_steps 1628 \
    --learning_rate 1e-4 \
    --weight_decay 0. \
    --warmup_ratio 0.03 \
    --lr_scheduler_type "cosine" \
    --logging_steps 1 \
    --tf32 False \
    --model_max_length $MODEL_MAX_LENGTH \
    --gradient_checkpointing True \
    --dataloader_num_workers 8 \
    --lazy_preprocess True \
    --report_to tensorboard \
    --tokenizer_use_fast False \
    --run_name Gemma-2.4B-1epoch
