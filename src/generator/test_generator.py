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
You are a test generator.

STRICT RULES:
- Output ONLY valid JSON
- No explanation
- No markdown (no ```json)
- No extra text
- JSON must be valid and complete

Format:
[
  {{
    "test_file_path": "tests/test_file.py",
    "test_code": "..."
  }}
]

Generate unit tests for:
{code}
"""

    def _parse_and_save_tests(self, response: str, original_filename: str):
        def extract_json(response: str):
            try:
                # Extract JSON array only
                match = re.search(r"\[.*\]", response, re.DOTALL)
                if match:
                    return json.loads(match.group(0))
                else:
                    raise ValueError("No JSON found")
            except Exception as e:
                print("JSON parsing failed:", e)
                print("Raw response:", response)
                return []

        tests = extract_json(response)
        
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
