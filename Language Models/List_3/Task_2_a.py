import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from torch.nn import functional as F
import pandas as pd
import kagglehub

model_name = 'distilgpt2'
device = 'cpu'

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)

path = kagglehub.dataset_download("yelp-dataset/yelp-dataset")
print("Path to dataset files:", path)

reviews_file = path + '/yelp_academic_dataset_review.json'
reviews = pd.read_json(reviews_file, lines=True)
reviews = reviews[['text']].sample(100, random_state=42)
print(reviews.head())

reviews.to_csv(r'C:\Users\beray\Code Projects\Language Models\Exercise_3\sampled_reviews_100.csv', index=False)
print("Sampled reviews saved to 'reviews.csv_100'.")

#sampled_reviews_file = r'C:\Users\beray\Code Projects\Language Models\Exercise_3\sampled_reviews.csv'
#sampled_reviews = pd.read_csv(sampled_reviews_file)
#print("Loaded Sampled Reviews:")
#print(sampled_reviews.head())

def log_probs_from_logits(logits, labels):
    logp = F.log_softmax(logits, dim=-1)
    logp_label = torch.gather(logp, 2, labels.unsqueeze(2)).squeeze(-1)
    return logp_label

def sentence_prob(sentence_txt):
    input_ids = tokenizer(sentence_txt, return_tensors='pt', truncation=True, max_length=1024)['input_ids'].to(device)
    length = input_ids.shape[1]
    with torch.no_grad():
        output = model(input_ids=input_ids)
        log_probs = log_probs_from_logits(
            output.logits[:, :-1, :], input_ids[:, 1:]
        )
        seq_log_probs = torch.sum(log_probs)
    return seq_log_probs.cpu().numpy() / length

def rate_sentence(sentence_txt):
    posSentence = sentence_txt + " - I absolutely loved it!"
    negSentence = sentence_txt + " - I hated it so much!"
    
    probP = sentence_prob(posSentence)
    probN = sentence_prob(negSentence)
    return probP, probN, probP - probN

results = []
#for review in sampled_reviews['text']:
for review in reviews['text']:
    probP, probN, diff = rate_sentence(review)
    results.append({'review': review, 'positive_score': probP, 'negative_score': probN, 'sentiment_diff': diff})

results_df = pd.DataFrame(results)
results_df['predicted_sentiment'] = results_df['sentiment_diff'].apply(lambda x: 'Positive' if x > 0 else 'Negative')

results_df.to_csv(r'C:\Users\beray\Code Projects\Language Models\Exercise_3\yelp_sentiment_results_100.csv', index=False)
print("Sentiment analysis completed. Results saved to 'yelp_sentiment_results_100k.csv'.")


