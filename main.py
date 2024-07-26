import os
import telebot
from telebot import types
import LargeMessages

bot = telebot.TeleBot('6483439802:AAHr5IV25iNvy23PRpnQkXNec3LtCSqDUGY')
nowcode = "root"

@bot.message_handler(commands=['start'])
def main(message):
    global nowcode
    nowcode = "root"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    _buttonImClient = types.KeyboardButton("👩 Я клиент")
    _buttonImMaster = types.KeyboardButton("👑 Я мастер")
    markup.add(_buttonImClient, _buttonImMaster)
    bot.send_message(message.chat.id, text=LargeMessages.root.format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def getButtons(message):
    global nowcode
    if (nowcode == "root"):
        if (message.text == "👩 Я клиент"): # Клиент
            nowcode = "client_morerelevant"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            _buttonTattooing = types.KeyboardButton("Татуаж")
            _buttonBrighteningTattoo = types.KeyboardButton("Осветление татуажа")
            markup.add(_buttonTattooing, _buttonBrighteningTattoo)
            bot.send_message(message.chat.id, text=LargeMessages.client_morerelevant.format(message.from_user), reply_markup=markup)

        elif (message.text == "👑 Я мастер"): # Мастер
            nowcode = "non"
            print("clear")

    elif (nowcode == "client_morerelevant"):
        if (message.text == "Татуаж"): # Татуаж
            nowcode = "client_what"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            _buttonEyebrows = types.KeyboardButton("Брови")
            _buttonLips = types.KeyboardButton("Губы")
            _buttonEyelids = types.KeyboardButton("Веки")
            _buttonCamouflage = types.KeyboardButton("Камуфляж")
            markup.add(_buttonEyebrows, _buttonLips, _buttonEyelids, _buttonCamouflage)
            bot.send_message(message.chat.id, text=LargeMessages.client_what.format(message.from_user), reply_markup=markup)

        elif (message.text == "Осветление татуажа"): # Осветление татуажа
            nowcode = "non"
            print("clear")

    elif (nowcode == "client_what"):
        if (message.text == "Брови"): # Брови
            nowcode = "general_point_tattoo"
            bot.send_message(message.chat.id, text=LargeMessages.aboutEyebrows.format(message.from_user))

        elif (message.text == "Губы"): # Губы
            nowcode = "general_point_tattoo"
            bot.send_message(message.chat.id, text=LargeMessages.aboutLips.format(message.from_user))

        elif (message.text == "Веки"): # Веки
            nowcode = "general_point_tattoo"
            bot.send_message(message.chat.id, text=LargeMessages.aboutEyelids.format(message.from_user))

        elif (message.text == "Камуфляж"): # Камуфляж
            nowcode = "general_point_tattoo"
            bot.send_message(message.chat.id, text=LargeMessages.aboutCamouflage_0.format(message.from_user))
            bot.send_message(message.chat.id, text=LargeMessages.aboutCamouflage_1.format(message.from_user))

        if (nowcode == "general_point_tattoo"):  # общая точка
            nowcode = "from_general_point_tattoo"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            _buttonExamples = types.KeyboardButton("Посмотреть примеры работ")
            _buttonSignUp = types.KeyboardButton("Записаться")
            _buttonLearnMore = types.KeyboardButton("Узнать больше о татуаже")
            _buttonPrice = types.KeyboardButton("Узнать прайс")
            markup.add(_buttonExamples, _buttonSignUp, _buttonLearnMore, _buttonPrice)
            bot.send_message(message.chat.id, text="Идем дальше".format(message.from_user), reply_markup=markup)

    elif (nowcode == "general_point_tattoo"): # общая точка
        nowcode = "from_general_point_tattoo"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        _buttonExamples = types.KeyboardButton("Посмотреть примеры работ")
        _buttonSignUp = types.KeyboardButton("Записаться")
        _buttonLearnMore = types.KeyboardButton("Узнать больше о татуаже")
        _buttonPrice = types.KeyboardButton("Узнать прайс")
        markup.add(_buttonExamples, _buttonSignUp, _buttonLearnMore, _buttonPrice)
        bot.send_message(message.chat.id, text="Идем дальше".format(message.from_user), reply_markup=markup)

    elif (nowcode == "from_general_point_tattoo"):
        if (message.text == "Посмотреть примеры работ"):
            nowcode = "general_point_tattoo"

            bot.send_message(message.chat.id, text="*Брови* \n\n Волосковая техника".format(message.from_user), parse_mode='Markdown') # Markdown делает bold **
            image_paths = [os.path.join("other/PhotoExamplesTattooing/Eyebrows/Voloskovaya", file) for file in os.listdir("other/PhotoExamplesTattooing/Eyebrows/Voloskovaya") if
                           file.endswith(('.png', '.jpg', '.jpeg'))]
            media_group = [telebot.types.InputMediaPhoto(open(image_path, 'rb')) for image_path in image_paths]
            bot.send_media_group(message.chat.id, media_group)

            bot.send_message(message.chat.id, text="Пудровое напыление".format(message.from_user), parse_mode='Markdown')  # Markdown делает bold **
            image_paths = [os.path.join("other/PhotoExamplesTattooing/Eyebrows/Pydrovoe_napilenie", file) for file in
                           os.listdir("other/PhotoExamplesTattooing/Eyebrows/Pydrovoe_napilenie") if
                           file.endswith(('.png', '.jpg', '.jpeg'))]
            media_group = [telebot.types.InputMediaPhoto(open(image_path, 'rb')) for image_path in image_paths]
            bot.send_media_group(message.chat.id, media_group)

            bot.send_message(message.chat.id, text="*Веки* \n\n".format(message.from_user),
                             parse_mode='Markdown')  # Markdown делает bold **
            image_paths = [os.path.join("other/PhotoExamplesTattooing/Eyelids", file) for file in
                           os.listdir("other/PhotoExamplesTattooing/Eyelids") if
                           file.endswith(('.png', '.jpg', '.jpeg'))]
            media_group = [telebot.types.InputMediaPhoto(open(image_path, 'rb')) for image_path in image_paths]
            bot.send_media_group(message.chat.id, media_group)

            bot.send_message(message.chat.id, text="*Губы* \n\n".format(message.from_user),
                             parse_mode='Markdown')  # Markdown делает bold **
            image_paths = [os.path.join("other/PhotoExamplesTattooing/Lips", file) for file in
                           os.listdir("other/PhotoExamplesTattooing/Lips") if
                           file.endswith(('.png', '.jpg', '.jpeg'))]
            media_group = [telebot.types.InputMediaPhoto(open(image_path, 'rb')) for image_path in image_paths]
            bot.send_media_group(message.chat.id, media_group)


        if (message.text == "Записаться"):
            nowcode = ""
            bot.send_message(message.chat.id, text=LargeMessages.aboutEyebrows.format(message.from_user))

        if (message.text == "Узнать больше о татуаже"):
            nowcode = ""
            bot.send_message(message.chat.id, text=LargeMessages.aboutEyebrows.format(message.from_user))

        if (message.text == "Узнать прайс"):
            nowcode = "from_general_point_tattoo"
            bot.send_message(message.chat.id, text=LargeMessages.aboutPrice.format(message.from_user))

    elif (message.text == "Записаться"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        _buttonTattooing = types.KeyboardButton("Татуаж")
        _buttonBrighteningTattoo = types.KeyboardButton("Осветление татуажа")
        markup.add(_buttonTattooing, _buttonBrighteningTattoo)
        bot.send_message(message.chat.id, text="Что для вас сейчас актуальнее?".format(message.from_user),
                         reply_markup=markup)

    elif (message.text == "Узнать больше о татуаже"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        _buttonTattooing = types.KeyboardButton("Татуаж")
        _buttonBrighteningTattoo = types.KeyboardButton("Осветление татуажа")
        markup.add(_buttonTattooing, _buttonBrighteningTattoo)
        bot.send_message(message.chat.id, text="Что для вас сейчас актуальнее?".format(message.from_user),
                         reply_markup=markup)

    elif (message.text == "Узнать прайс"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        _buttonTattooing = types.KeyboardButton("Татуаж")
        _buttonBrighteningTattoo = types.KeyboardButton("Осветление татуажа")
        markup.add(_buttonTattooing, _buttonBrighteningTattoo)
        bot.send_message(message.chat.id, text="Что для вас сейчас актуальнее?".format(message.from_user),
                         reply_markup=markup)

    else:
        bot.send_message(message.chat.id, text="Пожалуйста, используйте кнопки")

    print(nowcode)

bot.polling(none_stop=True)