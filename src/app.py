import json
import boto3
import uuid
from datetime import datetime
import os

# Initialize clients
bedrock = boto3.client('bedrock-runtime')
dynamodb = boto3.resource('dynamodb')
table_name = os.getenv('TABLE_NAME')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))
        
        # Parse input
        if 'body' not in event:
            return create_response(400, {'error': 'No body in request'})
            
        body = json.loads(event['body'])
        user_message = body.get('message', '')
        session_id = body.get('session_id', str(uuid.uuid4()))
        
        if not user_message:
            return create_response(400, {'error': 'No message provided'})
        
        # Retrieve or create session
        session = get_session(session_id)
        conversation_history = session.get('conversation', [])
        
        # Build prompt with conversation history
        prompt = build_prompt(user_message, conversation_history)
        print("Generated prompt:", prompt)
        
        # Call Bedrock
        try:
            response = bedrock.invoke_model(
                modelId='anthropic.claude-v2',
                body=json.dumps({
                    "prompt": prompt,
                    "max_tokens_to_sample": 1000,
                    "temperature": 0.5,
                    "top_p": 0.9,
                }),
                contentType='application/json',
                accept='application/json'
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            ai_response = response_body['completion'].strip()
            
        except Exception as e:
            print(f"Bedrock error: {str(e)}")
            ai_response = "I'm experiencing technical difficulties. Please try again later."
        
        # Update conversation history
        conversation_history.append({"role": "user", "content": user_message})
        conversation_history.append({"role": "assistant", "content": ai_response})
        
        # Save updated session
        update_session(session_id, conversation_history)
        
        return create_response(200, {
            'response': ai_response,
            'session_id': session_id,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return create_response(500, {'error': str(e)})

def create_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps(body)
    }

def build_prompt(user_message, conversation_history):
    system_prompt = """You are a helpful AI assistant. Provide clear, concise, and helpful responses.
    
Conversation history:"""
    
    # Build conversation context
    conversation_text = ""
    for turn in conversation_history[-6:]:
        role = "Human" if turn["role"] == "user" else "Assistant"
        conversation_text += f"\n\n{role}: {turn['content']}"
    
    if not conversation_text.strip():
        conversation_text = "\n\nNo previous conversation."
    
    prompt = f"""{system_prompt}{conversation_text}

Human: {user_message}

Assistant:"""
    
    return prompt

def get_session(session_id):
    try:
        response = table.get_item(Key={'sessionId': session_id})
        if 'Item' in response:
            return response['Item']
        return {'sessionId': session_id, 'conversation': []}
    except Exception as e:
        print(f"Error getting session: {str(e)}")
        return {'sessionId': session_id, 'conversation': []}

def update_session(session_id, conversation):
    try:
        table.put_item(
            Item={
                'sessionId': session_id,
                'conversation': conversation,
                'lastUpdated': datetime.now().isoformat()
            }
        )
    except Exception as e:
        print(f"Error updating session: {str(e)}")