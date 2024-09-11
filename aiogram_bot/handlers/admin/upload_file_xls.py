import os
import pandas as pd
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from asgiref.sync import sync_to_async
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ContentType
from aiogram_bot.loader import dp, bot
from aiogram_bot.states.admin import Update_xls
from student.models import Student
from group.models import Group
from aiogram_bot.filters.admin import IsAdminFilter

# Request to upload an Excel file
@dp.message(F.text == "📁 Upload Excel",IsAdminFilter())
async def request_file(message: Message, state: FSMContext):
    await message.answer("Iltimos, Excel faylni yuklang!")  # (Please upload the Excel file!)
    await state.set_state(Update_xls.xls)  # (Set state to handle file upload)


# Get group ID by its name (Synchronous function, no async needed here)
def get_group_id_by_name(group_name):
    try:
        group = Group.objects.get(name=group_name)  # (Try to get the group by its name)
        return group.id
    except Group.DoesNotExist:
        return None  # (Return None if the group does not exist)


# Handle the uploaded Excel file
@dp.message(F.content_type == ContentType.DOCUMENT,IsAdminFilter())
@dp.message(F.state == Update_xls.xls)
async def handle_document(message: Message, state: FSMContext):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path    
    await bot.download_file(file_path, "jadval.xlsx")  # (Download the Excel file)
    path = "jadval.xlsx"

    # Read the Excel file
    try:
        wb = pd.read_excel(path)
    except Exception as e:
        await message.reply("Faylni o'qishda xatolik yuz berdi.")  # (Error reading the file)
        os.remove(path)
        return

    os.remove(path)  # (Remove the file after reading it)

    for index, row in wb.iterrows():
        # Get the group ID
        group_id = await sync_to_async(get_group_id_by_name)(row['group_name'])
        if group_id is None:
            # Skip if group is not found
            print(f"Guruh '{row['group_name']}' topilmadi.")  # (Group not found)
            continue

        # Check if the phone number already exists
        phone_exists = await sync_to_async(Student.objects.filter(phone=row['phone']).exists)()
        if phone_exists:
            print(f"Telefon raqam '{row['phone']}' allaqachon mavjud.")  # (Phone number already exists)
            continue

        try:
            # Create a new Student entry
            await sync_to_async(Student.objects.create)(
                first_name=row.get('first_name', ''),
                last_name=row.get('last_name', ''),
                father_name=row.get('father_name', ''),
                group_id=group_id,
                amount=row.get('amount', 0),
                school_name=row.get('school_name', ''),
                student_class=row.get('student_class', ''),
                phone=row.get('phone', ''),
                start_date=row.get('start_date', pd.NaT),
                is_active=row.get('is_active', True)  # (Default to True if not provided)
            )
        except ValueError as e:
            # Handle errors related to data validation
            print(f"Xatolik: {e}")  # (Error: {e})
            continue  # (Skip to the next row)

    await message.reply("Fayldagi ma'lumotlar bazaga qo'shildi.")  # (Data from the file has been added to the database)
