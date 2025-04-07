from transformers import AutoTokenizer, AutoModelForCausalLM
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

filtered_tokens = [token for token in tokens[261:] if token[0] == 'Ġ']

suppressed_indices = text_tokenizer.convert_tokens_to_ids(filtered_tokens)
input_tensor = text_tokenizer(selected_prefix, return_tensors='pt').to(device_type)

generated_output = language_model.generate(
    **input_tensor,
    max_new_tokens=30,
    do_sample=True,
    eos_token_id=text_tokenizer.encode('.')[0],
    pad_token_id=text_tokenizer.eos_token_id,
    penalty_alpha=0.6,
    repetition_penalty=1.8,
    top_k=3,
    top_p=0.92,
    suppress_tokens=suppressed_indices
)

print(f'first prefix: {selected_prefix}')
decoded_output = text_tokenizer.decode(generated_output[0])
print(decoded_output)

#leading spaces check