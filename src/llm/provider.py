from abc import ABC, abstractmethod
import os
import google.generativeai as genai
import groq
from anthropic import Anthropic

class LLMProvider(ABC):
    @abstractmethod
    def generate_tests(self, code: str, language: str) -> str:
        pass

class GroqProvider(LLMProvider):
    def __init__(self, api_key: str = None, model = "llama-3.1-8b-instant"):
        self.api_key = api_key or os.environ.get('GROQ_API_KEY')
        self.model = model
        self.client = groq.Groq(api_key=self.api_key)

    def generate_tests(self, code: str, language: str) -> str:
        prompt = f"Write unit tests for the following {language} code. Output only the code and no explanations.\n\n```{language}\n{code}\n```"
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
        )
        return response.choices[0].message.content

class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str = None, model: str = 'gemini-1.5-pro-latest'):
        self.api_key = api_key or os.environ.get('GEMINI_API_KEY')
        self.model = model
        genai.configure(api_key=self.api_key)

    def generate_tests(self, code: str, language: str) -> str:
        prompt = f"Write unit tests for the following {language} code. Output only the code and no explanations.\n\n```{language}\n{code}\n```"
        model = genai.GenerativeModel(self.model)
        response = model.generate_content(prompt)
        return response.text

class ClaudeProvider(LLMProvider):
    def __init__(self, api_key: str = None, model: str = 'claude-3-opus-20240229'):
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        self.model = model
        self.client = Anthropic(api_key=self.api_key)

    def generate_tests(self, code: str, language: str) -> str:
        prompt = f"Write unit tests for the following {language} code. Output only the code and no explanations.\n\n```{language}\n{code}\n```"
        response = self.client.messages.create(
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
        )
        return response.content[0].text

def get_llm_provider(provider_name: str, api_key: str = None) -> LLMProvider:
    provider_name = provider_name.lower()
    if provider_name == 'groq':
        return GroqProvider(api_key)
    elif provider_name == 'gemini':
        return GeminiProvider(api_key)
    elif provider_name == 'claude':
        return ClaudeProvider(api_key)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider_name}")
