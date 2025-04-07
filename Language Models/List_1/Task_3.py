import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from torch.nn import functional as F

generator = pipeline('text-generation', model='flax-community/papuGaPT2')
model_name = 'flax-community/papuGaPT2'
device = 'cpu'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)

def log_probs_from_logits(logits, labels):
    logp = F.log_softmax(logits, dim=-1)
    logp_label = torch.gather(logp, 2, labels.unsqueeze(2)).squeeze(-1)
    return logp_label
    
            
def sentence_prob(sentence_txt):
    input_ids = tokenizer(sentence_txt, return_tensors='pt')['input_ids'].to(device)
    with torch.no_grad():
        output = model(input_ids=input_ids)
        log_probs = log_probs_from_logits(output.logits[:, :-1, :], input_ids[:, 1:])
        seq_log_probs = torch.sum(log_probs)
    return seq_log_probs.cpu().numpy()

def normalized_sentence_prob(txt):
    length = len(tokenizer(txt, return_tensors='pt')['input_ids'][0])
    return sentence_prob(txt) / length


bad_count, good_count, line_count = 0, 0, 0

with open('Language Models/Exercise_1/Materials_1/P1/reviews_for_task3.txt', 'r', encoding='UTF-8') as file:
    for line in file.readlines():
        prompt = ' '.join(line.split(' ')[1:])
        line_count += 1

        g_prompt = prompt + ' Polecam'
        b_prompt = prompt + ' Nie polecam'
        good_prob = normalized_sentence_prob(g_prompt)
        bad_prob = normalized_sentence_prob(b_prompt)

        if good_prob > bad_prob:
            if line.startswith('GOOD'):
                good_count += 1
        else:
            if line.startswith('BAD'):
                bad_count += 1

line_count /= 2
line_count = int(line_count)
print(f'{good_count}/{line_count} - Positive Reviews')
print(f'{bad_count}/{line_count} - Negative Reviews')