from flask import Flask, request, Response, jsonify, copy_current_request_context
from flask_cors import CORS
from services.deepseek_service import DeepSeekService
from services.memory_store import MemoryStore
from config.config import Config
import uuid
import json

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
    
    store = MemoryStore()
    deepseek_service = DeepSeekService()
    
    @app.route('/api/conversations', methods=['GET'])
    def get_conversations():
        return jsonify(store.get_conversations())

    @app.route('/api/conversations', methods=['POST'])
    def create_conversation():
        conv_id = str(uuid.uuid4())
        conversation = store.create_conversation(conv_id)
        return jsonify(conversation)

    @app.route('/api/chat/sse')
    def chat_sse():
        message = request.args.get('message', '')
        conv_id = request.args.get('conversation_id')
        is_reasoning = request.args.get('is_reasoning', 'false').lower() == 'true'
        
        # 检查参数
        if not conv_id or not message:
            return Response(
                'data: {"type": "error", "content": "Missing required parameters"}\n\n',
                mimetype='text/event-stream'
            )

        @copy_current_request_context
        def generate():
            conversation = store.get_conversation(conv_id)
            if not conversation:
                yield 'data: {"type": "error", "content": "Invalid conversation ID"}\n\n'
                return

            # 添加用户消息
            store.add_message(conv_id, 'user', message)
            
            try:
                # 如果开启推理模式，添加推理提示
                messages = conversation['messages']
                if is_reasoning:
                    reasoning_prompt = """请使用以下步骤来回答：
1. 思考：分析问题的关键点和需要考虑的方面
2. 推理：基于已知信息进行逻辑推导
3. 得出结论：总结推理过程并给出最终答案
4. 思考过程要以<think></think>标签展示给用户你的思考过程
"""
                    messages.append({
                        "role": "system",
                        "content": reasoning_prompt
                    })

                for chunk in deepseek_service.create_chat_completion(messages):
                    if chunk:
                        response_data = json.dumps({
                            "type": "message",
                            "content": chunk
                        })
                        yield f'data: {response_data}\n\n'
                
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
