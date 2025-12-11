# Overview

Our project aimed to identify if a model could be trained to predict whether or not a set of instructions for a drug was human-generated or AI-generated. This is important because  people are turning to AI for medical instructions and it is vital that the information they are receiving is accurate. We found that our model is very easily able to distinguish between human-generated and AI-generated drug instructions, and we also found that texts that were more similar in terms of wording and content were more likely to be mislabeled; however, the model was still incredibly accurate in its labeling. 

# Research Question

Can we train a model to predict whether or not a set of instructions for a drug is human-generated or AI-generated?

# Replication Instructions
Install [MiniForge](https://github.com/conda-forge/miniforge). Download all files from this repository to a folder and navigate to it. Run the following commands in Miniforge to download necessary libraries and activate environment:

```
$ conda env create -f environment.yml
$ conda activate ml
```
Download the additional dependencies: 
+ [nltk](https://www.nltk.org/)
+ [OpenAI API](https://platform.openai.com/docs/quickstart)
+ [Transformers](https://huggingface.co/docs/transformers/en/installation)
+ [Datasets](https://huggingface.co/docs/datasets/en/installation)
+ [bs4](https://pypi.org/project/beautifulsoup4/)

In order to run the generate_instructions.py, you will need your own OpenAI API key.
Run model.py to train model on a dataset and get results.

# Data

## Data Collection 

### Human-Generated Instructions

To begin, we created an excel spreadsheet and manually added 500 identification codes which we obtained for MedlinePlus. This is a government website that contains instructions for drug usage. We used the identification codes to then scrape MedlinePlus and create a CSV with descriptions of all of these medications. This included sections such as "Why is this medication prescribed?", "How should this medication be used?", "Other uses for this medicine", "What special precautions should I follow?", and "What special dietary instruction should I follow?"

### AI-Generated Instructions

Using the OpenAI API, we prompted ChatGPT-5 with the same 500 drugs and an example output of two medications we did not include in our dataset. We put all of the generated medication instructions into a CSV. 

### AI-Reworded Instructions

Using the OpenAI API, ChatGPT was separately prompted to reword all the MedlinePlus drug instructions.

## Data Organization
With the MedlinePlus, generated and reworded instructions, we created three CSV files: 
- Human-Generated and AI-Generated instructions
- Human-Generated and AI-reworded instructions
- AI-Generated and AI-reworded instructions

# Model

We used the RoBERTa for Sequence Classification model. This model utilizes supervised learning with the preassigned labels to determine if it can accurately distinguish between Human-Generated instructions, AI-Generated instructions and AI-Reworded instructions.

# Future Directions

Our model was extremely accurate, but AI is still known to hallucinate or give false information, so further investigation must be done to more accurately represent these interactions. Therefore, future research should focus on a less formal formatting and should have a more varied data set. Real interactions between humans and AI must be mimicked to gain a better understanding of what type of information AI is providing to humans. Our study was a very specific instance where we used one data set of medications and we had prompted AI to generate the same content, but this does not mimic how humans actually interact with AI nor does it mimic how patients interact with medical experts. Although we analyze how similar the content is, we do not evaluate the accuracy of the medical information provided so this should also be part of future research.

# Contributions

[Dilni Pathirana](https://github.com/dilnipath)
[Morgan Greenwald](https://github.com/Morgans-Code)
Grace Kenney

All three of us contributed equal time to this project.
