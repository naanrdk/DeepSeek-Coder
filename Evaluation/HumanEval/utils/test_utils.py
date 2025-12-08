
import unittest
import sys
import os

# Add the directory containing the utils module to the path
sys.path.append(os.path.abspath("Evaluation/HumanEval"))

from utils.utils import extract_generation_code, get_function_name

class TestUtils(unittest.TestCase):
    def test_get_function_name_indented(self):
        question = 'class Solution:\n    def my_func(self, a):'
        lang = 'Python'
        func_name, func_prefix = get_function_name(question, lang)
        self.assertEqual(func_name, 'def my_func')
        self.assertEqual(func_prefix, 'class Solution:')

    def test_extract_generation_code_standard(self):
        example = {
            'task_id': 'test/1',
            'prompt': 'def my_func(a):\n',
            'output': '```python\n    return a + 1\n```'
        }
        res = extract_generation_code(example, 'python')
        self.assertIn('return a + 1', res['generation'])

    def test_extract_generation_code_with_space(self):
        example = {
            'task_id': 'test/3',
            'prompt': 'def my_func(a):\n',
            'output': '```python \n    return a + 1\n```'
        }
        res = extract_generation_code(example, 'python')
        self.assertIn('return a + 1', res['generation'])
        # Ensure it didn't fallback to raw output (which would contain backticks)
        # However, the generation format in utils is func_prefix + body.
        # body is extracted code block.
        # If fallback, it returns prompt + output.
        if '```' in res['generation']:
             self.fail("Extraction failed and fell back to raw output")

    def test_extract_generation_code_indented_func(self):
        example = {
            'task_id': 'test/indent',
            'prompt': 'class Solution:\n    def my_func(self, a):\n',
            'output': '```python\n        return a + 1\n```'
        }
        res = extract_generation_code(example, 'python')
        self.assertIn('return a + 1', res['generation'])
        self.assertIn('class Solution:', res['generation'])

if __name__ == '__main__':
    unittest.main()
