import os
import telebot
from telebot import types
import LargeMessages
import communication_method_with_user
import enumProcedures
import enumZones
import user
from communication_method_with_user import EnumCommunicationMethod
from enumProcedures import Procedures
from enumZones import Zones

bot = telebot.TeleBot('6483439802:AAHr5IV25iNvy23PRpnQkXNec3LtCSqDUGY')
_AdminID = 772136193
nowcode = "root"
takedMessage = False

_user = user.User

@bot.message_handler(commands=['start'])
def main(message):
    global nowcode
    nowcode = "root"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    _buttonImClient = types.KeyboardButton("👩 Я клиент")
    _buttonImMaster = types.KeyboardButton("👑 Я мастер")
    markup.add(_buttonImClient, _buttonImMaster)
    bot.send_message(message.chat.id, text=LargeMessages.root.format(message.from_user), reply_markup=markup)

# Обработка контакта
@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    global nowcode
    global _user
    if message.contact is not None:
        phone_number = message.contact.phone_number
        first_name = message.contact.first_name
        last_name = message.contact.last_name
        user_id = message.contact.user_id

        _user.phone_number = phone_number
        _user.first_name = first_name
        _user.last_name = last_name
        _user.user_id = user_id

        #Обнуление что еще не выбрано
        _user.procedure = None

        _user.appointment_zone = None  # запоминает зону макияжа пользователя
        _user.communication_method = None  # запоминает метод связи с пользователем
        _user.want_consult = False  # Может хотеть на консультацию
        _user.delalaTattoo_v_Broowushka = False
        _user.delalaTattoo_v_zone = False
        _user.want_send_photo = False

        if (nowcode == "wait_contact"): # Татуаж
            message_text = f"{first_name}, очень приятно! \n Татуаж какой зоны вы хотели бы сделать?"

            nowcode = "make_appointment"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            _buttonEyebrows = types.KeyboardButton("Брови")
            _buttonEyelids = types.KeyboardButton("Веки")
            _buttonLips = types.KeyboardButton("Губы")
            _buttonCounseling = types.KeyboardButton("Хочу на консультацию")
            markup.add(_buttonEyebrows, _buttonEyelids, _buttonLips, _buttonCounseling)
            bot.send_message(message.chat.id, text=message_text.format(message.from_user), reply_markup=markup)

        elif (nowcode == "tattoo_lightening_yes"): # Осветление таттуажа
            message_text = f"{first_name}, очень приятно! \n Что вы хотите узнать?"

            nowcode = "tattoo_lightening_info"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            _buttonPriceZones = types.KeyboardButton("Прайс на осветление татуажа")
            _buttonMethods = types.KeyboardButton("Способы осветления")
            markup.add(_buttonPriceZones, _buttonMethods)
            bot.send_message(message.chat.id, text=message_text.format(message.from_user), reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Ошибка, попробуйте с начала.")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, отправьте контакт, используя кнопку 'Отправить контакт.")

@bot.message_handler(content_types=['text'])
def getButtons(message):
    global nowcode
    global takedMessage
    takedMessage = False
    global _user

    if (nowcode == "root"):
        if (message.text == "👩 Я клиент"): # Клиент
            nowcode = "client_morerelevant"
            takedMessage = True
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            _buttonTattooing = types.KeyboardButton("Татуаж")
            _buttonBrighteningTattoo = types.KeyboardButton("Осветление татуажа")
            markup.add(_buttonTattooing, _buttonBrighteningTattoo)
            bot.send_message(message.chat.id, text="Что для вас сейчас актуальнее?".format(message.from_user), reply_markup=markup)

        elif (message.text == "👑 Я мастер"): # Мастер
            nowcode = "non"
            takedMessage = True
            print("clear")

    elif (nowcode == "client_morerelevant"):
        if (message.text == "Татуаж"): # Татуаж
            nowcode = "client_what"
            takedMessage = True

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            _buttonEyebrows = types.KeyboardButton("Брови")
            _buttonLips = types.KeyboardButton("Губы")
            _buttonEyelids = types.KeyboardButton("Веки")
            _buttonCamouflage = types.KeyboardButton("Камуфляж")
            markup.add(_buttonEyebrows, _buttonLips, _buttonEyelids, _buttonCamouflage)
            bot.send_message(message.chat.id, text="Что конкретно?".format(message.from_user), reply_markup=markup)

        elif (message.text == "Осветление татуажа"):
            nowcode = "tattoo_lightening_correct"
            takedMessage = True

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            _buttonYes = types.KeyboardButton("Да")
            _buttonNo = types.KeyboardButton("Нет")
            markup.add(_buttonYes, _buttonNo)
            bot.send_message(message.chat.id, text="У вас есть старый татуаж, который хотелось бы удалить или просто сделать светлее, правильно?".format(message.from_user), reply_markup=markup)

    elif (nowcode == "client_what"):
        if (message.text == "Брови"): # Брови
            nowcode = "general_point_tattoo"
            takedMessage = True
            bot.send_message(message.chat.id, text=LargeMessages.aboutEyebrows.format(message.from_user))

        elif (message.text == "Губы"): # Губы
            nowcode = "general_point_tattoo"
            takedMessage = True
            bot.send_message(message.chat.id, text=LargeMessages.aboutLips.format(message.from_user))

        elif (message.text == "Веки"): # Веки
            nowcode = "general_point_tattoo"
            takedMessage = True
            bot.send_message(message.chat.id, text=LargeMessages.aboutEyelids.format(message.from_user))

        elif (message.text == "Камуфляж"): # Камуфляж
            nowcode = "general_point_tattoo"
            takedMessage = True
            bot.send_message(message.chat.id, text=LargeMessages.aboutCamouflage_0.format(message.from_user))
            bot.send_message(message.chat.id, text=LargeMessages.aboutCamouflage_1.format(message.from_user))

        if (nowcode == "general_point_tattoo"):  # общая точка
            nowcode = "from_general_point_tattoo"
            takedMessage = True
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            _buttonExamples = types.KeyboardButton("Посмотреть примеры работ")
            _buttonSignUp = types.KeyboardButton("Записаться")
            _buttonLearnMore = types.KeyboardButton("Узнать больше о татуаже")
            _buttonPrice = types.KeyboardButton("Узнать прайс")
            markup.add(_buttonExamples, _buttonSignUp, _buttonLearnMore, _buttonPrice)
            bot.send_message(message.chat.id, text="Идем дальше".format(message.from_user), reply_markup=markup)

    elif (nowcode == "general_point_tattoo"): # общая точка
        nowcode = "from_general_point_tattoo"
        takedMessage = True
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        _buttonExamples = types.KeyboardButton("Посмотреть примеры работ")
        _buttonSignUp = types.KeyboardButton("Записаться")
        _buttonLearnMore = types.KeyboardButton("Узнать больше о татуаже")
        _buttonPrice = types.KeyboardButton("Узнать прайс")
        markup.add(_buttonExamples, _buttonSignUp, _buttonLearnMore, _buttonPrice)
        bot.send_message(message.chat.id, text="Идем дальше".format(message.from_user), reply_markup=markup)

    elif (nowcode == "from_general_point_tattoo"):
        if (message.text == "Посмотреть примеры работ"):
            nowcode = "check_examples"
            takedMessage = True
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            _buttonEyebrows = types.KeyboardButton("Брови")
            _buttonEyelids = types.KeyboardButton("Веки")
            _buttonLips = types.KeyboardButton("Губы")
            _buttonGoBack = types.KeyboardButton("Назад")
            markup.add(_buttonEyebrows, _buttonEyelids, _buttonLips, _buttonGoBack)
            bot.send_message(message.chat.id, text="Какие примеры хотите посмотреть?".format(message.from_user), reply_markup=markup)

        if (message.text == "Записаться"):
            nowcode = "wait_contact"
            takedMessage = True
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            button = types.KeyboardButton('Отправить контакты', request_contact=True)
            markup.add(button)
            bot.send_message(message.chat.id, "Отлично, давайте познакомимся поближе!", reply_markup=markup)

        if (message.text == "Узнать больше о татуаже"):
            takedMessage = True
            bot.send_message(message.chat.id, text="Тут часто задаваемые вопросы".format(message.from_user))

        if (message.text == "Узнать прайс"):
            takedMessage = True
            bot.send_message(message.chat.id, text=LargeMessages.aboutPrice.format(message.from_user))

    elif(nowcode == "wait_contact"):
        takedMessage = True
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        button = types.KeyboardButton('Отправить контакты', request_contact=True)
        markup.add(button)
        bot.send_message(message.chat.id, "Вам нужно разрешить боту доступ к контактам. \n Попробуйте еще раз.", reply_markup=markup)

    elif (nowcode == "check_examples"):
        if (message.text == "Брови"):
            takedMessage = True
            bot.send_message(message.chat.id, text="Примеры \n\n волосковой техники и пудрового напыления".format(message.from_user),
                             parse_mode='Markdown')
            image_paths = [os.path.join("other/PhotoExamplesTattooing/Eyebrows/Voloskovaya", file) for file in
                           os.listdir("other/PhotoExamplesTattooing/Eyebrows/Voloskovaya") if
                           file.endswith(('.png', '.jpg', '.jpeg'))]
            media_group = [telebot.types.InputMediaPhoto(open(image_path, 'rb')) for image_path in image_paths]
            bot.send_media_group(message.chat.id, media_group)

            image_paths = [os.path.join("other/PhotoExamplesTattooing/Eyebrows/Pydrovoe_napilenie", file) for file in
                           os.listdir("other/PhotoExamplesTattooing/Eyebrows/Pydrovoe_napilenie") if
                           file.endswith(('.png', '.jpg', '.jpeg'))]
            media_group = [telebot.types.InputMediaPhoto(open(image_path, 'rb')) for image_path in image_paths]
            bot.send_media_group(message.chat.id, media_group)

        if (message.text == "Веки"):
            takedMessage = True
            image_paths = [os.path.join("other/PhotoExamplesTattooing/Eyelids", file) for file in
                           os.listdir("other/PhotoExamplesTattooing/Eyelids") if
                           file.endswith(('.png', '.jpg', '.jpeg'))]
            media_group = [telebot.types.InputMediaPhoto(open(image_path, 'rb')) for image_path in image_paths]
            bot.send_media_group(message.chat.id, media_group)

        if (message.text == "Губы"):
            takedMessage = True
            image_paths = [os.path.join("other/PhotoExamplesTattooing/Lips", file) for file in
                           os.listdir("other/PhotoExamplesTattooing/Lips") if
                           file.endswith(('.png', '.jpg', '.jpeg'))]
            media_group = [telebot.types.InputMediaPhoto(open(image_path, 'rb')) for image_path in image_paths]
            bot.send_media_group(message.chat.id, media_group)

        if (message.text == "Назад"):
            takedMessage = True
            nowcode = "from_general_point_tattoo"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            _buttonExamples = types.KeyboardButton("Посмотреть примеры работ")
            _buttonSignUp = types.KeyboardButton("Записаться")
            _buttonLearnMore = types.KeyboardButton("Узнать больше о татуаже")
            _buttonPrice = types.KeyboardButton("Узнать прайс")
            markup.add(_buttonExamples, _buttonSignUp, _buttonLearnMore, _buttonPrice)
            bot.send_message(message.chat.id, text="Возвращаемся. Что хотите узнать дальше?".format(message.from_user), reply_markup=markup)

    elif (nowcode == "make_appointment"):
        if (message.text == "Хочу на консультацию"):
            takedMessage = True
            nowcode = "make_appointment_final"

            _user.want_consult = True

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            _buttonMake = types.KeyboardButton("Записаться")
            markup.add(_buttonMake)
            bot.send_message(message.chat.id, text="Хорошо, давайте запишемся.".format(message.from_user), reply_markup=markup)
        else:
            if (message.text == "Брови"):
                takedMessage = True
                _user.appointment_zone = Zones.eyebrows
            elif (message.text == "Веки"):
                takedMessage = True
                _user.appointment_zone = Zones.eyelids
            elif (message.text == "Губы"):
                takedMessage = True
                _user.appointment_zone = Zones.lips

            if (takedMessage):
                nowcode = "make_appointment_zone"
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                _buttonYes = types.KeyboardButton("Да")
                _buttonNo = types.KeyboardButton("Нет")
                markup.add(_buttonYes, _buttonNo)
                bot.send_message(message.chat.id, text="Вы уже делали тауаж на этой зоне ранее?".format(message.from_user), reply_markup=markup)

    elif (nowcode == "make_appointment_zone"):
        if (message.text == "Да"):
            takedMessage = True
            nowcode = "make_appointment_where"
            _user.delalaTattoo_v_zone = True

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            _buttonYes = types.KeyboardButton("Да")
            _buttonNo = types.KeyboardButton("Нет")
            markup.add(_buttonYes, _buttonNo)
            bot.send_message(message.chat.id, text="В нашем центре BROWushka?".format(message.from_user), reply_markup=markup)
        elif (message.text == "Нет"):
            takedMessage = True
            nowcode = "make_appointment_final"
            _user.delalaTattoo_v_zone = False

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            _buttonPrice = types.KeyboardButton("Узнать прайс")
            _buttonMake = types.KeyboardButton("Записаться")
            markup.add(_buttonPrice, _buttonMake)
            bot.send_message(message.chat.id, text="Хорошо. Что делаем дальше?".format(message.from_user), reply_markup=markup)

    elif (nowcode == "make_appointment_where"):
        if (message.text == "Да"):
            takedMessage = True
            nowcode = "make_appointment_final"
            _user.delalaTattoo_v_Broowushka = True

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            _buttonPrice = types.KeyboardButton("Узнать прайс")
            _buttonMake = types.KeyboardButton("Записаться")
            markup.add(_buttonPrice, _buttonMake)
            bot.send_message(message.chat.id, text="Супер! Мы безумно ценим тех, кто с нами НАДОЛГО и не променяет ни какого другого! \nПоэтому дарим ВАМ скидку на обновление 20% от стоимости первичной процедуры в прайсе.".format(message.from_user), reply_markup=markup)
        elif (message.text == "Нет"):
            takedMessage = True
            nowcode = "make_appointment_photo_consult"

            _user.delalaTattoo_v_Broowushka = False

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            _buttonPhoto = types.KeyboardButton("Прислать фото зоны мастеру")
            _buttonConsult = types.KeyboardButton("Прийти на бесплатную консультацию")
            markup.add(_buttonConsult, _buttonPhoto)
            bot.send_message(message.chat.id, text="Мы не всегда берёмся за работу других мастеров. Только если мы уверены, что получится натурально и красиво 😍 \nСкажите, как вам будет удобнее:".format(
                                 message.from_user), reply_markup=markup)

    elif (nowcode == "make_appointment_photo_consult"):
        if (message.text == "Прислать фото зоны мастеру"):
            takedMessage = True
            nowcode = "make_appointment_end"
            _user.want_send_photo = True

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            _buttonPhone = types.KeyboardButton("Позвонил")
            _buttonWatsUp = types.KeyboardButton("Отписал в воцап")
            markup.add(_buttonPhone, _buttonWatsUp)
            bot.send_message(message.chat.id,
                             text="Вам будет удобнее, чтобы наш аминистартор позвонил или написал в воцап?".format(
                                 message.from_user), reply_markup=markup)

        elif (message.text == "Прийти на бесплатную консультацию"):
            takedMessage = True
            nowcode = "make_appointment_end"
            _user.want_consult = True

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            _buttonPhone = types.KeyboardButton("Позвонил")
            _buttonWatsUp = types.KeyboardButton("Отписал в воцап")
            markup.add(_buttonPhone, _buttonWatsUp)
            bot.send_message(message.chat.id,
                             text="Вам будет удобнее, чтобы наш аминистартор позвонил или написал в воцап?".format(
                                 message.from_user), reply_markup=markup)

    elif (nowcode == "make_appointment_final"):
        if (message.text == "Узнать прайс"):
            takedMessage = True
            nowcode = "make_appointment_end"
            image_paths = [os.path.join("other/Price/PriceTattoo", file) for file in
                           os.listdir("other/Price/PriceTattoo") if
                           file.endswith(('.png', '.jpg', '.jpeg'))]
            media_group = [telebot.types.InputMediaPhoto(open(image_path, 'rb')) for image_path in image_paths]
            bot.send_media_group(message.chat.id, media_group)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            _buttonPhone = types.KeyboardButton("Позвонил")
            _buttonWatsUp = types.KeyboardButton("Отписал в воцап")
            markup.add(_buttonPhone, _buttonWatsUp)
            bot.send_message(message.chat.id, text="Вам будет удобнее, чтобы наш аминистартор позвонил или написал в воцап?".format(message.from_user), reply_markup=markup)
        elif (message.text == "Записаться"):
            takedMessage = True
            nowcode = "make_appointment_end"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            _buttonPhone = types.KeyboardButton("Позвонил")
            _buttonWatsUp = types.KeyboardButton("Отписал в воцап")
            markup.add(_buttonPhone, _buttonWatsUp)
            bot.send_message(message.chat.id, text="Вам будет удобнее, чтобы наш аминистартор позвонил или написал в воцап?".format(message.from_user), reply_markup=markup)

    elif (nowcode == "make_appointment_end"):
        if (message.text == "Позвонил"):
            takedMessage = True
            _user.communication_method = EnumCommunicationMethod.Call
        elif (message.text == "Отписал в воцап"):
            takedMessage = True
            _user.communication_method = EnumCommunicationMethod.WhatsApp

        if (takedMessage == True):
            nowcode = "pre_root"

            _user.procedure = Procedures.tattoo

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            _buttonBack = types.KeyboardButton("Вернуться в начало")
            markup.add(_buttonBack)
            bot.send_message(message.chat.id, text=LargeMessages.appointment_final.format(message.from_user), reply_markup=markup)

            sendMessageToAdmin()

    elif (nowcode == "pre_root"):
        if(message.text == "Вернуться в начало"):
            takedMessage = True
            nowcode = "root"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            _buttonImClient = types.KeyboardButton("👩 Я клиент")
            _buttonImMaster = types.KeyboardButton("👑 Я мастер")
            markup.add(_buttonImClient, _buttonImMaster)
            bot.send_message(message.chat.id, text=LargeMessages.root.format(message.from_user), reply_markup=markup)

    #------------------------------ТУТ ВЕТКА ОСВЕТЛЕНИЯ (Левая правая часть)------------------------------------------

    elif (nowcode == "tattoo_lightening_correct"):
        if (message.text == "Да"):
            takedMessage = True
            nowcode = "tattoo_lightening_yes"

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            button = types.KeyboardButton('Отправить контакты', request_contact=True)
            markup.add(button)
            bot.send_message(message.chat.id, "Отлично, давайте познакомимся поближе!", reply_markup=markup)

        elif (message.text == "Нет"):
            takedMessage = True
            nowcode = "tattoo_lightening_no"

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            _buttonYes = types.KeyboardButton("Да")
            _buttonGoBack = types.KeyboardButton("Обратно")
            markup.add(_buttonYes, _buttonGoBack)
            bot.send_message(message.chat.id, "Рассказать вам подробнее про процедуру татуажа?", reply_markup=markup)

    elif (nowcode == "tattoo_lightening_no"):
        if (message.text == "Да"):
            takedMessage = True
            nowcode = "client_what"

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            _buttonEyebrows = types.KeyboardButton("Брови")
            _buttonLips = types.KeyboardButton("Губы")
            _buttonEyelids = types.KeyboardButton("Веки")
            _buttonCamouflage = types.KeyboardButton("Камуфляж")
            markup.add(_buttonEyebrows, _buttonLips, _buttonEyelids, _buttonCamouflage)
            bot.send_message(message.chat.id, text="Что конкретно?".format(message.from_user), reply_markup=markup)

        elif (message.text == "Обратно"):
            takedMessage = True
            nowcode = "client_morerelevant"

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            _buttonTattooing = types.KeyboardButton("Татуаж")
            _buttonBrighteningTattoo = types.KeyboardButton("Осветление татуажа")
            markup.add(_buttonTattooing, _buttonBrighteningTattoo)
            bot.send_message(message.chat.id, text="Что для вас сейчас актуальнее?".format(message.from_user),
                             reply_markup=markup)

    elif (nowcode == "tattoo_lightening_info"):
        if (message.text == "Прайс на осветление татуажа" or message.text == "Дальше"):
            takedMessage = True
            nowcode = "tattoo_lightening_make_appointment"

            image_paths = [os.path.join("other/Price/PriceDeletion", file) for file in
                           os.listdir("other/Price/PriceDeletion") if
                           file.endswith(('.png', '.jpg', '.jpeg'))]
            media_group = [telebot.types.InputMediaPhoto(open(image_path, 'rb')) for image_path in image_paths]
            bot.send_media_group(message.chat.id, media_group)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            _buttonLightening = types.KeyboardButton("Осветление")
            _buttonConsult = types.KeyboardButton("Консультация")
            markup.add(_buttonLightening, _buttonConsult)
            bot.send_message(message.chat.id, text="Подобрать вам время на осветление татуажа или консультацию?".format(message.from_user), reply_markup=markup)

        elif (message.text == "Способы осветления"):
            takedMessage = True
            nowcode = "tattoo_lightening_info"

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            _buttonNext = types.KeyboardButton("Прайс на осветление татуажа")
            markup.add(_buttonNext)
            bot.send_message(message.chat.id, text=LargeMessages.aboutTattoo_lightening.format(message.from_user),
                             reply_markup=markup)

    elif (nowcode == "tattoo_lightening_make_appointment"):
        if (message.text == "Осветление"):
            takedMessage = True

        elif (message.text == "Консультация"):
            takedMessage = True
            _user.want_consult = True

        if (takedMessage == True):
            nowcode = "tattoo_lightening_final"

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            _buttonLightening = types.KeyboardButton("Позвонил")
            _buttonConsult = types.KeyboardButton("Отписал в воцап")
            markup.add(_buttonLightening, _buttonConsult)
            bot.send_message(message.chat.id, text="Вам будет удобнее, чтобы наш аминистартор позвонил или написал в воцап?".format(
                                 message.from_user), reply_markup=markup)

    elif (nowcode == "tattoo_lightening_final"):
        if (message.text == "Позвонил"):
            takedMessage = True
            _user.communication_method = EnumCommunicationMethod.Call

        elif (message.text == "Отписал в воцап"):
            takedMessage = True
            _user.communication_method = EnumCommunicationMethod.WhatsApp

        if (takedMessage == True):
            nowcode = "pre_root"

            _user.procedure = Procedures.lightening_tatto

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            _buttonBack = types.KeyboardButton("Вернуться в начало")
            markup.add(_buttonBack)
            bot.send_message(message.chat.id, text=LargeMessages.appointment_final.format(message.from_user),
                             reply_markup=markup)

            sendMessageToAdmin()

    if (takedMessage == False):
        bot.send_message(message.chat.id, text="Пожалуйста, используйте кнопки или команду /start")

    print(nowcode)

def sendMessageToAdmin():
    global _user
    bot.send_message(_AdminID, text="Новая запись! \n\n"
                                    f"Имя/Фамилия: {_user.first_name} {_user.last_name} \n\n"
                                    f"Услуга: {enumProcedures.returnRuName(_user.procedure)}\n"
                                    f"Зона таттуажа: {enumZones.returnRuName(_user.appointment_zone)}\n"
                                    f"Делал ли клиент таттуаж в этой зоне: {_user.delalaTattoo_v_zone}\n"
                                    f"Если делал, то в Бровушке?: {_user.delalaTattoo_v_Broowushka}\n"
                                    f"Клиент хочет отослать фото зоны чтобы обсудить таттуаж с мастером: {_user.want_send_photo}\n\n"
                                    f"Клиент хочет бесплатную консультацию?: {_user.want_consult}\n"
                                    f"Метод связи: {communication_method_with_user.returnRuName(_user.communication_method)}\n"
                                    f"Номер: {_user.phone_number}")

bot.polling(none_stop=True)