import os
import json
import re
from src.llm.provider import LLMProvider

class TestGenerator:
    def __init__(self, provider: LLMProvider):
        self.provider = provider
    
    def generate_tests_for_files(self, low_coverage_files: list):
        """
        Takes a list of file dictionaries with 'filename' and 'coverage'.
        Generates and saves tests to the disk based on LLM suggestions.
        """
        for file_info in low_coverage_files:
            filename = file_info['filename']
            if not os.path.exists(filename):
                print(f"Skipping {filename} as it does not exist in workspace.")
                continue
            
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"Generating tests for {filename} (coverage: {file_info['coverage']}%)")
            
            prompt = self._build_prompt(filename, content)
            
            # Using language 'json' wrapper just to tell provider to generate as plain text or json.
            # Our prompt asks for JSON output anyway.
            response = self.provider.generate_tests(prompt, "")
            
            self._parse_and_save_tests(response, filename)
            
    def _build_prompt(self, original_filename: str, code: str) -> str:
        return f"""
You are an expert AI test generator that supports any programming language.
I need you to write unit tests for the following file to improve its code coverage. 
The tests should be comprehensive.

Original File path: {original_filename}

Original Code:
```
{code}
```

Based on conventional project structures for this programming language (e.g., placing Python tests in a `tests/` directory with `test_` prefix, Java tests in `src/test/java/...`, or JS tests as `*.test.js`), decide where the test file should be written and what its exact full path should be.

Return your response EXCLUSIVELY as a JSON array of objects. Each object should have two keys: `test_file_path` and `test_code`. Example:
[
  {{
    "test_file_path": "tests/test_example.py",
    "test_code": "import unittest\\n..."
  }}
]

DO NOT output any markdown blocks like ```json around the response. Only output raw JSON exactly.
"""

    def _parse_and_save_tests(self, response: str, original_filename: str):
        # Clean response in case LLM added markdown code blocks
        clean_res = re.sub(r"^```json\s*", "", response.strip())
        clean_res = re.sub(r"^```\w*\s*", "", clean_res)
        clean_res = re.sub(r"```$", "", clean_res.strip())
        
        try:
            tests = json.loads(clean_res)
            for test in tests:
                test_path = test.get("test_file_path")
                test_code = test.get("test_code")
                
                if not test_path or not test_code:
                    continue
                
                # Make sure directories exist
                os.makedirs(os.path.dirname(test_path), exist_ok=True)
                
                # Append if exists or write new
                mode = 'a' if os.path.exists(test_path) else 'w'
                with open(test_path, mode, encoding='utf-8') as f:
                    if mode == 'a':
                        f.write("\n\n")
                    f.write(test_code)
                    
                print(f"Successfully wrote tests to {test_path}")
        except json.JSONDecodeError as e:
            print(f"Failed to parse LLM response for {original_filename} as JSON. Error: {e}")
            print(f"Raw response: {response}")
