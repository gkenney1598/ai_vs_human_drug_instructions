from openai import OpenAI
import pandas as pd
import csv
import ast

with open('data/example_drug.txt', 'r', encoding='utf-8') as file: #example drug with no important warning about usage
    example_drug_no_warning = file.read()

with open('data/example_drug_w_warning.txt', 'r', encoding='utf-8') as file: #example drug with important warning about usage
    example_drug_w_warning = file.read()

#build dataframe to get drug names to pass to model
def generate(reword):

    drugs = pd.read_csv('data/edited_combined.csv', encoding='utf-8')
    drug_instructions = drugs[:500]["text"]
    drug_names = drugs[:500]["name"]

    #do not upload key!
    client = OpenAI()

    instructions = []

    prompt = [{}, {}];

    if reword:
        prompt[0] = {"role": "system", "content": "You are a doctor rewriting instructions for drug usage. "
            "You should rewrite all the instructions for each drug, making sure to answer all the same questions: Why is this medication prescribed? How should this medicine be used? What special precautions should I follow? What special dietary instructions should I follow? What should I do if I forget a dose? What side effects can this medication cause? Rewrite the instructions in the same format as the original. Return a dictionary with each response with the structure {'name': <drug_name>, 'instructions': <instructions>}. Do not include any new lines or \n"}
    else:
        prompt[0] = {"role": "system", "content": "You are a doctor writing instructions for drug usage. You should answer the following questions for each drug: "
                    "Why is this medication prescribed? How should this medicine be used? What special precautions should I follow? What special dietary instructions should I follow? "
                    "What should I do if I forget a dose? What side effects can this medication cause? Write this in this format if the drug does not need an"
                    "important warning about usage: {example_drug}. Write in this format if it does: {example_drug_w_warning} Create a dictionary with each response"
                    "with the structure {'name': <drug_name>, 'instructions': <instructions>}. Store all of the created dictionaries in a list"
                    "Do not include bullet points or '-' in the instructions" }


    x = 1 if reword else 10

    for i in range(0, 500, x):
        if reword:
            prompt[1] = {"role": "user", "content": f"Rewrite these instructions: {drug_instructions[i]} for the drug {drug_names[i]}"}
        else:
            prompt[1] = {"role": "user", "content": f"Write instructions for all of these drugs: {drug_names[i:i+10]}"}

        try:
            response = client.responses.parse(
                model="gpt-5",
                input=prompt
            )
            instruct = ast.literal_eval(response.output_text) #convert returned string to list of dicts
            instructions.append(instruct)
            print(i)

        except Exception as e:
            print("An error occurred:", e)


    with open('data/generated_drug_instructions.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'instructions']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        if reword:
            writer.writerows(instructions)
        else:
            for row in instructions: #write each instruction in each row into the csv
                writer.writerows(i for i in row)

def main():
    generate(True)

main()




