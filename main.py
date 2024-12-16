import os
from openai import OpenAI
import csv
from dotenv import load_dotenv, find_dotenv
from prompts import *

# load the .env file
_ = load_dotenv(find_dotenv())

client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY")
)


script_dir = os.path.dirname(os.path.abspath(__file__))  # Current script's directory
transport_data = os.path.join(script_dir, "input", "shipments.csv") 
inquiries = os.path.join(script_dir, "input", "inquiries.csv") 


# initialize model settings
model = "gpt-4o-mini"
temperature = 0.2
max_tokens = 800


# function for reading csv
def read_csv(file):
    data = []
    with open(file, "r", newline = "") as csvfile:   # open csv in read mode
        csv_reader = csv.reader(csvfile)             # create a csv reader object
        for row in csv_reader:
            data.append(row)                         # add each row to the data list
        return data
    

# apply read_csv to input csv's
sample_data = read_csv(transport_data)
sample_data_str = "\n".join([",".join(row) for row in sample_data])

mails = read_csv(inquiries)
mails_str = "\n".join([",".join(row) for row in mails])


# prompts variables
system_message = system_message
prompt = generate_prompt(sample_data_str, mails_str)


# assistant function to execute model with prompt
def shipment_information_assistant():
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {   
                "role": "system", 
                "content": system_message
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )

    return completion.choices[0].message.content

result = shipment_information_assistant()


# save output file
output_file = os.path.join(script_dir, "output", "inquiries_answers.txt") 

with open(output_file, "w") as file:
    file.write(result)


# display results
print("\nAssistants answer: \n")
print(result)
