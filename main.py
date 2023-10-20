import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State


state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot("6482416242:AAE8lKkLFaGalo8sHS-QQDnzhPQydaMLrtA",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "опросик"  # Можно менять текст
text_button_1 = "Как приготовить гречку?"  # Можно менять текст
text_button_2 = "Рецепт московского салата"  # Можно менять текст
text_button_3 = "Рецепт плова"  # Можно менять текст


menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Привет! Я бот,который покажет как приготовить несколько простых блюд.Выбери что-нибудь из меню.',  # Можно менять текст
        reply_markup=menu_keyboard)

@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Супер! *Как вас зовут?*')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Отлично! Какое [блюдо](https://telegra.ph/Primery-blyud-10-17) ваше самое любимое?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'Спасибо за ответ, посмотрим рецепты?', reply_markup=menu_keyboard)  # Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Чтобы приготовить рассыпчатую гречку, возьмите: 1 стакан гречки, 2 стакана воды, соль по вкусу.Промойте крупу, в кипящую подсоленную воду добавьте гречку и варите на медленном огне 15-20 минут. Оставьте настояться на 5-10 минут и подавайте горячей. Приятного аппетита! [Картинка гречневой каши](https://mykaleidoscope.ru/x/uploads/posts/2022-09/1663636306_1-mykaleidoscope-ru-p-grechnevaya-kasha-yeda-krasivo-1.jpg)", reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Чтобы приготовить Московский салат, нарежьте, заранее подготовленные, кубиками: вареный картофель, морковь, яйца, мясо и огурцы. Добавьте зеленый горошек, майонез, соль и перец, тщательно перемешайте. Охладите и подавайте салат. [Картинка салата](https://cookhelp.ru/upload/recipes/salat_moskovskiy_s_kopchenoy_kolbasoy.jpg)", reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "1)Сначала нужно обжарить мясо в казане на растительном масле до золотистого цвета.2) Затем добавить нарезанный лук и тертую морковь, обжарить до мягкости. 3)Добавить специи, соль и перец по вкусу, залить водой и тушить под крышкой около 30 минут.4) Пока мясо тушится, промыть рис и замочить его в холодной воде на 30-40 минут.5) Когда мясо будет почти готово, слить воду с риса, добавить его в казан и разровнять. 6) Если нужно, добавить еще воды, чтобы она была выше уровня риса на 1-2 см.7) Варить плов на медленном огне под крышкой до готовности риса, примерно 20-30 минут. [Картинка плова](https://otkrit-ka.ru/uploads/posts/2021-08/foto-i-kartinki-plova-4.jpg)", reply_markup=menu_keyboard)  # Можно менять текст


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()