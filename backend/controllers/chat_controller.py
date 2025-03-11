from flask import Blueprint, request, jsonify, Response
from services.deepseek_service import DeepSeekService
from services.redis_store import RedisStore
import uuid
import json

chat_bp = Blueprint('chat', __name__)
deepseek_service = DeepSeekService()
redis_store = RedisStore()

@chat_bp.route('/conversations', methods=['GET'])
def get_conversations():
    """获取所有会话列表"""
    conversations = redis_store.get_conversations()
    return jsonify(conversations)

@chat_bp.route('/conversations', methods=['POST'])
def create_conversation():
    """创建新会话"""
    conv_id = str(uuid.uuid4())
    conversation = redis_store.create_conversation(conv_id)
    return jsonify(conversation)

@chat_bp.route('/conversations/<conv_id>', methods=['GET'])
def get_conversation(conv_id):
    """获取指定会话详情"""
    conversation = redis_store.get_conversation(conv_id)
    if not conversation:
        return jsonify({"error": "会话不存在"}), 404
    return jsonify(conversation)

@chat_bp.route('/conversations/<conv_id>', methods=['DELETE'])
def delete_conversation(conv_id):
    """删除指定会话"""
    success = redis_store.delete_conversation(conv_id)
    if not success:
        return jsonify({"error": "删除失败"}), 400
    return jsonify({"message": "删除成功"})

@chat_bp.route('/conversations/<conv_id>/messages', methods=['POST'])
def send_message(conv_id):
    """发送消息并获取AI回复"""
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({"error": "消息内容不能为空"}), 400
        
    # 保存用户消息
    user_message = {
        "role": "user",
        "content": data['content']
    }
    if not redis_store.add_message(conv_id, user_message):
        return jsonify({"error": "会话不存在"}), 404
        
    # 获取会话历史
    conversation = redis_store.get_conversation(conv_id)
    
    try:
        # 调用AI服务获取回复
        response = deepseek_service.create_chat_completion(conversation['messages'])
        
        # 保存AI回复
        assistant_message = {
            "role": "assistant",
            "content": ""
        }
        
        def generate():
            for chunk in response:
                assistant_message['content'] += chunk
                yield f"data: {chunk}\n\n"
            
            # 保存完整的AI回复
            redis_store.add_message(conv_id, assistant_message)
            yield "data: [DONE]\n\n"
            
        return generate(), {"Content-Type": "text/event-stream"}
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chat_bp.route('/chat/sse', methods=['GET'])
def chat_sse():
    """SSE聊天接口"""
    conversation_id = request.args.get('conversation_id')
    message = request.args.get('message')
    is_reasoning = request.args.get('is_reasoning', 'false').lower() == 'true'
    
    if not conversation_id or not message:
        return jsonify({"error": "参数不完整"}), 400
        
    # 保存用户消息
    user_message = {
        "role": "user",
        "content": message
    }
    if not redis_store.add_message(conversation_id, user_message):
        return jsonify({"error": "会话不存在"}), 404
        
    # 获取会话历史
    conversation = redis_store.get_conversation(conversation_id)
    
    try:
        # 调用AI服务获取回复
        response = deepseek_service.create_chat_completion(conversation['messages'], is_reasoning)
        
        # 保存AI回复
        assistant_message = {
            "role": "assistant",
            "content": ""
        }
        
        def generate():
            buffer = ""
            for chunk in response:
                buffer += chunk
                assistant_message['content'] += chunk
                
                # 当遇到句子结束符号或缓冲区达到一定大小时发送
                if any(char in buffer for char in ['。', '！', '？', '\n']) or len(buffer) >= 10:
                    yield f"data: {json.dumps({'content': buffer}, ensure_ascii=False)}\n\n"
                    buffer = ""
            
            # 发送剩余的内容
            if buffer:
                yield f"data: {json.dumps({'content': buffer}, ensure_ascii=False)}\n\n"
            
            # 保存完整的AI回复
            redis_store.add_message(conversation_id, assistant_message)
            yield "data: {\"done\": true}\n\n"
            
        return Response(generate(), mimetype='text/event-stream')
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500