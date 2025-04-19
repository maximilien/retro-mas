import os, csv, json

from dotenv import load_dotenv
from huggingface_hub import login

from smolagents import (
    Tool,
    CodeAgent,
    DuckDuckGoSearchTool,
    InferenceClientModel,
    LiteLLMModel
)

load_dotenv()
login(token=os.getenv('HF_TOKEN'))

# tools

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

# model

model = LiteLLMModel(model_id="gpt-4o-mini")

# data

data_path = './data/easyretro_pqca.csv'

# agents

went_well_agent = CodeAgent(
    name="went_well",
    tools=[FileReader()],
    model = model,
    description="list all rows in 'Went well' with corresponding 'Votes Went well' columns",
)

went_ok_agent = CodeAgent(
    name="went_ok",
    tools=[FileReader()],
    model = model,
    description=f"list all rows in 'Went OK' with corresponding 'Votes Went OK' columns",
)

to_improve_agent = CodeAgent(
    name="to_improve",
    tools=[FileReader()],
    model = model,
    description=f"list all rows in 'To improve' with corresponding 'Votes To improve' columns",
)

summary_agent = CodeAgent(
    name="summary",
    tools=[],
    model = model,
    description="Take the input list of text and votes and create a summary making sure that items that have highest vote is at the top.",
)

writer_agent = CodeAgent(
    name="writer",
    tools = [],
    model = model,
    description="Writes blog posts based on the data passed. Provide the research findings and desired tone/style.",
)

editor_agent = CodeAgent(
    name="editor",
    tools = [],
    model = model,
    description="Reviews and polishes the blog post based on the research and original task request. Order the final blog post and any lists in a way that is most engaging to someone working in AI. Provides the final, edited version in markdown.",
)

# Main Blog Writer Manager
retro_manager = CodeAgent(
    tools=[FileReader()],
    model=model,
    managed_agents=[went_well_agent, went_ok_agent, to_improve_agent, summary_agent, writer_agent, editor_agent],
    additional_authorized_imports=["re", "csv", "json"],

    description="""You are a retro manager. Coordinate between went_well, went_ok, to_improve, summary, writer, and editor teams.
    Follow these steps:
    1. Use went_well to gather 'Went well' data and 'Went well votes' as went_well_data
    2. Use went_ok to gather 'Went ok' and 'Went OK votes' as went_ok_data
    3. Use to_improve to gather 'To Improve' and 'To Improve votes' as to_improve_data
    4. Pass went_well_data to summary to create went_well_summary
    5. Pass went_ok_data to summary to create went_ok_summary
    6. Pass to_improve_data to summary to create to_improve_summary
    7. Pass went_well_summary, went_ok_summary, and to_improve_summary to writer to create a blog post as draft
    8. Send draft to editor for final polish
    9. Save the final markdown file
    """
)

def retro_summary(input_file, output_file):
    """
    Creates a summary of the retro using multiple agents

    Args:
        input_file (str): the file containing the retro data
        output_file (str): The filename to save the markdown post
    """
    result = retro_manager.run(f"""Create a summary of the retro in file: {input_file}
    1. First, get the went_well, went_ok, and to_improve data
    2. Then, write an engaging summary of each
    3. Finally, edit and polish the content
    """)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    print(f"Blog post has been saved to {output_file}")

    return result

print(data_path)
answer = retro_summary(data_path, 'retro_blog.md')
print(answer)