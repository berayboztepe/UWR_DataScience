import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "distilgpt2"
device = "cpu"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)

sample_reviews_path = r"C:\Users\beray\Code Projects\Language Models\Exercise_3\sampled_reviews_100.csv"
sampled_reviews = pd.read_csv(sample_reviews_path)
sampled_reviews['token_length'] = sampled_reviews['text'].apply(lambda x: len(tokenizer(x, return_tensors='pt')['input_ids'][0]))
max_token_length = sampled_reviews['token_length'].max()

def truncate_text_to_max_length(text, max_length):
    tokens = tokenizer(text, return_tensors="pt", truncation=True, max_length=max_length)
    return tokenizer.decode(tokens["input_ids"][0])

def generate_review_variants(review):
    truncated_review = truncate_text_to_max_length(review, max_token_length - 50)
    prompt = truncated_review + " This was such a great experience because"

    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    outputs = model.generate(inputs["input_ids"], max_new_tokens=50, num_return_sequences=3, do_sample=True)

    augmented_reviews = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
    return augmented_reviews

augmented_data = []
for _, row in sampled_reviews.iterrows():
    review = row['text']
    augmented_variants = generate_review_variants(review)
    for variant in augmented_variants:
        augmented_data.append({"original_review": review, "augmented_review": variant})

output_file = r"C:\Users\beray\Code Projects\Language Models\Exercise_3\sampled_reviews_3_b_100.csv"
augmented_df = pd.DataFrame(augmented_data)
augmented_df.to_csv(output_file, index=False)

print(f"Augmented reviews saved to {output_file}.")      


"""
Went for lunch and found that my burger was meh.  
What was obvious was that the focus of the burgers is the amount of different and random crap they 
can pile on it and not the flavor of the meat.  My burger patty seemed steamed and appeared to be a preformed patty, 
contrary to what is stated on the menu.    I can get ground beef from Kroger and make a burger that blows them out of the water.


Went for lunch and found that my burger was meh.  
What was obvious was that the focus of the burgers is the amount of different and random crap they 
can pile on it and not the flavor of the meat.  My burger patty seemed steamed and appeared to be a preformed patty, 
contrary to what is stated on the menu.    I can get ground beef from Kroger and make a burger that blows them out of the water. 
This was such a great experience because there were no other burgers on the menu (and no pretzels, or food from that company).Â     
Also I like my burgers a lot and have been able to enjoy a burger from the other chain (and as well). 


"""