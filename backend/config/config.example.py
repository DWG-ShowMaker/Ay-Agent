import os

class Config:
    # 基础配置
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    PORT = int(os.getenv('PORT', 5000))
    
    # Redis配置
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)  # 如果Redis没有密码，设为None
    
    # DeepSeek配置
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
    DEEPSEEK_API_BASE = os.getenv('DEEPSEEK_API_BASE', '')
    
    # API配置
    DEEPSEEK_CHAT_MODEL = "deepseek-chat"
    DEEPSEEK_REASONER_MODEL = "deepseek-reasoner"
    
    # 默认参数
    MAX_TOKENS = 4096
    TEMPERATURE = 0.7
