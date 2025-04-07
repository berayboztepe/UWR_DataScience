from transformers import AutoTokenizer, AutoModel
import pandas as pd
import kagglehub

model_name = 'distilbert-base-uncased'
device = 'cpu'

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name).to(device)

def get_contextual_embedding(sentence):
    inputs = tokenizer(sentence, return_tensors='pt', truncation=True, padding=True, max_length=512).to(device)
    outputs = model(**inputs)
    cls_embedding = outputs.last_hidden_state[:, 0, :].detach().cpu().numpy().flatten()
    return cls_embedding

#path = kagglehub.dataset_download("yelp-dataset/yelp-dataset")
# reviews_file = path + '/yelp_academic_dataset_review.json'

sampled_reviews_file = r'C:\Users\beray\Code Projects\Language Models\Exercise_3\sampled_reviews_100k.csv'
sampled_reviews = pd.read_csv(sampled_reviews_file)
print("Loaded Sampled Reviews:")
print(sampled_reviews.head())

embeddings = []
for review in sampled_reviews['text']:
    embedding = get_contextual_embedding(review)
    embeddings.append(embedding)

embedding_dim = len(embeddings[0])
embeddings_df = pd.DataFrame(embeddings, columns=[f'feature_{i+1}' for i in range(embedding_dim)])
embeddings_df['review'] = sampled_reviews['text'].values

output_file = r"C:\Users\beray\Code Projects\Language Models\Exercise_3\yelp_contextual_embeddings_100k.csv"
embeddings_df.to_csv(output_file, index=False)
print(f"Contextual embeddings saved to {output_file}.")