#!/usr/bin/env python3

import os, json, unittest

from unittest import TestCase
from dotenv import load_dotenv
from jigsawstack import JigsawStack

load_dotenv()

class TestJigsaw(TestCase):
  def setUp(self):
    self.jigsaw = JigsawStack(api_key=os.getenv('JIGSAW_STACK_API_KEY'))

  def tearDown(self):
    self.jigsaw = None

  def _test_jigsaw_web(self):
    response = self.jigsaw.web.ai_scrape({
      "url": "https://news.ycombinator.com/show",
      "element_prompts": [
        "post title",
        "post points"
      ]
    })
    pretty_json = json.dumps(response, indent=4)
    print(pretty_json)
    self.assertTrue(response is not None)

if __name__ == '__main__':
    unittest.main()