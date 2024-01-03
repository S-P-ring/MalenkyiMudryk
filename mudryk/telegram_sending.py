import asyncio
import datetime
import os

from telethon import TelegramClient, events, errors, sync
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.types import InputPhoneContact
from telethon import functions, types
from telethon.sessions import StringSession


API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
INVITE_LINK = os.getenv("INVITE_LINK")
PATH_TO_SESSION = os.getenv("PATH_TO_SESSION")


# def login():
#     if not client.is_user_authorized():
#         client.send_code_request(PHONE_NUMBER)
#         try:
#             client.sign_in(PHONE_NUMBER, input('Enter the code (sent on your telegram account): '))
#         except errors.SessionPasswordNeededError:
#             pw = input('Two-Step Verification enabled. Please enter your account password: ')
#             client.sign_in(password=pw)

# client = TelegramClient(PHONE_NUMBER, API_ID, API_HASH)


async def send_record_message(selected_course, selected_day, selected_time, parent_name, child_name, email, phone):
    client = TelegramClient(PATH_TO_SESSION, API_ID, API_HASH)
    await client.connect()
    await asyncio.sleep(1)
    destination_group_invite_link = INVITE_LINK
    entity = await client.get_entity(destination_group_invite_link)
    message = f'Новий запис на урок .\n' \
              f'Обраний курс: {selected_course}\n' \
              f'Дата та час: {selected_day}, {selected_time}\n' \
              f'Батько: {parent_name}\n' \
              f'Дитина: {child_name}\n' \
              f'Email: {email}\n' \
              f'Телефон: {phone}'
    await client.send_message(entity=entity, message=message)
    await client.disconnect()


def send_record(selected_course, selected_day, selected_time, parent_name, child_name, email, phone):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_record_message(selected_course, selected_day, selected_time, parent_name, child_name, email, phone))
    loop.close()


async def send_feedback_or_proposal_message(selected_option, name, email, text, phone_number):
    client = TelegramClient(PATH_TO_SESSION, API_ID, API_HASH)
    await client.connect()
    await asyncio.sleep(1)
    destination_group_invite_link = INVITE_LINK
    entity = await client.get_entity(destination_group_invite_link)
    time_now = datetime.datetime.now().strftime('%A, %d %B, %H:%m')
    message = f"Ім'я: {name}\n" \
              f'Дата та час: {time_now}\n' \
              f'Email: {email}\n' \
              f'Текст: {text}\n' \
              f'Телефон: {phone_number}'
    if selected_option == 'feedback':
        message = f'Новий відгук на сайті .\n' + message
    else:
        message = f'Нова пропозиція на сайті .\n' + message
    await client.send_message(entity=entity, message=message)
    await client.disconnect()


def send_feedback_or_proposal(selected_option, name, email, text, phone_number):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        send_feedback_or_proposal_message(selected_option, name, email, text, phone_number))
    loop.close()
