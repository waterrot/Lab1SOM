import pandas as pd
from openai import OpenAI

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
      
      
    def ChatGPT_mechanic_accuracy(self, game_name):
      mechanics_list = df.loc[df['name'] == game_name, 'mechanics'].values
      return f"{mechanics_list}"
        


# Info:
dataset_path = 'bgg_dataset.csv'
api_key = OpenAI(api_key="hierzo")
analyzer = BoardGameMechanicsAnalyzer(dataset_path, api_key)

game_name = 'Gloomhaven'
#show df
cleaned_data = analyzer.data
print(cleaned_data)

mech = analyzer.ChatGPT_mechanic_accuracy
print(mech)
