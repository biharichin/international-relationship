
import os
import json
import asyncio
from telegram import Bot
from telegram.error import TelegramError

async def send_mcqs():
    """
    Sends a batch of 20 MCQs to the specified Telegram chats.
    """
    bot_token = os.getenv('TELEGRAM_TOKEN')
    if not bot_token:
        print("Error: TELEGRAM_TOKEN environment variable not set.")
        return

    chat_ids_str = os.getenv('TELEGRAM_CHAT_IDS')
    if not chat_ids_str:
        print("Error: TELEGRAM_CHAT_IDS environment variable not set.")
        return
    
    chat_ids = [chat_id.strip() for chat_id in chat_ids_str.split(',')]

    bot = Bot(token=bot_token)

    # Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    questions_file = os.path.join(script_dir, 'questions.json')
    progress_file = os.path.join(script_dir, 'progress.txt')

    # Load questions
    try:
        with open(questions_file, 'r', encoding='utf-8') as f:
            questions = json.load(f)
    except FileNotFoundError:
        print(f"Error: {questions_file} not found.")
        return

    # Get progress
    try:
        with open(progress_file, 'r') as f:
            start_index = int(f.read().strip())
    except FileNotFoundError:
        start_index = 0

    if start_index >= len(questions):
        completion_message = "no question, we done"
        for chat_id in chat_ids:
            try:
                await bot.send_message(chat_id=chat_id, text=completion_message)
                print(f"Sent completion message to {chat_id}")
            except TelegramError as e:
                print(f"Error sending completion message to {chat_id}: {e}")
        return

    # Send 20 questions
    end_index = min(start_index + 20, len(questions))
    questions_to_send = questions[start_index:end_index]

    for question_data in questions_to_send:
        question = f"{question_data['question_number']}. {question_data['question']}"
        options = question_data['options']
        correct_option_index = question_data['correct_option_index']

        for chat_id in chat_ids:
            try:
                await bot.send_poll(
                    chat_id=chat_id,
                    question=question,
                    options=options,
                    is_anonymous=True,
                    type='quiz',
                    correct_option_id=correct_option_index
                )
                print(f"Sent question {question_data['question_number']} to {chat_id}")
            except TelegramError as e:
                print(f"Error sending question {question_data['question_number']} to {chat_id}: {e}")
            # Add a small delay between messages to avoid rate limiting
            await asyncio.sleep(1)

    # Update progress
    with open(progress_file, 'w') as f:
        f.write(str(end_index))
    
    print(f"Successfully sent questions {start_index + 1} to {end_index}.")

if __name__ == '__main__':
    asyncio.run(send_mcqs())
