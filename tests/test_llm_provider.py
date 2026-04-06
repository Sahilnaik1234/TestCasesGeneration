{"tests": [{"name": "Test GroqProvider with valid code", "code": "from abc import ABC, abstractmethod"}]}

{"tests": [{"name": "Test GroqProvider with invalid code", "code": "invalid code"}]}

{"tests": [{"name": "Test GeminiProvider with valid code", "code": "from abc import ABC, abstractmethod"}]}

{"tests": [{"name": "Test GeminiProvider with invalid code", "code": "invalid code"}]}

{"tests": [{"name": "Test ClaudeProvider with valid code", "code": "from abc import ABC, abstractmethod"}]}

{"tests": [{"name": "Test ClaudeProvider with invalid code", "code": "invalid code"}]}

{"tests": [{"name": "Test get_llm_provider with valid provider name", "code": "get_llm_provider(\"Groq\")"}]}

{"tests": [{"name": "Test get_llm_provider with invalid provider name", "code": "get_llm_provider(\"InvalidProvider\")"}]}

{"tests": [{"name": "Test get_llm_provider with custom api key", "code": "get_llm_provider(\"Groq\", api_key=\"custom_api_key\")"}]}

{"tests": [{"name": "Test get_llm_provider with missing api key", "code": "get_llm_provider(\"Groq\")"}]}