import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import random
import time
import os

n = 100

device = "cpu"

random.seed(time.time())

model_name = "eryk-mazus/polka-1.1b"

tokenizer = AutoTokenizer.from_pretrained(model_name, padding_side="left")
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_name, device_map="auto")


def gen_equation(digits, operator):
    a = random.randint(0, 10**digits)
    b = random.randint(1, 10**digits) if operator == "/" else random.randint(0, 10**digits)

    if operator == "+":
        return f"{a} {operator} {b} = {a + b}"
    elif operator == "-":
        return f"{a} {operator} {b} = {a - b}"
    elif operator == "*":
        return f"{a} {operator} {b} = {a * b}"
    elif operator == "/":
        return f"{a} {operator} {b} = {a // b}" if b != 0 else f"{a} {operator} {b} = undefined"


def gen_prompt(digits, operator, num_equations):
    prompt = ""
    for _ in range(num_equations):
        prompt += gen_equation(digits, operator) + "\n"
    end = prompt.rfind("=")
    return prompt[:end+1]


ops = ["ADD", "SUB", "MUL", "DIV"]

for op in ops:
    current_operator = ["+", "-", "*", "/"][ops.index(op)]

    for digits in [2, 3]:
        for num_eq in [1, 2, 3, 10]:
            directory = fr"C:\Users\beray\Code Projects\Language Models\Exercise_2\{op}"
            file_path = f"{directory}/output_{digits}_{num_eq}.txt"

            if not os.path.exists(directory):
                os.makedirs(directory)

            if not os.path.exists(file_path):
                with open(file_path, "w") as f:
                    print(f"File created: {file_path}")

            with open(file_path, "w") as outFile:

                correct = 0
                total = 0

                for i in range(n):
                    prompt = gen_prompt(digits, current_operator, num_eq)
                    model_inputs = tokenizer([prompt],
                                             return_tensors="pt").to(device)
                    with torch.no_grad():
                        generated_ids = model.generate(
                            **model_inputs,
                            max_new_tokens=digits+1,
                            do_sample=True,
                            penalty_alpha=0.6,
                            pad_token_id=tokenizer.eos_token_id,
                            top_k=1
                        )

                    output = tokenizer.batch_decode(
                        generated_ids, skip_special_tokens=True)[0]

                    output = output.split("\n")[num_eq-1]
                    if "=" in output:
                        generated = output.split("=")[1].strip()
                        try:
                            generated = int(generated)
                            expected = eval(prompt.split("\n")[num_eq - 1].split("=")[0].strip())
                            if generated == expected:
                                correct += 1
                            total += 1
                        except Exception as e:
                            total += 1
                    else:
                        print(f"Invalid output: {output}")
                
                    outFile.write(f"Prompt: {prompt}\nGenerated: {output}\nExpected: {expected}\nCorrect: {generated == expected}\n\n")

                accuracy = correct / total if total > 0 else 0
                print(f"Accuracy for {digits}-digit numbers with {num_eq} equations: {accuracy:.2f}")
                outFile.write(f"Accuracy for {digits}-digit numbers with {num_eq} equations: {accuracy:.2f}")