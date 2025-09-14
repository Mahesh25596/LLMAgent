import requests
import json
import sys

class LLMAgentClient:
    def __init__(self, api_url):
        self.api_url = api_url
        self.session_id = None
        
    def send_message(self, message):
        payload = {
            'message': message,
            'session_id': self.session_id or 'test-session'
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers={'Content-Type': 'application/json'},
                data=json.dumps(payload),
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                self.session_id = data.get('session_id', self.session_id)
                return data['response']
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except requests.exceptions.RequestException as e:
            return f"Request failed: {str(e)}"

def main():
    # Get API URL from command line or use default
    if len(sys.argv) > 1:
        api_url = sys.argv[1]
    else:
        # Replace with your actual API URL from SAM outputs
        api_url = "https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/prod/chat"
    
    client = LLMAgentClient(api_url)
    print("LLM Agent Client - Type 'quit' to exit")
    print("=" * 50)
    print(f"Using API: {api_url}")
    
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['quit', 'exit', 'bye', '']:
                break
                
            print("Thinking...", end=" ", flush=True)
            response = client.send_message(user_input)
            print(f"\nAI: {response}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()