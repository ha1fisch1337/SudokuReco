from aiogram import Bot, Dispatcher, types
import requests
from PIL import Image
from key import API

key = API

bot = Bot(token=key)
dp=Dispatcher()

@dp.message()
async def echo(message: types.Message):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    path = file.file_path
    img_data = requests.get(f"https://api.telegram.org/file/bot{key}/{path}").content
    with open('/home/ha1fy/Desktop/Python/SudokuBot/ph.jpg', 'wb') as handler:
        handler.write(img_data)
        im=Image.open('/home/ha1fy/Desktop/Python/SudokuBot/ph.jpg').rotate(180)
        im.save('/home/ha1fy/Desktop/Python/SudokuBot/ph.jpg')
    photo=types.FSInputFile('/home/ha1fy/Desktop/Python/SudokuBot/ph.jpg')
    await bot.send_photo(message.chat.id, photo)

dp.run_polling(bot)
