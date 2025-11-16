import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    filters, ContextTypes, CallbackQueryHandler
)
from config import TELEGRAM_BOT_TOKEN, OPENAI_API_KEY
from database import Database
from ai_messages import AIMessenger
from lead_scraper import LeadScraper

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize
db = Database()
ai = AIMessenger(OPENAI_API_KEY)
scraper = LeadScraper()

class LeadGenBot:
    def __init__(self):
        self.db = db
        self.ai = ai
        self.scraper = scraper
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command"""
        keyboard = [
            [InlineKeyboardButton("📊 Load Sample Leads", callback_data="load_leads")],
            [InlineKeyboardButton("📧 Generate Messages", callback_data="gen_messages")],
            [InlineKeyboardButton("📈 View Stats", callback_data="view_stats")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🤖 Welcome to AI Lead Generation Bot!\n\n"
            "I help you:\n"
            "✅ Collect leads\n"
            "✅ Generate personalized messages\n"
            "✅ Track engagement\n\n"
            "What would you like to do?",
            reply_markup=reply_markup
        )
    
    async def load_sample_leads(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Load sample leads"""
        leads = self.scraper.scrape_sample_leads()
        
        for lead in leads:
            self.db.add_lead(
                lead["name"], 
                lead["email"], 
                lead["company"]
            )
        
        await update.callback_query.edit_message_text(
            text=f"✅ Loaded {len(leads)} sample leads!\n\n"
                 "Now you can generate personalized messages for each."
        )
    
    async def generate_messages(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Generate AI messages"""
        leads = self.db.get_leads(status='new')
        
        if not leads:
            await update.callback_query.edit_message_text(
                text="📭 No leads to process. Load leads first!"
            )
            return
        
        messages_generated = 0
        
        for lead in leads[:3]:  # First 3 for demo
            lead_id, name, email, company = lead[0], lead[1], lead[2], lead[3]
            
            try:
                # Generate message using AI
                message = self.ai.generate_message(name, company, "Technology")
                
                # Save to database
                self.db.save_message(lead_id, message)
                self.db.update_lead_status(lead_id, 'contacted')
                
                messages_generated += 1
                
            except Exception as e:
                logger.error(f"Error generating message: {e}")
        
        await update.callback_query.edit_message_text(
            text=f"📧 Generated {messages_generated} personalized messages!\n\n"
                 "Messages are ready to be sent."
        )
    
    async def view_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """View statistics"""
        new_leads = len(self.db.get_leads('new'))
        contacted = len(self.db.get_leads('contacted'))
        
        await update.callback_query.edit_message_text(
            text=f"📈 Lead Generation Stats:\n\n"
                 f"🆕 New Leads: {new_leads}\n"
                 f"📧 Contacted: {contacted}\n"
                 f"📊 Total: {new_leads + contacted}"
        )
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button clicks"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "load_leads":
            await self.load_sample_leads(update, context)
        elif query.data == "gen_messages":
            await self.generate_messages(update, context)
        elif query.data == "view_stats":
            await self.view_stats(update, context)

async def main():
    """Start the bot"""
    bot = LeadGenBot()
    
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", bot.start))
    app.add_handler(CallbackQueryHandler(bot.button_callback))
    
    logger.info("Bot started...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
