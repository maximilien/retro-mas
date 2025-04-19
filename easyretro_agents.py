import os, csv, json

from dotenv import load_dotenv
from huggingface_hub import login

from smolagents import Tool, CodeAgent, DuckDuckGoSearchTool, InferenceClientModel

load_dotenv()
login(token=os.getenv('HF_TOKEN'))

class CsvToJson(Tool):
    description = "Converts CSV content to JSON."
    name = "csv_to_json"
    inputs = {"csv_filepath": {"type": "string", "description": "Path to the CSV file to read"}}
    output_type = "string"

    def forward(self, csv_filepath: str) -> str:
        data = []
        with open(csv_filepath, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                data.append(row)
        return json.dump(data, file, indent=4)

class FileReader(Tool):
    description = "Reads the content of a file."
    name = "file_reader"
    inputs = {"file_path": {"type": "string", "description": "Path to the file to read"}}
    output_type = "string"

    def forward(self, file_path: str) -> str:
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            return f"Error: File not found at {file_path}"

class EasyRetroDataAgent():
    def run(self, data_path):
        agent = CodeAgent(tools=[FileReader(), DuckDuckGoSearchTool()], model=InferenceClientModel())
        return agent.run(f"Read file from {data_path} as a Dataframe list all rows in 'Went well' with corresponding 'Votes Went well' columns")

if __name__ == '__main__':
    response = EasyRetroDataAgent().run('./data/easyretro_pqca.csv')
    print(response)
