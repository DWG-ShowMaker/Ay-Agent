class MemoryStore:
    def __init__(self):
        self.conversations = {}
        
    def get_conversations(self):
        return list(self.conversations.values())
        
    def get_conversation(self, conv_id):
        return self.conversations.get(conv_id)
        
    def create_conversation(self, conv_id, title="新对话"):
        conversation = {
            'id': conv_id,
            'title': title,
            'messages': []
        }
        self.conversations[conv_id] = conversation
        return conversation
        
    def add_message(self, conv_id, role, content):
        if conv_id not in self.conversations:
            return None
        message = {'role': role, 'content': content}
        self.conversations[conv_id]['messages'].append(message)
        return message
