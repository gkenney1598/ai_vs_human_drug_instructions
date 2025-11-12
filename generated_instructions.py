from openai import OpenAI
import pandas as pd

#build dataframe for instructions
drugs = pd.read_csv('drug_instructions.csv', encoding='utf-8')

client = OpenAI(api_key="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")

with open('example_drug.txt', 'r', encoding='utf-8') as file:
    example_drug = file.read()

prompt_messages = [
    {"role": "system", "content": "You are a doctor writing instructions for drug usage. You should answer the following questions for each drug: "
        "Why is this medication prescribed? How should this medicine be used? What special precautions should I follow? What special dietary instructions should I follow? "
        "What should I do if I forget a dose? What side effects can this medication cause? Write this in this format: {example_drug}" },
    {"role": "user", "content": f"Write instructions for these drugs: ibuprofen"}
]

try:
    response = client.chat.completions.create(
        model="gpt-5",
        messages=prompt_messages,
        response_format={"type": "text"}
    )
    instructions = response.choices[0].message['content']
    print(instructions)

except Exception as e:
    print("An error occurred:", e)



