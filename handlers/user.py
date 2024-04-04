import telebot
from telebot.handler_backends import StatesGroup, State

from funcs.datatime_funcs import get_welcome
from funcs.db import get_notes_from_db, save_notes, delete_notes_from_db
from init_bot import bot


class UserState(StatesGroup):
    state1 = State()


@bot.message_handler(commands=["start", "help"])
def start_help(message: telebot.types.Message):
    text = f"{get_welcome()} Я бот для заметок))\n\n" \
           f"Список команд:\n" \
           f"/create_notes - создать заметку\n" \
           f"/watch_notes - просмотреть заметки\n" \
           f"/delete_notes - удалить заметки\n" \
           f"/end - выйти из бота"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["create_notes"])
def create_notes_1(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Введите заметку в формате: \n"
                                      "Название: текст заметки")
    bot.register_next_step_handler(message, create_notes_2)


def create_notes_2(message: telebot.types.Message):
    data_text = message.text.split(": ")
    if len(data_text) == 1:
        bot.send_message(message.chat.id, "Не было достаточно данных для добавления.Попробуйте еще раз.")
    elif len(data_text) == 2:
        name = data_text[0]
        notes_text = data_text[1]
        bot.send_message(message.chat.id, f"Название заметки: {name}\n"
                                          f"Текст заметки: : {notes_text}")
        save_notes(name=name, notes_text=notes_text)
        bot.send_message(message.chat.id, "Данные вставлены")
    else:
        bot.send_message(message.chat.id, "Неверный формат. Попробуйте еще раз.")


@bot.message_handler(commands=["watch_notes"])
def watch_notes(message: telebot.types.Message):
    notes = get_notes_from_db()
    if not notes:
        bot.send_message(message.chat.id, "Заметок нет")
    else:
        for idx, note in enumerate(notes):
            bot.send_message(message.chat.id, f"Заметка {idx + 1}:\nНазвание: {note[1]}\nСодержание: {note[2]}", parse_mode="HTML")


@bot.message_handler(commands=["delete_notes"])
def delete_notes(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Введите название заметки, которую хотите удалить:")
    bot.register_next_step_handler(message, process_delete_notes)


def process_delete_notes(message: telebot.types.Message):
    note_to_delete = message.text.strip()

    notes = get_notes_from_db()
    if not notes:
        bot.send_message(message.chat.id, "Нет заметок для удаления")
        return

    if note_to_delete not in [note[1] for note in notes]:
        bot.send_message(message.chat.id, f"Заметки с названием '{note_to_delete}' не найдено")
        return

    delete_notes_from_db(note_to_delete)
    bot.send_message(message.chat.id, f"Заметка '{note_to_delete}' успешно удалена")


@bot.message_handler(commands=["end"], state=UserState.state1)
def end(message: telebot.types.Message):
    markup = telebot.types.ReplyKeyboardRemove()
    text = f"Спасибо! Пока)"
    bot.send_message(message.chat.id, text, reply_markup=markup)