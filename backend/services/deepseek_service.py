import json
import requests
from config.config import Config

class DeepSeekService:
    def __init__(self):
        self.api_key = Config.DEEPSEEK_API_KEY
        self.api_base = Config.DEEPSEEK_API_BASE
        self.model = Config.DEEPSEEK_MODEL

    def create_chat_completion(self, messages):
        url = f"{self.api_base}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": Config.TEMPERATURE,
            "max_tokens": Config.MAX_TOKENS,
            "stream": True
        }
        
        response = requests.post(url, headers=headers, json=data, stream=True)
        
        if response.status_code != 200:
            raise Exception(f"API请求失败: {response.text}")
            
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    json_str = line[6:]
                    if json_str.strip() == '[DONE]':
                        break
                    try:
                        chunk = json.loads(json_str)
                        if chunk.get('choices') and chunk['choices'][0].get('delta', {}).get('content'):
                            yield chunk['choices'][0]['delta']['content']
                    except json.JSONDecodeError:
                        continue
