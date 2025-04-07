import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from torch.nn import functional as F
import pandas as pd

model_identifier = 'flax-community/papuGaPT2'
device_type = 'cpu'

text_tokenizer = AutoTokenizer.from_pretrained(model_identifier)
language_model = AutoModelForCausalLM.from_pretrained(model_identifier).to(device_type)

vocab_indices = list(range(text_tokenizer.vocab_size))
tokens = text_tokenizer.convert_ids_to_tokens(vocab_indices)

prefix_file_path = r"C:\Users\beray\Code Projects\Language Models\Exercise_2\prefiksy.txt"
prefix_dataset = pd.read_csv(prefix_file_path, header=None, sep='\t')
prefix_dataset = prefix_dataset.sample(frac=1)
selected_prefix = prefix_dataset.iloc[0, 0]

first_letter = selected_prefix[0].lower()

print(f'Should start with: "{first_letter}"')
filtered_tokens = [t for t in tokens[261:] if (
    t.startswith('Ġ') and t[1].lower() != first_letter)]

suppressed_indices = text_tokenizer.convert_tokens_to_ids(filtered_tokens)

input_tensor = text_tokenizer(selected_prefix, return_tensors='pt').to(device_type)

outputs = []
option_count = 5
for i in range(option_count):
    output = language_model.generate(**input_tensor,
                            max_new_tokens=30,
                            do_sample=True,
                            eos_token_id=text_tokenizer.encode('.')[0],
                            pad_token_id=text_tokenizer.eos_token_id,
                            penalty_alpha=0.6,
                            repetition_penalty=1.8,
                            top_k=5,
                            top_p=0.92,
                            suppress_tokens=suppressed_indices)
    outputs.append(text_tokenizer.decode(output[0]))


def clean_sentence(sentence):
    sentence = sentence.replace(" ,", ",").replace(" .", ".").replace(" ?", "?")
    return sentence.strip()

def score_sentence(output):
    return sum([len(w) for w in output.split(' ')])

best_sentence = ""
best_score = 0
for output in outputs:
    output = clean_sentence(output)
    score = score_sentence(output)
    if score > best_score:
        best_score = score
        best_sentence = output

print(f'best_sentence : {best_sentence} - with score: {best_score}')
