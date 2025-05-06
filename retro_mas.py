# MIT License

# Copyright (c) 2025 dr.max

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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

class RetroMas:
    def __init__(self, data_path='./data/easyretro_pqca.csv', output_file='retro_blog.md'):
        self.model = LiteLLMModel(model_id="gpt-4o-mini")
        self.data_path = data_path
        self.output_file = output_file
        self._create_agents()
        self._create_retro_manager()

    def _create_agents(self):
        self.went_well_agent = CodeAgent(
            name="went_well",
            tools=[FileReader()],
            model = self.model,
            description="list all rows in 'Went well' with corresponding 'Votes Went well' columns",
        )

        self.went_ok_agent = CodeAgent(
            name="went_ok",
            tools=[FileReader()],
            model = self.model,
            description=f"list all rows in 'Went OK' with corresponding 'Votes Went OK' columns",
        )

        self.to_improve_agent = CodeAgent(
            name="to_improve",
            tools=[FileReader()],
            model = self.model,
            description=f"list all rows in 'To improve' with corresponding 'Votes To improve' columns",
        )

        self.action_items_agent = CodeAgent(
            name="action_items",
            tools=[FileReader()],
            model = self.model,
            description=f"list all rows in 'Action items' with corresponding 'Votes Action items' columns",
        )

        self.summary_agent = CodeAgent(
            name="summary",
            tools=[],
            model = self.model,
            description="Take the input list of text and votes and create a summary making sure that items that have highest vote is at the top.",
        )

        self.writer_agent = CodeAgent(
            name="writer",
            tools = [],
            model = self.model,
            description="Writes blog posts based on the data passed. Provide the research findings and desired tone/style.",
        )

        self.editor_agent = CodeAgent(
            name="editor",
            tools = [],
            model = self.model,
            description="Reviews and polishes the blog post based on the research and original task request. Order the final blog post and any lists in a way that is most engaging to someone working in AI. Provides the final, edited version in markdown.",
        )

    def _create_retro_manager(self):
        self.retro_manager = CodeAgent(
            tools=[FileReader()],
            model=self.model,
            managed_agents=[self.went_well_agent, self.went_ok_agent, self.to_improve_agent, self.action_items_agent, self.summary_agent, self.writer_agent, self.editor_agent],
            additional_authorized_imports=["re", "csv", "json"],

            description="""You are a retro manager. Coordinate between went_well, went_ok, to_improve, summary, writer, and editor teams.
            Follow these steps:
            1. Use went_well to gather 'Went well' data and 'Went well votes' as went_well_data
            2. Use went_ok to gather 'Went ok' and 'Went OK votes' as went_ok_data
            3. Use to_improve to gather 'To Improve' and 'To Improve votes' as to_improve_data
            4. Use action_items to gather 'Action items' and 'Action items votes' as action_items_data
            5. Pass went_well_data to summary to create went_well_summary
            6. Pass went_ok_data to summary to create went_ok_summary
            8. Pass to_improve_data to summary to create to_improve_summary
            9. Pass action_items_data to summary to create action_items_summary
            10. Pass went_well_summary, went_ok_summary, to_improve_summary, and action_items_summary to writer to create a blog post as draft
            11. Send draft to editor for final polish
            12. Save the final markdown file
            """
        )

    def retro_summary(self):
        """
        Creates a summary of the retro using multiple agents

        Args:
            input_file (str): the file containing the retro data
            output_file (str): The filename to save the markdown post
        """
        result = self.retro_manager.run(f"""Create a summary of the retro in file: {self.data_path}
        1. First, get the went_well, went_ok, to_improve, and action_items data
        2. Then, write an engaging summary of each
        3. Finally, edit and polish the content
        """)

        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"Blog post has been saved to {self.output_file}")

        return result
