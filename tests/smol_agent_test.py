#!/usr/bin/env python3

import os

from dotenv import load_dotenv
from huggingface_hub import login

from smolagents import CodeAgent, DuckDuckGoSearchTool, InferenceClientModel

load_dotenv()

class TestSmolAgent():
    def setUp(self):
        login(token=os.getenv('HF_TOKEN'))
        self.model = InferenceClientModel()

    def tearDown(self):
        self.model = None

    def test_simple_agent(self):
        agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=self.model)
        response = agent.run("How many seconds would it take for a leopard at full speed to run through Pont des Arts?")
        print(response)

if __name__ == '__main__':
    test = TestSmolAgent()
    test.setUp()
    test.test_simple_agent()