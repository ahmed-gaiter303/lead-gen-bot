from openai import OpenAI

class AIMessenger:
    def __init__(self, api_key=None):
        self.api_key = api_key
    
    def generate_message(self, lead_name, company, industry):
        # Mock messages - no need for API
        messages = [
            f"Hi {lead_name}! I saw you're at {company}. Let's connect!",
            f"Hi {lead_name}, I'm interested in collaborating with {company}.",
            f"Hey {lead_name}! Your work at {company} caught my attention.",
        ]
        return messages[hash(lead_name) % len(messages)]

