import sys
import os
# Add the project root directory to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

import unittest
from main.main import save_text_to_file

class TestSaveInput(unittest.TestCase):
    def test_save_text_to_file(self):
        # Test text
        test_text = "This is a test text."
        # Test file path
        test_file_path = "favordb.txt"

        try:
            # Call the function in main.py to save text
            result = save_text_to_file(test_text, test_file_path)
            self.assertTrue(result)

            # Verify if the file exists
            self.assertTrue(os.path.exists(test_file_path))

            # Verify if the file content is correct
            with open(test_file_path, 'r', encoding='utf-8') as file:
                saved_text = file.read()
            self.assertEqual(saved_text, test_text)

        finally:
            # Clean up the test file
            if os.path.exists(test_file_path):
                os.remove(test_file_path)

if __name__ == '__main__':
    unittest.main()