#!/usr/bin/env python3

from pathlib import Path
from docling.document_converter import DocumentConverter

from unittest import TestCase

class TestDocling(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_docling_pdf(self):
        source = Path('./data/easy_retro_pqca.pdf')
        source = "https://arxiv.org/pdf/2408.09869" 
        converter = DocumentConverter()
        result = converter.convert(source)
        markdown = result.document.export_to_markdown()
        self.assertTrue(markdown is not None)
        print(markdown)

if __name__ == '__main__':
    unittest.main()
