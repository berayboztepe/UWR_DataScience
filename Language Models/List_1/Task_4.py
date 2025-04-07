import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from torch.nn import functional as F
import random
import pandas as pd

model_name = 'eryk-mazus/polka-1.1b'
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
    return seq_log_probs.cpu().numpy()

def normalized_sentence_prob(txt):
    length = len(tokenizer(txt, return_tensors='pt')['input_ids'][0])
    return sentence_prob(txt) / length


questions = pd.read_csv("Language Models/Exercise_1/Materials_1/P1/task4_questions.txt",
                        sep="#",
                        header=None,
                        names=["question"],
                        encoding="utf-8")


categories = {
    "yes_noQuestions": "Czy",
    "howQuestions": "Jak",
    "how_manyQuestions": "Ile|Ilu",
    "whoQuestions": "Kto|Któr|któr",
    "whatQuestions": "Co | Czym | Czego"
}

question_categories = {}

otherQuestions = questions

for category, pattern in categories.items():
    question_categories[category] = otherQuestions[otherQuestions['question'].str.contains(pattern, na=True)]
    otherQuestions = otherQuestions[~otherQuestions['question'].str.contains(pattern, na=True)]


correct = pd.read_csv("Language Models/Exercise_1/Materials_1/P1/task4_answers.txt",
                      sep="#",
                      header=None,
                      names=['answer'],
                      encoding="utf-8")


outFile = open("Language Models/Exercise_1/found_answers_10.txt", "w", encoding="utf-8")

random.seed(42)

# frac 1 to shuffle entire dataframe
yes_noQuestions = question_categories['yes_noQuestions'].sample(frac=1)
howQuestions = question_categories['howQuestions'].sample(frac=1)
how_manyQuestions = question_categories['how_manyQuestions'].sample(frac=1)
whoQuestions = question_categories['whoQuestions'].sample(frac=1)
whatQuestions = question_categories['whatQuestions'].sample(frac=1)
otherQuestions = otherQuestions.sample(frac=1)


def few_shots(typeQ):
    lines = []
    for q in typeQ.itertuples():
        lines.append(f"[INST] {q.question} [/INST]\n{correct.loc[q.Index].answer}")
    return "\n".join(lines)

number_few_questions = 3

for q in questions[:10].itertuples():
    few = ""

    if "Czy" in q.question:
        few = few_shots(yes_noQuestions[:number_few_questions])
        yes_noQuestions = yes_noQuestions.sample(frac=1)

    elif "Jak" in q.question:
        few = few_shots(howQuestions[:number_few_questions])
        howQuestions = howQuestions.sample(frac=1)

    elif "Ile" in q.question or "Ilu" in q.question:
        few = few_shots(how_manyQuestions[:number_few_questions])
        how_manyQuestions = how_manyQuestions.sample(frac=1)

    elif "Kto" in q.question or "Któr" in q.question or "któr" in q.question:
        few = few_shots(whoQuestions[:number_few_questions])
        whoQuestions = whoQuestions.sample(frac=1)

    elif "Co" in q.question or "Czym" in q.question or "Czego" in q.question:
        few = few_shots(whatQuestions[:number_few_questions])
        whatQuestions = whatQuestions.sample(frac=1)

    else:
        few = few_shots(otherQuestions[:number_few_questions])
        otherQuestions = otherQuestions.sample(frac=1)


    query = few + f"\n[INST] {q.question} [/INST]\n"

    input = tokenizer(query, return_tensors='pt').to(device)

    output = model.generate(
        input["input_ids"],
        max_new_tokens=50,
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id).to(device)
    
    answer = tokenizer.decode(
        output[0], skip_special_tokens=True).split("\n")[1+(number_few_questions*2)]
    
    print(f'question: {q.question}\nanswer: {answer}\nprob: {normalized_sentence_prob(answer)}')
    outFile.write(answer + "\n")

outFile.close()