import itertools
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
from torch.nn import functional as F

model_name = "gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
device = "cpu"

def log_probs_from_logits(logits, labels):
    logp = F.log_softmax(logits, dim=-1)
    logp_label = torch.gather(logp, 2, labels.unsqueeze(2)).squeeze(-1)
    return logp_label

def score_sentence(sentence):
    input_ids = tokenizer(sentence, return_tensors='pt')['input_ids'].to(device)
    with torch.no_grad():
        output = model(input_ids=input_ids)
        log_probs = log_probs_from_logits(output.logits[:, :-1, :], input_ids[:, 1:])
        seq_log_probs = torch.sum(log_probs)
    return seq_log_probs.cpu().numpy()

def generate_permutations(words):
    return list(itertools.permutations(words))

def generate_sentences(permutations, first_word):
    sentences = []
    for perm in permutations:
        sentence = first_word + " " + " ".join(perm) + "."
        sentences.append(sentence)
    return sentences

def rank_sentences(sentences):
    scored_sentences = [(sentence, score_sentence(sentence)) for sentence in sentences]
    return scored_sentences


words = {"John": ["likes", "spinach", "very", "much"], "Squirrels": ["live", "in", "the", "park"], "Last night, ": ["I met", "a wonderful woman who", "passionately talked about", "language models"], "This": ["is", "my", "example", "model"]}
for first_word, sentence in words.items():
    permutations = generate_permutations(sentence)
    sentences = generate_sentences(permutations, first_word)
    ranked_sentences = rank_sentences(sentences)

    print("Ranked sentences:")
    ranked_sentences.sort(key=lambda x: x[1], reverse=True)
    for sentence, rank in ranked_sentences:
        print(f"Rank: {rank}, sentence: {sentence}")
    print("\n")

chunks = [["study", "data science"], ["study data", "science"], ["study science", "data"], ["data study", "science"],
           ["data", "science study"], ["science", "study data"]]
first_word = "I"

for chunk in chunks:
    permutations = generate_permutations(chunk)
    sentences = generate_sentences(permutations, first_word)
    ranked_sentences = rank_sentences(sentences)

    print("Ranked sentences from chunks:")
    for sentence, rank in ranked_sentences:
        print(f"Rank: {rank}, sentence: {sentence}")
