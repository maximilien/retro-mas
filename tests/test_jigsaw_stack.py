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

  # def test_easy_retro(self):    
  #   print(self.jigsaw)
  #   response = self.jigsaw.web.ai_scrape({
  #     "url": "https://easyretro.io/publicboard/YYae4J4PluNYsxlbv3irwOWZY4n2/e2686146-a560-4ed2-ba6e-01bd5329a848",
  #     "element_prompts": [
  #       "Went Well",
  #       "Went OK"
  #     ],
  #     'cookies': [{
  #       'name': '__session',
  #       'value': "eyJhbGciOiJSUzI1NiIsImtpZCI6Ijg1NzA4MWNhOWNiYjM3YzIzNDk4ZGQzOTQzYmYzNzFhMDU4ODNkMjgiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiTWljaGFlbCBNYXhpbWlsaWVuIChEck1heCkiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jSkl0eG1DSEEzNFBGbEdqMnluUWw5MkxXTWlEank0V3NSazV3clBxLXo3bWwwMzFNNGJTUT1zOTYtYyIsImxhc3RfYWN0aXZlIjoxNzQ0NjQyMTcyMzMxLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZnVucmV0cm8tcHJvIiwiYXVkIjoiZnVucmV0cm8tcHJvIiwiYXV0aF90aW1lIjoxNzQ1MDg1NjQyLCJ1c2VyX2lkIjoiWVlhZTRKNFBsdU5Zc3hsYnYzaXJ3T1daWTRuMiIsInN1YiI6IllZYWU0SjRQbHVOWXN4bGJ2M2lyd09XWlk0bjIiLCJpYXQiOjE3NDUwODU2NDUsImV4cCI6MTc0NTA4OTI0NSwiZW1haWwiOiJtbWF4aW1pbGllbkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjEwMzY1NTAxMzEyNjU5NjE5NzA5NyJdLCJlbWFpbCI6WyJtbWF4aW1pbGllbkBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.nb7XL5L4o-_NijOhRUher6Pok-XiDSWyJ3GsAL6SjeHSclnC4hyiIuG24JH7krJLbSrwS76dE2u_eeyEhcOtLkFQUKm_0Gq5vPgrj7itZp-g31rgwWuYtQaMe_bhNMKsxylc6xFdvkWKFjm02oJ9ai0JS__i_rJ2yuubyrv8vETg3ZO0GeftY0compaRyhwWD__eVZa5qKXxtwU5Gjka4mMq-Z2e1Eu4Fc9sihu2tsyRTIFMkzVydUbYZ_mVtu0-Cxf0SgZYQE3ynR6uxRu5PrsE3oT6mkmoyvDiYJpcuIeCvlI_DMyscxR3_2sZ8bZHATaJZJiKarq9QN_2lvsQ7w",
  #       'domain': 'https://easyretro.io/',
  #       'secure': True,
  #       'httpOnly': True
  #     }],
  #     'force_rotate_proxy': True
  #   })
  #   pretty_json = json.dumps(response, indent=4)
  #   print(pretty_json)
  #   self.assertTrue(response is not None)

  def test_jigsaw_pdf(self):
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