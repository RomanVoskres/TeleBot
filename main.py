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
_AdminID = 772136193 # 391388060

_user = user.User

# Обработка контакта
@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    global _user
    if message.contact is not None and _user.phone_number is None:
        phone_number = message.contact.phone_number
        first_name = message.contact.first_name
        last_name = message.contact.last_name
        user_id = message.contact.user_id

        _user.phone_number = phone_number
        _user.first_name = first_name
        _user.last_name = last_name
        _user.user_id = user_id

        #Обнуление что еще не выбрано
        #_user.procedure = None
        #_user.appointment_zone = None  # запоминает зону макияжа пользователя
        _user.communication_method = None  # запоминает метод связи с пользователем
        _user.want_consult = False  # Может хотеть на консультацию
        _user.delalaTattoo_v_Broowushka = False
        _user.delalaTattoo_v_zone = False
        _user.want_send_photo = False

        if _user.procedure is Procedures.tattoo: # Татуаж
            if _user.comuflage is True:
                message_text = f"{first_name}, очень приятно! \nВы выбрали 'камуфляж'.)"

                markup = types.InlineKeyboardMarkup()
                _buttonMake = types.InlineKeyboardButton("Хочу записаться", callback_data="make_appointment_end")
                _buttonPrice = types.InlineKeyboardButton("Узнать прайс", callback_data="price_tattoo")
                _buttonCounseling = types.InlineKeyboardButton("Хочу на консультацию", callback_data="want_consult")
                markup.add(_buttonMake, _buttonPrice, _buttonCounseling)
                bot.send_message(message.chat.id, text=message_text.format(message.from_user), reply_markup=markup)
            else:
                message_text = f"{first_name}, очень приятно! \nВы уже делали тауаж на этой зоне ранее? (Вы выбрали зону {enumZones.returnRuName(_user.appointment_zone)})"

                markup = types.InlineKeyboardMarkup()
                _buttonYes = types.InlineKeyboardButton("Да", callback_data="make_appointment_zone_yes")
                _buttonNo = types.InlineKeyboardButton("Нет", callback_data="make_appointment_zone_no")
                _buttonCounseling = types.InlineKeyboardButton("Хочу на консультацию", callback_data="want_consult")
                markup.add(_buttonYes, _buttonNo, _buttonCounseling)
                bot.send_message(message.chat.id, text=message_text.format(message.from_user), reply_markup=markup)
        else: # Осветление таттуажа
            message_text = f"{first_name}, очень приятно! \nЧто вы хотите узнать?)"

            markup = types.InlineKeyboardMarkup()
            _buttonPrice = types.InlineKeyboardButton("Прайс на осветление татуажа", callback_data="make_lightening_Price")
            _buttonMethods = types.InlineKeyboardButton("Способы осветления", callback_data="make_lightening_Methods")
            markup.add(_buttonPrice, _buttonMethods)
            bot.send_message(message.chat.id, text=message_text.format(message.from_user), reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, отправьте контакт, используя кнопку 'Отправить контакты'")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global _user
    if call.data == "client":
        _user.procedure = None

        markup = types.InlineKeyboardMarkup()
        _buttonTattooing = types.InlineKeyboardButton("Татуаж", callback_data="tattoo")
        _buttonBrighteningTattoo = types.InlineKeyboardButton("Осветление татуажа", callback_data="tattoo_lightening")
        markup.add(_buttonTattooing, _buttonBrighteningTattoo)
        bot.send_message(call.message.chat.id, text="Что для вас сейчас актуальнее?".format(call.message.from_user),
                         reply_markup=markup)
    elif call.data == "master":
        _user.procedure = None

        markup = types.InlineKeyboardMarkup()
        _buttonWantKnow = types.InlineKeyboardButton("Хочу узнать про повышение квалификации", callback_data="like_to_know")
        _buttonLearning = types.InlineKeyboardButton("Хочу пройти обучение с 0", callback_data="want_training")
        _buttonPoleznyashki = types.InlineKeyboardButton("Хочу полезняшек", callback_data="some_goodies")
        markup.add(_buttonWantKnow, _buttonLearning, _buttonPoleznyashki)
        bot.send_message(call.message.chat.id, text=LargeMessages.aboutMaster.format(call.message.from_user), reply_markup=markup)
    elif call.data == "tattoo":
        _user.procedure = Procedures.tattoo

        markup = types.InlineKeyboardMarkup()
        _buttonEyebrows = types.InlineKeyboardButton("Брови", callback_data="tattoo_brows")
        _buttonLips = types.InlineKeyboardButton("Губы", callback_data="tattoo_lips")
        _buttonEyelids = types.InlineKeyboardButton("Веки", callback_data="tattoo_eyelids")
        _buttonCamouflage = types.InlineKeyboardButton("Камуфляж", callback_data="tattoo_camouflage")
        markup.add(_buttonEyebrows, _buttonLips, _buttonEyelids, _buttonCamouflage)
        bot.send_message(call.message.chat.id, text="Что конкретно?".format(call.message.from_user), reply_markup=markup)
    elif call.data == "tattoo_lightening":
        _user.procedure = Procedures.lightening_tatto

        markup = types.InlineKeyboardMarkup()
        _buttonYes = types.InlineKeyboardButton("Да", callback_data="yes_lightening")
        _buttonNo = types.InlineKeyboardButton("Нет", callback_data="no_lightening")
        markup.add(_buttonYes, _buttonNo)
        bot.send_message(call.message.chat.id, text="У вас есть старый татуаж, который хотелось бы удалить или просто сделать светлее, правильно?".format(
                             call.message.from_user), reply_markup=markup)

    if _user.procedure is Procedures.tattoo:
        if call.data == "tattoo_brows":
            _user.appointment_zone = Zones.eyebrows
            bot.send_message(call.message.chat.id, text=LargeMessages.aboutEyebrows.format(call.message.from_user))

            markup = types.InlineKeyboardMarkup()
            _buttonNext = types.InlineKeyboardButton("Дальше", callback_data="general_point_tattoo")
            _buttonBack = types.InlineKeyboardButton("Назад", callback_data="tattoo")
            markup.add(_buttonNext, _buttonBack)
        elif call.data == "tattoo_lips":
            _user.appointment_zone = Zones.lips
            bot.send_message(call.message.chat.id, text=LargeMessages.aboutLips.format(call.message.from_user))

            markup = types.InlineKeyboardMarkup()
            _buttonNext = types.InlineKeyboardButton("Дальше", callback_data="general_point_tattoo")
            _buttonBack = types.InlineKeyboardButton("Назад", callback_data="tattoo")
            markup.add(_buttonNext, _buttonBack)
        elif call.data == "tattoo_eyelids":
            _user.appointment_zone = Zones.eyelids
            bot.send_message(call.message.chat.id, text=LargeMessages.aboutEyelids.format(call.message.from_user))

            markup = types.InlineKeyboardMarkup()
            _buttonNext = types.InlineKeyboardButton("Дальше", callback_data="general_point_tattoo")
            _buttonBack = types.InlineKeyboardButton("Назад", callback_data="tattoo")
            markup.add(_buttonNext, _buttonBack)
        elif call.data == "tattoo_camouflage":
            _user.comuflage = True
            bot.send_message(call.message.chat.id, text=LargeMessages.aboutCamouflage_0.format(call.message.from_user))
            bot.send_message(call.message.chat.id, text=LargeMessages.aboutCamouflage_1.format(call.message.from_user))

            markup = types.InlineKeyboardMarkup()
            _buttonNext = types.InlineKeyboardButton("Дальше", callback_data="general_point_tattoo")
            _buttonBack = types.InlineKeyboardButton("Назад", callback_data="tattoo")
            markup.add(_buttonNext, _buttonBack)
        elif call.data == "general_point_tattoo":
            markup = types.InlineKeyboardMarkup()
            _buttonExamples = types.InlineKeyboardButton("Посмотреть примеры работ", callback_data="check_examples_tattoo")
            _buttonSignUp = types.InlineKeyboardButton("Записаться", callback_data="")
            _buttonLearnMore = types.InlineKeyboardButton("Узнать больше о татуаже", callback_data="about_tattoo")
            _buttonPrice = types.InlineKeyboardButton("Узнать прайс", callback_data="know_price")
            markup.add(_buttonExamples, _buttonSignUp, _buttonLearnMore, _buttonPrice)
            bot.send_message(call.message.chat.id, text="Идем дальше".format(call.message.from_user), reply_markup=markup)
        elif call.data == "check_examples_tattoo":
            markup = types.InlineKeyboardMarkup()
            _buttonEyebrows = types.InlineKeyboardButton("Брови", callback_data="check_examples_tattoo_brows")
            _buttonEyelids = types.InlineKeyboardButton("Веки", callback_data="check_examples_tattoo_eyelids")
            _buttonLips = types.InlineKeyboardButton("Губы", callback_data="check_examples_tattoo_lips")
            markup.add(_buttonEyebrows, _buttonEyelids, _buttonLips)
            bot.send_message(call.message.chat.id, text="Какие примеры хотите посмотреть?".format(call.message.from_user), reply_markup=markup)
        elif call.data == "check_examples_tattoo_brows":
            bot.send_message(call.message.chat.id,
                             text="Примеры \n\n волосковой техники и пудрового напыления".format(call.message.from_user),
                             parse_mode='Markdown')
            image_paths = [os.path.join("other/PhotoExamplesTattooing/Eyebrows/Voloskovaya", file) for file in
                           os.listdir("other/PhotoExamplesTattooing/Eyebrows/Voloskovaya") if
                           file.endswith(('.png', '.jpg', '.jpeg'))]
            media_group = [telebot.types.InputMediaPhoto(open(image_path, 'rb')) for image_path in image_paths]
            bot.send_media_group(call.message.chat.id, media_group)

            image_paths = [os.path.join("other/PhotoExamplesTattooing/Eyebrows/Pydrovoe_napilenie", file) for file in
                           os.listdir("other/PhotoExamplesTattooing/Eyebrows/Pydrovoe_napilenie") if
                           file.endswith(('.png', '.jpg', '.jpeg'))]
            media_group = [telebot.types.InputMediaPhoto(open(image_path, 'rb')) for image_path in image_paths]
            bot.send_media_group(call.message.chat.id, media_group)
        elif call.data == "check_examples_tattoo_eyelids":
            image_paths = [os.path.join("other/PhotoExamplesTattooing/Eyelids", file) for file in
                           os.listdir("other/PhotoExamplesTattooing/Eyelids") if
                           file.endswith(('.png', '.jpg', '.jpeg'))]
            media_group = [telebot.types.InputMediaPhoto(open(image_path, 'rb')) for image_path in image_paths]
            bot.send_media_group(call.message.chat.id, media_group)
        elif call.data == "check_examples_tattoo_lips":
            image_paths = [os.path.join("other/PhotoExamplesTattooing/Lips", file) for file in
                           os.listdir("other/PhotoExamplesTattooing/Lips") if
                           file.endswith(('.png', '.jpg', '.jpeg'))]
            media_group = [telebot.types.InputMediaPhoto(open(image_path, 'rb')) for image_path in image_paths]
            bot.send_media_group(call.message.chat.id, media_group)
        elif call.data == "know_price":
            bot.send_message(call.message.chat.id, text=LargeMessages.aboutPrice.format(call.message.from_user))
        elif call.data == "about_tattoo":
            markup = types.InlineKeyboardMarkup()
            _buttonhowlong = types.InlineKeyboardButton("Как долго держится татуаж?", callback_data="about_tattoo_howlong")
            _buttoncorrect = types.InlineKeyboardButton("Зачем нужна коррекция?", callback_data="about_tattoo_correct")
            _buttoncando = types.InlineKeyboardButton("Можно ли делать татуаж беременным и на гв?", callback_data="about_tattoo_cando")
            _buttonotkuda = types.InlineKeyboardButton("Откуда берутся синие брови?", callback_data="about_tattoo_otkuda")
            _buttonhurt = types.InlineKeyboardButton("Татуаж - это больно?", callback_data="about_tattoo_hurt")
            _buttonalergy = types.InlineKeyboardButton("Бывает аллергия на татуаж?", callback_data="about_tattoo_alergy")
            _buttontehnicks = types.InlineKeyboardButton("В каких техниках вы работаете?", callback_data="about_tattoo_tehnicks")
            _buttonYarche = types.InlineKeyboardButton("А можно сделать ПОЯРЧЕ?", callback_data="about_tattoo_Yarche")
            _buttondorogo = types.InlineKeyboardButton("Почему так дорого?", callback_data="about_tattoo_dorogo")
            markup.row(_buttonhowlong, _buttoncorrect, _buttoncando, _buttonotkuda, _buttonhurt, _buttonalergy, _buttontehnicks, _buttonYarche, _buttondorogo)
            bot.send_message(call.message.chat.id, text="Часто задаваемые вопросы:".format(call.message.from_user),
                             reply_markup=markup)
        elif call.data == "about_tattoo_howlong":
            bot.send_message(call.message.chat.id, text=LargeMessages.about_tattoo_howlong.format(call.message.from_user))
        elif call.data == "about_tattoo_correct":
            bot.send_message(call.message.chat.id, text=LargeMessages.about_tattoo_correct.format(call.message.from_user))
        elif call.data == "about_tattoo_cando":
            bot.send_message(call.message.chat.id, text=LargeMessages.about_tattoo_cando.format(call.message.from_user))
        elif call.data == "about_tattoo_otkuda":
            bot.send_message(call.message.chat.id, text=LargeMessages.about_tattoo_otkuda.format(call.message.from_user))
        elif call.data == "about_tattoo_hurt":
            bot.send_message(call.message.chat.id, text=LargeMessages.about_tattoo_hurt.format(call.message.from_user))
        elif call.data == "about_tattoo_alergy":
            bot.send_message(call.message.chat.id, text=LargeMessages.about_tattoo_alergy.format(call.message.from_user))
        elif call.data == "about_tattoo_tehnicks":
            bot.send_message(call.message.chat.id, text=LargeMessages.about_tattoo_tehnicks.format(call.message.from_user))
        elif call.data == "about_tattoo_Yarche":
            bot.send_message(call.message.chat.id, text=LargeMessages.about_tattoo_Yarche.format(call.message.from_user))
        elif call.data == "about_tattoo_dorogo":
            bot.send_message(call.message.chat.id, text=LargeMessages.about_tattoo_dorogo.format(call.message.from_user))

        #Запись
        elif call.data == "signup":
            markup = types.InlineKeyboardMarkup()
            button_signup = types.InlineKeyboardButton('Отправить контакты', request_contact=True) #запрос
            markup.add(button_signup)
            bot.send_message(call.message.chat.id, "Отлично, давайте познакомимся поближе!", reply_markup=markup)

        elif call.data == "make_appointment_zone_yes":
            _user.delalaTattoo_v_zone = True

            markup = types.InlineKeyboardMarkup()
            _buttonYes = types.InlineKeyboardButton("Да", callback_data="make_appointment_incenter")
            _buttonNo = types.InlineKeyboardButton("Нет", callback_data="make_appointment_nocenter")
            markup.add(_buttonYes, _buttonNo)
            bot.send_message(call.message.chat.id, text="В нашем центре BROWushka?".format(call.message.from_user),
                             reply_markup=markup)
        elif call.data == "make_appointment_incenter":
            _user.delalaTattoo_v_Broowushka = True

            markup = types.InlineKeyboardMarkup()
            _buttonPrice = types.InlineKeyboardButton("Узнать прайс", callback_data="price_tattoo")
            _buttonMake = types.InlineKeyboardButton("Записаться", callback_data="make_appointment_end")
            markup.add(_buttonPrice, _buttonMake)
            bot.send_message(call.message.chat.id, text="Супер! Мы безумно ценим тех, кто с нами НАДОЛГО и не променяет ни какого другого! \nПоэтому дарим ВАМ скидку на обновление 20% от стоимости первичной процедуры в прайсе.".format(
                                 call.message.from_user), reply_markup=markup)
        elif call.data == "make_appointment_nocenter":
            _user.delalaTattoo_v_Broowushka = False

            markup = types.InlineKeyboardMarkup()
            _buttonSendPhoto = types.InlineKeyboardButton("Прислать фото зоны, на которой сделан татуаж?", callback_data="make_appointment_sendPhoto")
            _buttonConsult = types.InlineKeyboardButton("Прийти на бесплатную консультацию", callback_data="want_consult")
            markup.add(_buttonSendPhoto, _buttonConsult)
            bot.send_message(call.message.chat.id, text="Мы не всегда берёмся за работу других мастеров. Только если мы уверены, что получится натурально и красиво 😍 \nСкажите, как вам будет удобнее:".format(
                                 call.message.from_user), reply_markup=markup)
        elif call.data == "make_appointment_sendPhoto":
            _user.want_send_photo = True

            markup = types.InlineKeyboardMarkup()
            _buttonMake = types.InlineKeyboardButton("Записаться", callback_data="make_appointment_end")
            markup.add(_buttonMake)
            bot.send_message(call.message.chat.id, text="Хорошо, давайте запишемся.".format(call.message.from_user),
                             reply_markup=markup)
        elif call.data == "make_appointment_zone_no":
            _user.delalaTattoo_v_zone = False

            markup = types.InlineKeyboardMarkup()
            _buttonPrice = types.InlineKeyboardButton("Узнать прайс", callback_data="price_tattoo")
            _buttonMake = types.InlineKeyboardButton("Записаться", callback_data="make_appointment_end")
            markup.add(_buttonPrice, _buttonMake)
            bot.send_message(call.message.chat.id, text="Хорошо. Что делаем дальше?".format(call.message.from_user),
                             reply_markup=markup)
        elif call.data == "want_consult":
            _user.want_consult = True

            markup = types.InlineKeyboardMarkup()
            _buttonMake = types.InlineKeyboardButton("Записаться", callback_data="make_appointment_end")
            markup.add(_buttonMake)
            bot.send_message(call.message.chat.id, text="Хорошо, давайте запишемся.".format(call.message.from_user),
                             reply_markup=markup)
        elif call.data == "price_tattoo":
            if _user.appointment_zone is None: #прайс за осветление
                image_paths = [os.path.join("other/Price/PriceTattoo", file) for file in
                               os.listdir("other/Price/PriceTattoo") if
                               file.endswith(('.png', '.jpg', '.jpeg'))]
                media_group = [telebot.types.InputMediaPhoto(open(image_path, 'rb')) for image_path in image_paths]
                bot.send_media_group(call.message.chat.id, media_group)
            else:
                image_paths = [os.path.join("other/Price/PriceDeletion", file) for file in
                               os.listdir("other/Price/PriceDeletion") if
                               file.endswith(('.png', '.jpg', '.jpeg'))]
                media_group = [telebot.types.InputMediaPhoto(open(image_path, 'rb')) for image_path in image_paths]
                bot.send_media_group(call.message.chat.id, media_group)

        elif call.data == "make_appointment_end": #-----------------------запись финал-----------------
            markup = types.InlineKeyboardMarkup()
            _buttonPhone = types.InlineKeyboardButton("Позвонил", callback_data="call_connect")
            _buttonWatsUp = types.InlineKeyboardButton("Отписал в воцап", callback_data="whatsapp_connect")
            markup.add(_buttonPhone, _buttonWatsUp)
            bot.send_message(call.message.chat.id, text="Вам будет удобнее, чтобы наш администартор позвонил или написал в воцап?".format(
                                 call.message.from_user), reply_markup=markup)
        elif call.data == "call_connect":
            _user.communication_method = EnumCommunicationMethod.Call
            bot.send_message(call.message.chat.id, text=LargeMessages.appointment_final.format(call.message.from_user))
            sendMessageToAdmin() #сделать проверку есть ли запись чтобы не спамили
        elif call.data == "whatsapp_connect":
            _user.communication_method = EnumCommunicationMethod.WhatsApp
            bot.send_message(call.message.chat.id, text=LargeMessages.appointment_final.format(call.message.from_user))
            sendMessageToAdmin() #сделать проверку есть ли запись чтобы не спамили

    #------------------------------ТУТ ВЕТКА ОСВЕТЛЕНИЯ (Левая правая часть)------------------------------------------
    #_user.appointment_zone использовать None что будет значить - осветление
    if _user.procedure is Procedures.lightening_tatto:
        if call.data == "yes_lightening":
            markup = types.InlineKeyboardMarkup()
            button_signup = types.InlineKeyboardButton('Отправить контакты', request_contact=True)  # запрос
            markup.add(button_signup)
            bot.send_message(call.message.chat.id, text="Отлично, давайте познакомимся поближе!".format(call.message.from_user))
        elif call.data == "no_lightening": #Смена процедуры
            markup = types.InlineKeyboardMarkup()
            _buttonYes = types.InlineKeyboardButton("Да", callback_data="tattoo")
            _buttonNo = types.InlineKeyboardButton("Нет", callback_data="client")
            markup.add(_buttonYes, _buttonNo)
            bot.send_message(call.message.chat.id, text="Рассказать вам подробнее про процедуру татуажа?".format(call.message.from_user), reply_markup=markup)
        elif call.data == "make_lightening_Price":
            image_paths = [os.path.join("other/Price/PriceDeletion", file) for file in
                           os.listdir("other/Price/PriceDeletion") if
                           file.endswith(('.png', '.jpg', '.jpeg'))]
            media_group = [telebot.types.InputMediaPhoto(open(image_path, 'rb')) for image_path in image_paths]
            bot.send_media_group(call.message.chat.id, media_group)

            markup = types.InlineKeyboardMarkup()
            _buttonLightening = types.InlineKeyboardButton("Осветление", callback_data="make_lightening_end")
            _buttonConsult = types.InlineKeyboardButton("Консультация", callback_data="make_lightening_end_consult")
            markup.add(_buttonLightening, _buttonConsult)
            bot.send_message(call.message.chat.id, text="Подобрать вам время на осветление татуажа или консультацию?".format(call.message.from_user), reply_markup=markup)
        elif call.data == "make_lightening_Methods":
            bot.send_message(call.message.chat.id, text=LargeMessages.aboutTattoo_lightening.format(call.message.from_user))

        elif call.data == "make_lightening_end_consult":  # -----------------------запись финал + Консультация
            _user.want_consult = True

            markup = types.InlineKeyboardMarkup()
            _buttonPhone = types.InlineKeyboardButton("Позвонил", callback_data="call_connect")
            _buttonWatsUp = types.InlineKeyboardButton("Отписал в воцап", callback_data="whatsapp_connect")
            markup.add(_buttonPhone, _buttonWatsUp)
            bot.send_message(call.message.chat.id, text="Вам будет удобнее, чтобы наш администартор позвонил или написал в воцап?".format(call.message.from_user), reply_markup=markup)
        elif call.data == "make_lightening_end":  # -----------------------запись финал-----------------
            markup = types.InlineKeyboardMarkup()
            _buttonPhone = types.InlineKeyboardButton("Позвонил", callback_data="call_connect")
            _buttonWatsUp = types.InlineKeyboardButton("Отписал в воцап", callback_data="whatsapp_connect")
            markup.add(_buttonPhone, _buttonWatsUp)
            bot.send_message(call.message.chat.id, text="Вам будет удобнее, чтобы наш администартор позвонил или написал в воцап?".format(call.message.from_user), reply_markup=markup)
        elif call.data == "call_connect":
            _user.communication_method = EnumCommunicationMethod.Call
            bot.send_message(call.message.chat.id, text=LargeMessages.appointment_final.format(call.message.from_user))
            sendMessageToAdmin()  # сделать проверку есть ли запись чтобы не спамили
        elif call.data == "whatsapp_connect":
            _user.communication_method = EnumCommunicationMethod.WhatsApp
            bot.send_message(call.message.chat.id, text=LargeMessages.appointment_final.format(call.message.from_user))
            sendMessageToAdmin()  # сделать проверку есть ли запись чтобы не спамили

    # ----------------------------------------- ТУТ ВЕТКА МАСТЕРА ----------------------------------------------------
    if _user.procedure is None:
        if call.data == "like_to_know":
            markup = types.InlineKeyboardMarkup()
            _buttonArrows = types.InlineKeyboardButton("Стрелки в технике Eye Pollen", callback_data="master_tehnic_price_1")
            _buttonEyeBrows = types.InlineKeyboardButton("Пудровые брови", callback_data="master_tehnic_price_1")
            _buttonLips = types.InlineKeyboardButton("Губы", callback_data="master_tehnic_price_1")
            _buttonVoloski = types.InlineKeyboardButton("Волоски", callback_data="master_tehnic_price_2")
            markup.add(_buttonArrows, _buttonEyeBrows, _buttonLips, _buttonVoloski)
            bot.send_message(call.message.chat.id, text=LargeMessages.aboutQualifications.format(call.message.from_user), reply_markup=markup)
        elif call.data == "master_tehnic_price_1":
            image_paths = [os.path.join("other/PriceTraining/Couple", file) for file in
                           os.listdir("other/PriceTraining/Couple") if
                           file.endswith(('.png', '.jpg', '.jpeg'))]
            media_group = [telebot.types.InputMediaPhoto(open(image_path, 'rb')) for image_path in image_paths]
            bot.send_media_group(call.message.chat.id, media_group)
        elif call.data == "master_tehnic_price_2":
            image_paths = [os.path.join("other/PriceTraining", file) for file in
                           os.listdir("other/PriceTraining") if
                           file.endswith(('.png', '.jpg', '.jpeg'))]
            media_group = [telebot.types.InputMediaPhoto(open(image_path, 'rb')) for image_path in image_paths]
            bot.send_media_group(call.message.chat.id, media_group)
        elif call.data == "want_training":
            markup = types.InlineKeyboardMarkup()
            _buttonSubscribe = types.InlineKeyboardButton("Подписаться на соцсети", callback_data="master_social")
            markup.add(_buttonSubscribe)
            bot.send_message(call.message.chat.id, text=LargeMessages.aboutLearning.format(call.message.from_user),
                             reply_markup=markup)
        elif call.data == "some_goodies":
            markup = types.InlineKeyboardMarkup()
            _buttonCheckList1 = types.InlineKeyboardButton("Чек-лист 'Не ложится пигмент. Что делать?'и", callback_data="some_goodies_checkNe")
            _buttonPlan = types.InlineKeyboardButton("Контент план на месяц", callback_data="some_goodies_content")
            _buttonCheckList2 = types.InlineKeyboardButton("Чек-лист про пигменты: 'Органика VS Минералы'", callback_data="some_goodies_checkPigment")
            _buttonGuide = types.InlineKeyboardButton("Гайд: 'Рассылки для бьюти мастера'", callback_data="some_goodies_guide")
            markup.add(_buttonCheckList1, _buttonPlan, _buttonCheckList2, _buttonGuide)
            bot.send_message(call.message.chat.id, text="Выбирай, моя красотка, что тебе актуальнее.".format(call.message.from_user),
                             reply_markup=markup)

        elif call.data == "some_goodies_checkNe":
            pdf_file_path = 'other/UsefulStuff/Не ложится пигмент check-list.pdf'
            try:
                with open(pdf_file_path, 'rb') as pdf_file:
                    bot.send_document(call.message.chat.id, pdf_file)
            except FileNotFoundError:
                bot.send_message(call.message.chat.id, "Извините, файл не найден.")
        elif call.data == "some_goodies_content":
            pdf_file_path = 'other/UsefulStuff/Контент-план Марина Шмойлова.pdf'
            try:
                with open(pdf_file_path, 'rb') as pdf_file:
                    bot.send_document(call.message.chat.id, pdf_file)
            except FileNotFoundError:
                bot.send_message(call.message.chat.id, "Извините, файл не найден.")
        elif call.data == "some_goodies_checkPigment":
            pdf_file_path = 'other/UsefulStuff/Органика vs Минералы check-list.pdf'
            try:
                with open(pdf_file_path, 'rb') as pdf_file:
                    bot.send_document(call.message.chat.id, pdf_file)
            except FileNotFoundError:
                bot.send_message(call.message.chat.id, "Извините, файл не найден.")
        elif call.data == "some_goodies_guide":
            pdf_file_path = 'other/UsefulStuff/Гайд рассылки для бьюти мастера.pdf'
            try:
                with open(pdf_file_path, 'rb') as pdf_file:
                    bot.send_document(call.message.chat.id, pdf_file)
            except FileNotFoundError:
                bot.send_message(call.message.chat.id, "Извините, файл не найден.")

        elif call.data == "master_qualifications_next":
            markup = types.InlineKeyboardMarkup()
            _buttonQuest = types.InlineKeyboardButton("Задать Марине лично вопрос", callback_data="master_quest")
            _buttonSocial = types.InlineKeyboardButton("Подписаться на соцсети", callback_data="master_social")
            _buttongoodies = types.InlineKeyboardButton("Полезняшки", callback_data="some_goodies")
            _buttonSubscribe = types.InlineKeyboardButton("Записаться на обучение", callback_data="master_make")
            markup.add(_buttonQuest, _buttonSocial, _buttongoodies, _buttonSubscribe)
            bot.send_message(call.message.chat.id, text="Ну что, моя королева, давай решим, куда двигаемся дальше?".format(call.message.from_user), reply_markup=markup)
        elif call.data == "master_quest":
            bot.send_contact(chat_id=call.message.chat.id, phone_number='+79601088966', first_name='Марина')
        elif call.data == "master_social":
            bot.send_message(call.message.chat.id, text=LargeMessages.aboutSocial.format(call.message.from_user))
        elif call.data == "master_make":
            _user.training_appointment_id = None
            bot.send_message(call.message.chat.id, text=LargeMessages.aboutTrainingAppointment.format(call.message.from_user))
            bot.send_message(call.message.chat.id, text=LargeMessages.formAppointment.format(call.message.from_user))
        elif call.data == "master_make_final":
            bot.send_message(call.message.chat.id, text="Анкета отправлена. Ожидайте.".format(call.message.from_user))

            bot.send_message(_AdminID, text="Новая анкета на обучение!".format(call.message.from_user))
            bot.forward_message(_AdminID, call.message.chat.id, _user.training_appointment_id)

    _user.last_call_data = call.data

@bot.message_handler(content_types=['text'])
def getMessage(message): #Тут принимается сообщение пользователя для записи на мастера
    if _user.last_call_data == "master_make":
        _user.training_appointment_id = message.message_id

        markup = types.InlineKeyboardMarkup()
        _buttonYes = types.InlineKeyboardButton("Да", callback_data="master_make_final")
        _buttonNo = types.InlineKeyboardButton("Нет", callback_data="master_make")
        markup.add(_buttonYes, _buttonNo)
        bot.send_message(message.chat.id, text="Вы проверили свою анкету и уверены, что хотите её отправить?".format(message.from_user),
                         reply_markup=markup)

@bot.message_handler(commands=['start'])
def main(message):
    markup = types.InlineKeyboardMarkup()
    _buttonImClient = types.InlineKeyboardButton("👩 Я клиент", callback_data="client")
    _buttonImMaster = types.InlineKeyboardButton("👑 Я мастер", callback_data="master")

    markup.add(_buttonImClient, _buttonImMaster)
    bot.send_message(message.chat.id, text=LargeMessages.root.format(message.from_user), reply_markup=markup)



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