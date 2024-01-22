from openai import OpenAI
import pandas as pd
import time
import unittest
import ast
import re

# Info:
dataset_path = 'bgg_dataset.csv'
api_key = OpenAI(api_key="")

# Class
class BoardGameMechanicsAnalyzer:
    def __init__(self, dataset_path, api_key):
        self.dataset = dataset_path
        self.api_key = api_key
        self.data = self.load_and_clean_dataset()
        self.df = self.load_and_clean_dataset()

    def load_and_clean_dataset(self):
        df = pd.read_csv(dataset_path, sep=';')

        # Drop rows with missing values in 'Name', 'Year Published', or 'Mechanics' columns
        df = df.dropna(subset=['Name', 'Year Published', 'Mechanics'])

        return df

    def _split_mechanics(self, mechanics_string):
        # Split the mechanics string into a list of mechanics
        return mechanics_string.split(', ')

    def get_input_data(self):
        input_data = []
        with open('game_list.txt', 'r') as file:

            # make the data readable
            all_data = file.read()
            line_data = all_data.split("\n")

            # make a tuple of the data
            for line in line_data:
                input_data.append((line.split(";")[0], int(line.split(";")[1])))

        return input_data

    def query_mechanics_with_chatgpt(self, game_name, game_mechanics):
        # Prepare a prompt for ChatGPT
        prompt = f"For the game {game_name}, which of the following mechanics apply to the game: {', '.join(game_mechanics)}. Don't introduce your answer, return only the mechanics, seperated by semicolons."

        # Send the prompt to ChatGPT
        response = self.api_key.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )

        # Extract and return the generated response
        return response.choices[0].message

    def accuracy_chatgpt(self, game_list):

        total_accuracy = 0
        total_games = 0

        for game_name, year_published in game_list:
            game_row = self.dataset[(self.dataset['Name'] == game_name) & (self.dataset['Year Published'] == year_published)]

            # Check if game in dataset
            if not game_row.empty:
                game_mechanics = self._split_mechanics(game_row['Mechanics'].iloc[0])
                chatgpt_response = self.query_chatgpt(game_name, game_mechanics)
                response_list = chatgpt_response.split(';')

                # Calculate accuracy for the current game
                accuracy = len(response_list) / len(game_mechanics)
                print("Accuracy for "+game_name+"("+str(year_published)+"): "+str(accuracy * 100)+"%")

                # Keep count of total accuracy and total games
                total_accuracy += accuracy
                total_games += 1
                mean_accuracy = total_accuracy / total_games
                print(f"Mean accuracy at {str(total_games)} amount of games: {str(mean_accuracy * 100)}%")
                #Delay because of rate limits
                time.sleep(20)  
            else:
                print("Game not found in dataset")
        # Calculate mean accuracy
        if total_games > 0:
            mean_accuracy = total_accuracy / total_games
            print(f"Mean accuracy for all games: {str(mean_accuracy * 100)}%")
        else:
            print("No valid games found in the provided list.")


    def mean_top_200(self):
        df = pd.read_csv(dataset_path, sep=';')
        
        # Convert 'Rating Average' to numeric
        copy_dataset = pd.DataFrame.from_dict(df)
        copy_dataset['Rating Average'] = pd.to_numeric(copy_dataset['Rating Average'], errors='coerce')

        # Find 200 highest rated games
        top_200 = copy_dataset.nlargest(200, 'Rating Average')
        top_200_list = [(row['Name'], row['Year Published']) for index, row in top_200.iterrows()]
        print(top_200_list)

        # Convert Rating Average to integer and get accuracy for games
        accuracy = self.accuracy_chatgpt(top_200_list)
        return accuracy

#show
analyzer = BoardGameMechanicsAnalyzer(dataset_path, api_key)
cleaned_data = analyzer.data

# Query ChatGPT about the accuracy of mechanics for the specified game
analyzer.mean_top_200()


class test_class(unittest.TestCase):

    def test_dataframe_clean(self):
        # test if empty collums have acctualy been removed from the database
        self.assertTrue(analyzer.data['Name'].notnull().all(), "Missing values in 'Name' column")
        self.assertTrue(analyzer.data['Year Published'].notnull().all(), "Missing values in 'Year Published' column")
        self.assertTrue(analyzer.data['Mechanics'].notnull().all(), "Missing values in 'Mechanics' column")
    
    def test_api_unreachable_error(self):
        # Assume chat_gpt_function sends a request to the ChatGPT API
        # For the sake of this example, let's mock the function to simulate an API unreachable scenario
        with unittest.mock.patch('analyzer.ask_chatgpt') as mock_function:
            # Set the side effect of the mock function to raise a ConnectionError
            mock_function.side_effect = ConnectionError("Unable to reach ChatGPT API")

            # Call the function and expect it to raise a ConnectionError
            with self.assertRaises(ConnectionError):
                ask_chatgpt("Hello, ChatGPT!")

if __name__ == '__main__':
    unittest.main()