#!/usr/bin/env python3

from docling.document_converter import DocumentConverter

from unittest import TestCase

class TestDocling(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_docling_pdf(self):
        source = 'data/easy_retro_pqca.pdf'
        converter = DocumentConverter()
        result = converter.convert(source)
        markdown = result.document.export_to_markdown()
        self.assertTrue(markdown is not None)
        print(markdown)

if __name__ == '__main__':
    unittest.main()