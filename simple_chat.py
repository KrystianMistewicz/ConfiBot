"""
Author: Krystian Mistewicz
"""

import requests


class LocalLLM:
    def __init__(self, model, ollama_url):
        self.model = model
        self.url = ollama_url
        self.messages = []

    def chat(self, message):
        self.messages.append({"role": "user", "content": message})
        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "messages": self.messages,
                "stream": False,
            },
            stream=False
        )
        answer = response.json()["message"]["content"]
        self.messages.append({"role": "assistant", "content": answer})
        return answer


if __name__ == '__main__':
    model = "qwen2.5:3b"
    url = "http://localhost:11434/api/chat"
    lllm = LocalLLM(model, url)
    message = input("I am your local LLM. What would you like to ask?\n")
    response = lllm.chat(message)
    print(response)
