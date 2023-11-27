import pandas as pd
from openai import OpenAI

# Info:
dataset_path = 'bgg_dataset.csv'
api_key = OpenAI(api_key="")


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

    def query_mechanics_with_chatgpt(self, game_name, mechanics_list):
        # Prepare a prompt for ChatGPT
        prompt = f"Verify which mechanics for the game {game_name} are accurate: {', '.join(mechanics_list)}"

        # Send the prompt to ChatGPT and get the response
        chatgpt_response = self.ask_chatgpt(prompt)

        # Print the response
        print(f"ChatGPT response for {game_name} mechanics verification:\n{chatgpt_response}")

    def ask_chatgpt(self, prompt):
        # Send the prompt to ChatGPT
        response = api_key.completions.create(
            engine="gpt-3.5-turbo", 
            prompt=prompt,
            max_tokens=150
        )

        # Extract and return the generated response
        return response['choices'][0]['text']


#show
analyzer = BoardGameMechanicsAnalyzer(dataset_path, api_key)
cleaned_data = analyzer.data

# Specify a game name and its associated mechanics
game_name = 'Gloomhaven'
mechanics_list = ['Action Queue', 'Action Retrieval', 'Campaign / Battle Card Driven']

# Query ChatGPT about the accuracy of mechanics for the specified game
analyzer.query_mechanics_with_chatgpt(game_name, mechanics_list)