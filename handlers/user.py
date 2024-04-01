import telebot

from funcs.datatime_funcs import get_welcome
from funcs.db import get_notes_from_db, save_notes
from init_bot import bot


@bot.message_handler(commands=["start", "help"])
def start_help(message: telebot.types.Message):
    text = f"{get_welcome()} Я бот для заметок))\n\n" \
           f"Список команд:\n" \
           f"/create_notes - создать заметку\n" \
           f"/watch_notes - просмотреть заметки\n" \
           f"/delete_notes - удалить заметки"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["create_notes"])
def create_notes(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Введите заметку в формате: \n"
                                      "Название: текст заметки")
    data_text = message.text.split(": ")
    if len(data_text) == 1:
        bot.send_message(message.chat.id, "Не было достаточно данных для добавления.")
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
            bot.send_message(message.chat.id, f"Заметка {idx + 1}:\nНазвание: {note.name}\nСодержание: {note.content}")


@bot.message_handler(commands=["delete_notes"])
def delete_notes(message: telebot.types.Message):
    notes = get_notes_from_db()
    if not notes:
        bot.send_message(message.chat.id, "Нет заметок для удаления")
        return

    data_text = message.text.split("--")
    if len(data_text) != 2:
        bot.send_message(message.chat.id, "Неверный формат команды. Используйте /delete_note Название_или_Автор")
        return

    keyword = data_text[1].strip()
    deleted = False
    for note in notes:
        if keyword.lower() in [note.name.lower(), note.author.lower()]:
            notes.remove(note)
            bot.send_message(message.chat.id,
                             f"Заметка удалена:\nНазвание: {note.name}\nАвтор: {note.author}\nСодержание: {note.content}")
            deleted = True
            break

    if not deleted:
        bot.send_message(message.chat.id, f"Заметка с названием или автором '{keyword}' не найдена")

