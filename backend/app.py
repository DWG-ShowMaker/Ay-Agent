from flask import Flask, request, Response, jsonify, copy_current_request_context
from flask_cors import CORS
from services.deepseek_service import DeepSeekService
from services.redis_store import RedisStore
from config.config import Config
import uuid
import json
import time

def create_app():
    app = Flask(__name__)
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "supports_credentials": True,
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    store = RedisStore()
    deepseek_service = DeepSeekService()
    
    @app.route('/api/conversations', methods=['GET'])
    def get_conversations():
        return jsonify(store.get_conversations())

    @app.route('/api/conversations', methods=['POST'])
    def create_conversation():
        conv_id = str(uuid.uuid4())
        conversation = store.create_conversation(conv_id)
        return jsonify(conversation)

    @app.route('/api/conversations/<conv_id>', methods=['GET'])
    def get_conversation_messages(conv_id):
        """获取指定对话的完整内容"""
        conversation = store.get_conversation(conv_id)
        if not conversation:
            return jsonify({"error": "对话不存在"}), 404
        return jsonify(conversation)

    @app.route('/api/conversations/<conv_id>', methods=['DELETE'])
    def delete_conversation(conv_id):
        """删除指定对话"""
        success = store.delete_conversation(conv_id)
        if not success:
            return jsonify({"error": "删除对话失败"}), 400
        return jsonify({"message": "对话已删除"})

    @app.route('/api/chat/sse')
    def chat_sse():
        message = request.args.get('message', '')
        conv_id = request.args.get('conversation_id')
        is_reasoning = request.args.get('is_reasoning', 'false').lower() == 'true'
        
        if not conv_id or not message:
            return Response(
                'data: {"type": "error", "content": "缺少必要参数"}\n\n',
                mimetype='text/event-stream'
            )

        @copy_current_request_context
        def generate():
            conversation = store.get_conversation(conv_id)
            if not conversation:
                yield 'data: {"type": "error", "content": "无效的会话ID"}\n\n'
                return

            # 构建消息
            current_message = {
                "role": "user",
                "content": message,
                "timestamp": int(time.time())
            }
            
            # 添加用户消息到存储
            store.add_message(conv_id, current_message)
            
            try:
                # 准备发送给AI的消息列表
                messages_for_ai = []
                
                # 添加系统角色的基础设置
                messages_for_ai.append({
                    "role": "system",
                    "content": "你是一个专业的AI助手，请用中文回答用户的问题。"
                })
                
                # 如果开启推理模式，添加推理提示
                if is_reasoning:
                    messages_for_ai.append({
                        "role": "system",
                        "content": """在回答问题时，请按照以下步骤进行思考：
1. 分析问题的关键点和需要考虑的方面
2. 基于已知信息进行逻辑推导
3. 总结推理过程并给出最终答案

请使用<think>标签来展示你的思考过程。
例如：
<think>
1. 分析：...
2. 推理：...
3. 结论：...
</think>

然后再给出最终答案。"""
                    })
                
                # 添加历史消息
                for msg in conversation['messages'][-5:]:  # 只取最近5条消息作为上下文
                    if msg['role'] in ['user', 'assistant']:
                        messages_for_ai.append({
                            "role": msg['role'],
                            "content": msg['content']
                        })
                
                # 添加当前消息
                messages_for_ai.append(current_message)
                
                # 调用AI服务
                assistant_message = {
                    "role": "assistant",
                    "content": "",
                    "timestamp": int(time.time())
                }
                
                for chunk in deepseek_service.create_chat_completion(messages_for_ai):
                    if chunk:
                        assistant_message["content"] += chunk
                        response_data = json.dumps({
                            "type": "message",
                            "content": chunk
                        })
                        yield f'data: {response_data}\n\n'
                
                # 保存AI的完整回复
                store.add_message(conv_id, assistant_message)
                yield 'data: {"type": "done"}\n\n'
                
            except Exception as e:
                print(f"Error in SSE: {str(e)}")
                error_data = json.dumps({
                    "type": "error",
                    "content": str(e)
                })
                yield f'data: {error_data}\n\n'

        return Response(
            generate(),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'X-Accel-Buffering': 'no',
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'text/event-stream;charset=utf-8'
            }
        )
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=Config.DEBUG, port=Config.PORT)
