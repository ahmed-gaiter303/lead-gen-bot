from openai import OpenAI
import os

class AIMessenger:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-3.5-turbo"
    
    def generate_message(self, lead_name, company, industry):
        """Generate personalized message for lead"""
        
        prompt = f"""
        Write a personalized, friendly outreach message to {lead_name} at {company} in the {industry} industry.
        
        The message should:
        - Be 2-3 sentences
        - Feel natural, not spammy
        - Mention something relevant to their industry
        - Include a call to action (CTA)
        - Be in English
        
        Just return the message, nothing else.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )
        
        return response.choices[0].message.content
    
    def generate_followup(self, lead_name, original_message):
        """Generate follow-up message"""
        
        prompt = f"""
        Write a follow-up message to {lead_name} after they didn't respond to:
        "{original_message}"
        
        The message should:
        - Be 2-3 sentences
        - Not be pushy
        - Reference the previous message subtly
        - Offer value or a new angle
        
        Just return the message, nothing else.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )
        
        return response.choices[0].message.content
