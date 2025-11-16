import requests
from bs4 import BeautifulSoup

class LeadScraper:
    """Simple lead scraper - for portfolio purposes"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_sample_leads(self):
        """
        Sample leads for demo purposes.
        In real production, you'd integrate with APIs like:
        - Hunter.io
        - RocketReach
        - Apollo
        - Clearbit
        """
        
        sample_leads = [
            {
                "name": "Ahmed Hassan",
                "email": "ahmed@techstartup.com",
                "company": "TechStartup",
                "industry": "Technology"
            },
            {
                "name": "Sara Mohamed",
                "email": "sara@ecommerce.com",
                "company": "Ecommerce Plus",
                "industry": "E-commerce"
            },
            {
                "name": "John Smith",
                "email": "john@consulting.com",
                "company": "Consulting Group",
                "industry": "Consulting"
            }
        ]
        
        return sample_leads
    
    def validate_email(self, email):
        """Basic email validation"""
        return "@" in email and "." in email
