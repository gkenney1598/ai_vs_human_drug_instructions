import pandas as pd
import random
import numpy as np
from sklearn.model_selection import train_test_split
from transformers import RobertaTokenizer, RobertaForSequenceClassification
from transformers import Trainer, TrainingArguments
from datasets import Dataset
from sklearn.metrics import f1_score, accuracy_score, recall_score

def arg_max(model_preds):
    label_preds = []
    for i in model_preds:
        label_preds.append(np.argmax(i))
    return label_preds

def evaluate(type, labels, preds):
    f1 = f1_score(labels, preds)
    print(f"{type} F1 SCORE: ", f1)
    accuracy = accuracy_score(labels, preds)
    print(f"{type} ACCURACY SCORE: ", accuracy)
    recall = recall_score(labels, preds)
    print(f"{type} RECALL SCORE: ", recall)

def tokenize(batch):
    tokenizer = RobertaTokenizer.from_pretrained("roberta-base")

    return tokenizer(
        batch["sentence"],
        truncation=True,
        padding="max_length",
        max_length=512,
    )

def model(fname):
    df = pd.read_csv(fname)

    df = df.rename(columns={"instructions": "sentence", "generated": "labels"})

    train_df, test_df = train_test_split(df, test_size=0.3, random_state=42)

    val_df, test_df = train_test_split(test_df, test_size=0.5, random_state=0)

    train_ds = Dataset.from_pandas(train_df)
    test_ds = Dataset.from_pandas(test_df)
    val_ds = Dataset.from_pandas(val_df)

    for index, row in df.iterrows():
        sentence = row["sentence"]
        beginning = random.randint(0, len(sentence) - 512)
        truncated_sentence = sentence[beginning:beginning + 512]
        df.at[index, "sentence"] = truncated_sentence

    train_ds = train_ds.map(tokenize, batched=True)
    test_ds = test_ds.map(tokenize, batched=True)
    val_ds = val_ds.map(tokenize, batched=True)

    #Set format for PyTorch
    train_ds.set_format("torch")
    test_ds.set_format("torch")
    val_ds.set_format("torch")

    model = RobertaForSequenceClassification.from_pretrained("roberta-base", num_labels=2)

    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        logging_steps=20,
        evaluation_strategy="epoch",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
    )

    trainer.train()

    train_preds, train_label_ids, train_metrics = trainer.predict(train_ds)
    preds = arg_max(train_preds)
    evaluate("train", train_df["labels"], preds)

    val_preds, val_label_ids, val_metrics = trainer.predict(val_ds)
    preds = arg_max(val_preds)
    evaluate("val", val_df["labels"], preds)

    test_preds, test_label_ids, test_metrics = trainer.predict(test_ds)
    preds = arg_max(test_preds)
    evaluate("test", test_df["labels"], preds)

def main():
    model("data/Human_ChatGPTGen.csv")

main()