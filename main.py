import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes
)
from config import TELEGRAM_BOT_TOKEN, OPENAI_API_KEY
from database import Database
from ai_messages import AIMessenger
from lead_scraper import LeadScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = Database()
ai = AIMessenger(OPENAI_API_KEY)
scraper = LeadScraper()

class LeadGenBot:
    def __init__(self):
        self.db = db
        self.ai = ai
        self.scraper = scraper
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [InlineKeyboardButton("📊 Load Leads", callback_data="load_leads")],
            [InlineKeyboardButton("📧 Generate Messages", callback_data="gen_messages")],
            [InlineKeyboardButton("📈 View Stats", callback_data="view_stats")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🤖 AI Lead Gen Bot\n\n✅ Collect leads\n✅ Generate messages\n✅ Track engagement",
            reply_markup=reply_markup
        )
    
    async def load_sample_leads(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        leads = self.scraper.scrape_sample_leads()
        for lead in leads:
            self.db.add_lead(lead["name"], lead["email"], lead["company"])
        
        await update.callback_query.edit_message_text(
            text=f"✅ Loaded {len(leads)} leads!"
        )
    
    async def generate_messages(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        leads = self.db.get_leads(status='new')
        
        if not leads:
            await update.callback_query.edit_message_text(text="📭 No leads!")
            return
        
        count = 0
        for lead in leads[:3]:
            try:
                msg = self.ai.generate_message(lead[1], lead[3], "Tech")
                self.db.save_message(lead[0], msg)
                self.db.update_lead_status(lead[0], 'contacted')
                count += 1
            except Exception as e:
                logger.error(f"Error: {e}")
        
        await update.callback_query.edit_message_text(text=f"📧 Generated {count} messages!")
    
    async def view_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        new = len(self.db.get_leads('new'))
        contacted = len(self.db.get_leads('contacted'))
        
        await update.callback_query.edit_message_text(
            text=f"📈 Stats:\n\n🆕 New: {new}\n📧 Contacted: {contacted}\n📊 Total: {new + contacted}"
        )
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        if query.data == "load_leads":
            await self.load_sample_leads(update, context)
        elif query.data == "gen_messages":
            await self.generate_messages(update, context)
        elif query.data == "view_stats":
            await self.view_stats(update, context)

async def main():
    bot = LeadGenBot()
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", bot.start))
    app.add_handler(CallbackQueryHandler(bot.button_callback))
    
    logger.info("✅ Bot started...")
    await app.run_polling()

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n✅ Bot stopped")
