import redis
import json
import time
from config.config import Config

class RedisStore:
    def __init__(self):
        self.redis = redis.Redis(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            password=Config.REDIS_PASSWORD,
            decode_responses=True
        )
        
    def _get_conversation_key(self, conv_id):
        return f"conversation:{conv_id}"
        
    def _get_conversations_list_key(self):
        return "conversations:list"
    
    def create_conversation(self, conv_id):
        """创建新的会话"""
        conversation = {
            "id": conv_id,
            "title": "新对话",
            "created_at": int(time.time()),
            "messages": []
        }
        
        # 保存会话信息
        conv_key = self._get_conversation_key(conv_id)
        self.redis.set(conv_key, json.dumps(conversation))
        
        # 添加到会话列表
        self.redis.lpush(self._get_conversations_list_key(), conv_id)
        
        return conversation
    
    def get_conversation(self, conv_id):
        """获取指定会话"""
        conv_key = self._get_conversation_key(conv_id)
        conv_data = self.redis.get(conv_key)
        if conv_data:
            return json.loads(conv_data)
        return None
    
    def get_conversations(self):
        """获取所有会话列表"""
        conv_ids = self.redis.lrange(self._get_conversations_list_key(), 0, -1)
        conversations = []
        
        for conv_id in conv_ids:
            conv_data = self.get_conversation(conv_id)
            if conv_data:
                # 只返回基本信息，不包含消息内容
                conversations.append({
                    "id": conv_data["id"],
                    "title": conv_data["title"],
                    "created_at": conv_data["created_at"]
                })
        
        return conversations
    
    def add_message(self, conv_id, message):
        """添加消息到会话"""
        conversation = self.get_conversation(conv_id)
        if not conversation:
            return False
            
        # 添加消息
        conversation["messages"].append(message)
        
        # 如果是用户的第一条消息，更新会话标题
        if message["role"] == "user" and len(conversation["messages"]) == 1:
            # 使用用户的第一条消息作为会话标题
            title = message["content"][:20] + ("..." if len(message["content"]) > 20 else "")
            conversation["title"] = title
        
        # 保存更新后的会话
        conv_key = self._get_conversation_key(conv_id)
        self.redis.set(conv_key, json.dumps(conversation))
        
        return True
    
    def delete_conversation(self, conv_id):
        """删除会话"""
        # 从Redis中删除会话数据
        conv_key = self._get_conversation_key(conv_id)
        self.redis.delete(conv_key)
        
        # 从会话列表中移除
        self.redis.lrem(self._get_conversations_list_key(), 0, conv_id)
        
        return True 