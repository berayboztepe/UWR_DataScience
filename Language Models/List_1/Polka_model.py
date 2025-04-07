import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "eryk-mazus/polka-1.1b"

tokenizer = AutoTokenizer.from_pretrained(model_name, padding_side="left")
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto"
)

prompt = "Translate from English to Polish: 'I love learning new languages.'"
prompt_2 = "Translate from English to Polonistyczne: 'She enjoys swimming in the lake.'"

model_inputs = tokenizer([prompt], return_tensors="pt", padding=True)

with torch.no_grad():
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=50,  
        do_sample=False,    
        top_k=5,            
        penalty_alpha=0.6 
    )

output = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
print(output)
