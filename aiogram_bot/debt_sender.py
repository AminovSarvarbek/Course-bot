from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.base import ConflictingIdError
from apscheduler.triggers.cron import CronTrigger
from asgiref.sync import sync_to_async
from student.models import Student
from payment.utils import get_unpaid_months_for_student
from aiogram_bot.loader import bot
from pytz import timezone
import logging
from aiogram_bot.utils.month_names import month_names  # Import month_names

# Configure logging
logging.basicConfig(level=logging.INFO)

async def send_unpaid_reminders():
    """
    Send reminders to students with unpaid months every day at 8:00 AM Uzbekistan time.
    """
    # Fetch all students
    students = await sync_to_async(list)(Student.objects.all())

    for student in students:
        if not student.telegram_id:  # Skip students without Telegram ID
            logging.warning(f"Student {student.id} has no Telegram ID.")
            continue
        
        unpaid_months = await get_unpaid_months_for_student(student.id)
        
        if unpaid_months:
            monthly_amount = student.amount
            total_debt = monthly_amount * len(unpaid_months)
            
            # Prepare the reminder message
            unpaid_months_details = '\n'.join([
                f"• {month[:4]}-yilning {month_names[int(month[5:])-1]} oyi ({month}) — 💰 <b>{int(monthly_amount):,}</b> so'm"
                for month in unpaid_months
            ])
            
            message_text = (f"Assalomu alaykum, hurmatli ota-ona!\n\n"
                            f"Farzandingiz <b>{student.first_name} {student.last_name}</b> uchun\n"
                            f"quyidagi to'lovlarni amalga oshirishingiz kerak:\n\n"
                            f"To'lanmagan oylar ({len(unpaid_months)} ta):\n"
                            f"{unpaid_months_details}\n\n"
                            f"💵 Oylik to'lov narxi: <b>{int(monthly_amount):,}</b> so'm\n"
                            f"💰 Jami qarzdorlik: <b>{int(total_debt):,}</b> so'm\n\n"
                            f"Iltimos, ushbu to'lovlarni vaqtida amalga oshiring. Rahmat!")

            try:
                # Send the message to the student's Telegram account
                await bot.send_message(student.telegram_id, message_text, parse_mode='HTML')
            except Exception as e:
                # Log any exception that occurs
                logging.error(f"Failed to send message to {student.telegram_id}: {e}, bu chat idi mavju emas deyapti")

def setup_scheduler():
    """
    Setup a scheduler to send messages every day at 8:00 AM Uzbekistan time.
    """
    scheduler = AsyncIOScheduler(timezone=timezone('Asia/Tashkent'))
    print("Scheduler running...")

    try:
        # Schedule the task to run every day at 8:00 AM Uzbekistan time
        scheduler.add_job(
            send_unpaid_reminders,
            trigger=CronTrigger(hour=8, minute=00, timezone='Asia/Tashkent'),
            id='daily_reminder'
        )
        print("Job scheduled for 8:00 AM daily.")
    except ConflictingIdError:
        print("Job ID conflict.")

    scheduler.start()
    print("Scheduler started.")
