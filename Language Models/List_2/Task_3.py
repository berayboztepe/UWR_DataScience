import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from torch.nn import functional as F

model_name = 'flax-community/papuGaPT2'
device = 'cpu'

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)


def log_probs_from_logits(logits, labels):
    logp = F.log_softmax(logits, dim=-1)
    logp_label = torch.gather(logp, 2, labels.unsqueeze(2)).squeeze(-1)
    return logp_label


def sentence_prob(sentence_txt):
    input_ids = tokenizer(sentence_txt, return_tensors='pt')[
        'input_ids'].to(device)

    with torch.no_grad():
        output = model(input_ids=input_ids)
        log_probs = log_probs_from_logits(
            output.logits[:, :-1, :], input_ids[:, 1:])
        seq_log_probs = torch.sum(log_probs)
    return seq_log_probs.cpu().numpy().item()


sentence_options = "ona|ono wprost|wyprosty|wyprostu|wyprost uwielbiała|wielbił|wielbiła|uwielbił|wielbiło|uwielbiał|uwielbiało|uwielbiały słuchać|osłuchać|słychać|usłuchać o|i|e|a|ó|ę|y|ą|u wartościach własnych|owłosionych macierzy|mocarz|macierzą|macierze|mocarza|mocarze|mocarzy|macierz"
sentence_options = [x.split('|') for x in sentence_options .split(' ')]

beam_size = 2

beam_candidates  = [(x, sentence_prob(x)) for x in sentence_options [0]]
beam_candidates  = sorted(beam_candidates , key=lambda x: x[1], reverse=True)
beam_candidates  = beam_candidates [:beam_size]

for depth in range(1, len(sentence_options)):
    variations = sentence_options [depth]
    print(f"depth: {depth}\n")
    new_beam_candidates  = []
    
    for index, beam in enumerate(beam_candidates):
        print(f'Current beam {index + 1}/{len(beam_candidates)}')
        best_candidates = []

        for variation in variations:
            sentence = beam[0] + ' ' + variation
            prob = sentence_prob(sentence)
            best_candidates.append((sentence, prob))
        best_candidates = sorted(best_candidates, key=lambda x: x[1], reverse=True)
        best_candidates = best_candidates[:beam_size]
        new_beam_candidates .extend(best_candidates)

    beam_candidates  = new_beam_candidates 

beam_candidates = sorted(beam_candidates, key=lambda x: x[1], reverse=True)
correct_sentence = " ".join([o[0] for o in sentence_options ])

for beam in beam_candidates:
    print(beam)

print(f"correct sentence = {correct_sentence}")

for index, beam in enumerate(beam_candidates):
    if beam[0] == correct_sentence:
        print(f"Correct sentence found in beam_candidates  at: {index}. index")
        break