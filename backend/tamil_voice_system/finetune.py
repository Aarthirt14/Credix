import torch
from datasets import load_dataset, Audio
from transformers import (
    WhisperForConditionalGeneration, 
    WhisperProcessor, 
    Seq2SeqTrainingArguments, 
    Seq2SeqTrainer
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import os

def train():
    # 1. Load Dataset
    print("Loading dataset...")
    # Using 'mozilla-foundation/common_voice_13_0' mapped from the ID provided
    ds = load_dataset("mozilla-foundation/common_voice_13_0", "ta", split="train", streaming=True)
    
    # 2. Load Processor and Model
    model_name = "openai/whisper-small"
    processor = WhisperProcessor.from_pretrained(model_name, language="Tamil", task="transcribe")
    model = WhisperForConditionalGeneration.from_pretrained(model_name)
    
    # 3. Prepare for LoRA (Efficiency)
    model = prepare_model_for_kbit_training(model)
    config = LoraConfig(r=32, lora_alpha=64, target_modules=["q_proj", "v_proj"], lora_dropout=0.05, bias="none")
    model = get_peft_model(model, config)
    
    # 4. Data Collator
    from transformers import DataCollatorForSeq2Seq
    data_collator = DataCollatorForSeq2Seq(processor, model=model)

    # 5. Training Arguments
    training_args = Seq2SeqTrainingArguments(
        output_dir="./whisper-tamil-finetuned",
        per_device_train_batch_size=8,
        gradient_accumulation_steps=2,
        learning_rate=1e-4,
        warmup_steps=50,
        max_steps=500, # Adjust based on GPU time
        gradient_checkpointing=True,
        fp16=True,
        evaluation_strategy="no",
        save_steps=100,
        logging_steps=10,
        report_to=["tensorboard"],
        load_best_model_at_end=False,
        predict_with_generate=True,
        push_to_hub=False,
    )

    # 6. Trainer
    trainer = Seq2SeqTrainer(
        args=training_args,
        model=model,
        train_dataset=ds, # Streaming dataset requires special handling or conversion
        data_collator=data_collator,
        tokenizer=processor.feature_extractor,
    )

    print("Starting training (LoRA)...")
    trainer.train()
    
    # Save the adapter
    model.save_pretrained("./whisper-tamil-finetuned")
    print("Training finished. Adaptor saved to ./whisper-tamil-finetuned")

if __name__ == "__main__":
    if torch.cuda.is_available():
        train()
    else:
        print("CUDA not available. Fine-tuning requires a GPU.")
