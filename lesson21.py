import logging
import random

from aiogram import Bot, Dispatcher, executor, types

from decouple import config

API_TOKEN = config('TELEGRAM_BOT_TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

gameStarted = False
score = 0
answer = ''




def save_id_sticker(file_id):
    with open('stickers.txt', 'a') as f:
        f.write(file_id + '\n')
    
def open_id_sticker():
    with open('stickers.txt', 'r') as f:
        return f.read().split('\n')
        



@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    text = 'Прівіт, радий тебе бачити!\n\n' \
            'Якщо ти хочеш дізнатися, що я вмію, то напиши /help'
    await message.reply(text)

    
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply("Я бот для навчання Python. Поки що я вмію тільки це.")

@dp.message_handler(content_types=['sticker'])
async def sticker_handler(message: types.Message):
    print(message)
    save_id_sticker(message.sticker.file_id)
    await message.reply_sticker(message.sticker.file_id)

@dp.message_handler(commands=['sticker'])
async def sticker_command(message: types.Message):
    all_stickers = open_id_sticker()
    random_sticker = random.choice(all_stickers)
    await message.answer_sticker(random_sticker)


@dp.message_handler(content_types=['photo'])    
async def photo_handler(message: types.Message):
    print(message.photo)
    await message.reply_photo(message.photo[-1].file_id)
    
@dp.message_handler(commands=['+'])
async def plus_command(message: types.Message):
    global score,answer
    score += 1
    answer = eval('1+2')
    print('score', score)
    await message.answer(f'Ваш рахунок: {score}')
    
@dp.message_handler()
async def echo(message: types.Message):
    print(message)
    if message.text.lower() == 'привіт':
        await message.answer_sticker("CAACAgQAAxkBAAIJtmR00PmLChg9AAFcGnHY6bkRxllO-QACBwEAAmuuXgm32BqzJKDKhy8E")
        await message.answer('І тобі привіт!')
    elif message.text.lower() == 'пока':
        await message.answer_photo("AgACAgIAAxkBAAIJzWR00-GORyiTVsn3mJJGBvblA6qyAAKgyzEbY_igS3fnUhy-6aw5AQADAgADbQADLwQ", caption='Прощавай!')        
    else:
        await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    

