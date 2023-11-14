from random import randint
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, Text
from aiogram.types import Message
from datetime import datetime
import os
import time
import json

BOT_TOKEN: str = os.getenv('BOT_TOKEN')

bot: Bot = Bot(token=BOT_TOKEN)
dp: Dispatcher = Dispatcher()
attempts: int = 7
users2: dict = {}
with open('./users.json', "r") as file:
    users = json.load(file)


def get_random_number() -> int:
    return randint(1, 100)


async def command_start(message: Message):
    if not message.from_user.first_name.lower() == 'ирина123':
        await message.answer_sticker(sticker='CAACAgIAAxkBAAEIwiFkS0R-N3Yplbh-6RmaW8eQql8_-wAC0wUAAj-VzAqfWrvSXUfHMS8E')
        # if not os.path.exists("C:/Users/Kain/Desktop/Ugadai_cache/"):
        #     os.makedirs("C:/Users/Kain/Desktop/Ugadai_cache/")
        print(f'Старт бот: {message.from_user.id}, {message.from_user.full_name}, {datetime.now()}')
        await message.answer(text=f'Приветствую, {message.from_user.first_name}!\nПредлагаю твоему вниманию игру:'
                                  f'\n\tУгадай число =)\nДля изучения правил игры\nЖми --> "/help"')

        if str(message.from_user.id) not in users:
            print('Первый раз зашел')
            # print(users)
            users2[str(message.from_user.id)] = {
                'first_name': message.from_user.first_name,
                'last_name': message.from_user.last_name,
                'full_name': message.from_user.full_name,
                'in_game': False,
                'secret_number': None,
                'attempts': None,
                'total_games': 0,
                'wins': 0,
                'date': datetime.now().strftime('%H:%M:%S - %d.%m.%y')
            }
            with open("./users.json", "a") as file1:
                json.dump(users2, file1, indent=4, ensure_ascii=False)
    else:
        await message.answer(text='Обнаружена - Ирина!!!')
        time.sleep(1.8)
        await message.answer_sticker(sticker='CAACAgIAAxkBAAEIwkdkS0jNz32zkpBIS34V3ZUxDfdEXwACCAMAAm2wQgMvOYPVPlZS6S8E')


async def command_game(message: Message):
    if not users[str(message.from_user.id)]["in_game"]:
        await message.answer_sticker(sticker='CAACAgIAAxkBAAEIwidkS0VVrImVGUoJfqqs5VvxJFT4dwACFw8AAnnYQUhZXcd4aSNmiS8E')
        time.sleep(1.8)
        await message.answer(text='Ну, поехали! Я уже загадал, пиши ответ')

        users[str(message.from_user.id)]["total_games"] += 1
        with open("./users.json", "w") as file:
            json.dump(users, file, indent=4, ensure_ascii=False)

        users[str(message.from_user.id)]["in_game"] = True
        users[str(message.from_user.id)]["secret_number"] = get_random_number()
        users[str(message.from_user.id)]["attempts"] = attempts
    else:
        await message.answer(text='Не нужно, Вы уже в режиме игры\nПишите число от 1 до 100')


async def command_help(message: Message):
    await message.answer(
        text=f'Я загадываю любое число от 1 до 100.\nВаша задача угадать это число за {attempts} попыток.\n'
             f'Для начала игры - напишите в чат: "игра"\nИли в меню выберите команду - "/game"\n'
             f'Для просмотра статистики, наберите команду - "/stat".\nДля завершения игры - "/cancel"')


async def get_stats(message: Message):
    await message.answer(
        f'Количество ваших игр: {users[str(message.from_user.id)]["total_games"]}\n'
        f'Количество ваших побед: {users[str(message.from_user.id)]["wins"]}')


async def command_cancel(message: Message):
    if users[str(message.from_user.id)]["in_game"]:
        users[str(message.from_user.id)]["in_game"] = False
        await message.answer(text='Игра окончена')
    else:
        await message.answer(text='Игра не запущена!')


async def check_input_number(message: Message):
    if users[str(message.from_user.id)]["in_game"]:
        if int(message.text) == users[str(message.from_user.id)]["secret_number"]:
            await message.answer_sticker(
                sticker='CAACAgIAAxkBAAEIwkVkS0iZf0UCuVLNzIW0pOATT5FAJQACoAADwZxgDFeN0A5Zq2liLwQ')
            time.sleep(1.8)
            await message.answer(text='Поздравляю! Вы угадали!\n'
                                      'Для начала игры, снова напишите в чат: игра\nИли напишите команду - "/game"')
            users[str(message.from_user.id)]["in_game"] = False
            users[str(message.from_user.id)]["wins"] += 1
            with open("./users.json", "w") as file:
                json.dump(users, file, indent=4, ensure_ascii=False)
        elif int(message.text) > users[str(message.from_user.id)]["secret_number"]:
            await message.answer_sticker(
                sticker='CAACAgIAAxkBAAEIwitkS0a_67oJ_EHwIHmaTBNWgx-98AACAgEAAladvQpO4myBy0Dk_y8E')
            users[str(message.from_user.id)]["attempts"] -= 1
            if users[str(message.from_user.id)]["attempts"] > 0:
                await message.answer(text='Не правильно, нужно меньше')
                await message.answer(f'Осталось попыток: {users[str(message.from_user.id)]["attempts"]}')
        else:
            await message.answer_sticker(
                sticker='CAACAgIAAxkBAAEIwi1kS0dK-2kflGXxrsFL_zUTPwaIkgACuQ4AAmxu8Emp2F_Xn3emBi8E')
            users[str(message.from_user.id)]["attempts"] -= 1
            if users[str(message.from_user.id)]["attempts"] > 0:
                await message.answer(text='Не правильно, нужно больше')
                await message.answer(f'Осталось попыток: {users[str(message.from_user.id)]["attempts"]}')

        if users[str(message.from_user.id)]["attempts"] == 0:
            await message.answer_sticker(
                sticker='CAACAgIAAxkBAAEIwi9kS0fFFGoyZ-xp_qHE87X-8Ho-UAACRwEAAlKJkSMDBgYs0ffwdS8E')
            time.sleep(1.8)
            await message.answer(
                text=f'К сожалению попытки закончились. Вы проиграли!\nПравильный ответ был: {users[str(message.from_user.id)]["secret_number"]}\n'
                     f'Для просмотра статистики, наберите команду - "/stat"\nДля начала новой игры, напишите снова: игра\nИли напишите команду - "/game"')
            users[str(message.from_user.id)]["in_game"] = False

    else:
        await message.reply(text='Вы не начали игру, напишите: игра')


async def lets_play(message: Message):
    if message.text.lower() == 'игра':
        if not users[str(message.from_user.id)]["in_game"]:
            await message.answer_sticker(
                sticker='CAACAgIAAxkBAAEIwidkS0VVrImVGUoJfqqs5VvxJFT4dwACFw8AAnnYQUhZXcd4aSNmiS8E')
            time.sleep(1.8)
            await message.answer(text='Ну, поехали! Я уже загадал, пиши ответ')
            users[str(message.from_user.id)]["total_games"] += 1
            users[str(message.from_user.id)]["in_game"] = True
            users[str(message.from_user.id)]["secret_number"] = get_random_number()
            users[str(message.from_user.id)]["attempts"] = attempts
        else:
            await message.answer(text='Не нужно, Вы уже в режиме игры\nПишите число от 1 до 100')


async def any_mess(message: Message):
    if users[str(message.from_user.id)]["in_game"]:
        await message.answer_sticker(sticker='CAACAgIAAxkBAAEIwn5kS2yvZjJzxf7VxC8YuYuY_7SPJAACuQADwZxgDCwddEfAT6lOLwQ')
        await message.reply(text='Что это?! Вы в режиме игры, отправляйте только число от 1 до 100!')
    else:
        await message.reply(text='Что это?! Вы не в игре. '
                                 'Если хотите начать игру, пишите: "игра"\nИли нажмите на команду - "/game"')


dp.message.register(command_start, Command(commands='start'))
dp.message.register(command_game, Command(commands='game'))
dp.message.register(command_help, Command(commands='help'))
dp.message.register(get_stats, Command(commands='stat'))
dp.message.register(command_cancel, Command(commands='cancel'))
dp.message.register(check_input_number, lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
dp.message.register(lets_play, Text(text=['игра'], ignore_case=True))
dp.message.register(any_mess)

if __name__ == '__main__':
    dp.run_polling(bot)
