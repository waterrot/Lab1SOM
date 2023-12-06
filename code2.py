from openai import OpenAI
import pandas as pd
import unittest
import ast
import re

# Info:
dataset_path = 'bgg_dataset.csv'
api_key = OpenAI(api_key="")

Hi = "Hi"

# Class
class BoardGameMechanicsAnalyzer:
    def __init__(self, dataset_path, api_key):
        self.dataset_path = dataset_path
        self.api_key = api_key
        self.data = self.load_and_clean_dataset()

    def load_and_clean_dataset(self):
        df = pd.read_csv(self.dataset_path, sep=';')

        # Drop rows with missing values in 'Name', 'Year Published', or 'Mechanics' columns
        df = df.dropna(subset=['Name', 'Year Published', 'Mechanics'])

        return df

    def query_mechanics_with_chatgpt(self, game_name):
        # Prepare a prompt for ChatGPT
        prompt = f"Which mechanics does the game {game_name} has? Only give it in the form of a python list, no extra text"

        # Send the prompt to ChatGPT and get the response
        full_chatgpt_response = self.ask_chatgpt(prompt)

        # Extract the content from the ChatCompletionMessage
        response_content = full_chatgpt_response.content

        # Use regular expressions to find the Python list
        match = re.search(r'\[.*\]', response_content)

        # Extract the matched substring
        python_list_string = match.group(0)

        # make a list of the output
        chatgpt_response_list = ast.literal_eval(python_list_string)
        
        # output the results
        get_common = self.accuracy_chatgpt(chatgpt_response_list, game_name)
    
    def accuracy_chatgpt(self,chatgpt_response_list, game_name):
        df = pd.read_csv(self.dataset_path, sep=';')
        # Check if the item is in the 'Name' column
        if game_name in df['Name'].values:
            # Get the value corresponding to the specified item name
            mechanics_from_database = df.loc[df['Name'] == game_name, ['Mechanics']].values[0]
            # Convert the array to a list of strings
            mechanics_from_database_list = []

            # Iterate through the array and extract each string element
            for item in mechanics_from_database:
                # Split the item into individual mechanics
                mechanics = item.split(",")

                # Append each mechanic to the list
                for mechanic in mechanics:
                    mechanics_from_database_list.append(mechanic)
            mechanics_from_database_list = [item.strip() for item in mechanics_from_database_list]

        else:
            print(f"{game_name} not found in the dataset.")

        # compare the list of the db and chatgpt with each other
        common_elements = len(set(mechanics_from_database_list) & set(chatgpt_response_list))
        accuracy_compare = common_elements/len(mechanics_from_database_list)
        print(f"these are from the database: {mechanics_from_database_list}")
        print(f"this is from chatgpt: {chatgpt_response_list}")
        print(f"these are the common elements: {common_elements}")
        print(f"this is the accuracy: {accuracy_compare}")

    def ask_chatgpt(self, prompt):

        # Send the prompt to ChatGPT
        response = self.api_key.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )

        # Extract and return the generated response
        return response.choices[0].message


#show
analyzer = BoardGameMechanicsAnalyzer(dataset_path, api_key)
cleaned_data = analyzer.data

# Specify a game name and its associated mechanics
game_name = 'Pandemic Legacy: Season 1'

# Query ChatGPT about the accuracy of mechanics for the specified game
analyzer.query_mechanics_with_chatgpt(game_name)

