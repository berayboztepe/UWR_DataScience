from transformers import pipeline, set_seed

model_name = "gpt2"
set_seed(42)

def generate_responses(prompt, num_responses):
    generator = pipeline('text-generation', model=model_name)
    g = generator(prompt, max_new_tokens=15, num_return_sequences=num_responses)

    return g

# returning the shortest example
def select_optimal_response(responses):
    print("Optimal Response: ") 
    return min(responses, key=len) 

def print_responses(g, num_responses, prompt):
    print("Generated Responses: ")
    for i in range(num_responses):
        print(g[i]['generated_text'][len(prompt):])

dialogue_history = ["User: Hi, how are you?", "Bot: I'm doing well, thank you!"]
new_input = "User: What about you?"
prompt = " ".join(dialogue_history) + " " + new_input

num_responses = 3
responses = generate_responses(prompt, num_responses)
print_responses(responses, num_responses, prompt)

print("\n")
optimal_response = select_optimal_response(responses)
print(optimal_response['generated_text'])