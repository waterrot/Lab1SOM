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

    def get_input_data(self):
        input_data = []
        with open('game_list.txt', 'r') as file:
            for line in file:
                items = line.split(";")
                game_info = {}

                for index, item in enumerate(items):
                    if index % 2 == 0:
                        game_info['Name'] = item.strip()
                    else:
                        game_info['Year Published'] = item.strip()

                input_data.append(game_info)

        return input_data

    def query_mechanics_with_chatgpt(self):
        # import the data from the input txt file
        input_data = self.get_input_data()
        
        # Prepare a prompt for ChatGPT
        prompt = f"Add for each of the following games an extra key to the dict named 'Mechanics'. add to the value a string with the mechanics from that game (corresponding to the right publish year). Since there can be and probably will be multiple mechanics seperate these mechanics within the string with a comma, and if there is no mechanic add a value of 'No mechanic found'. Give no extra text as answer, only the new dictionary. {input_data}"
        
        # Send the prompt to ChatGPT and get the response
        full_chatgpt_response = self.ask_chatgpt(prompt)

        # Extract the content from the ChatCompletionMessage
        response_content = full_chatgpt_response.content

        # Use regular expressions to find the Python list
        match = re.search(r'\[.*\]', response_content)

        if match:
            # Extract the matched substring
            python_dict_string = match.group(0)

            try:
                # Use the ast module to safely convert the string to a Python dictionary
                chatgpt_response_dict = ast.literal_eval(python_dict_string)
                # Now, 'python_dict' contains the dictionary of mechanics
                print(chatgpt_response_dict)
            except (SyntaxError, ValueError) as e:
                print(f"Error converting string to dictionary: {e}")

        else:
            print("No Python dictionary found in the response.")

        #get_common = self.accuracy_chatgpt(chatgpt_response_dict, game_name)
        #print(chatgpt_response_dict)
    

    def accuracy_chatgpt(self,chatgpt_response_dict, game_name):
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
            max_tokens=250
        )

        # Extract and return the generated response
        return response.choices[0].message

#show
analyzer = BoardGameMechanicsAnalyzer(dataset_path, api_key)
cleaned_data = analyzer.data

# Query ChatGPT about the accuracy of mechanics for the specified game
analyzer.query_mechanics_with_chatgpt()


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