from fnmatch import translate
import telebot
from telebot import types
import json
from functools import partial
from transformers import FSMTForConditionalGeneration, FSMTTokenizer, AutoTokenizer, T5ForConditionalGeneration

from http.client import RemoteDisconnected

import traceback

import time

start = time.time()

CKPT_translator = "facebook/wmt19-ru-en"
tokenizer_translator = FSMTTokenizer.from_pretrained(CKPT_translator)
model_translator = FSMTForConditionalGeneration.from_pretrained(CKPT_translator)

CKPT = '../models/t5-base-finetuned-only-spider'
tokenizer = AutoTokenizer.from_pretrained(CKPT)
model = T5ForConditionalGeneration.from_pretrained(CKPT)

print(f"Loading models took {time.time() - start} seconds")


bot = telebot.TeleBot('')



def read_json_db(): #чтение json файлов
    with open("db.json", encoding='utf-8') as f:
        return json.load(f)

hello_text = "Привет, я бот для перевода естественного языка в SQL, созданный командой «DeviAⁱnts». \nДля перевода естественного языка в язык SQL используется модель t5-base.\nДля перевода запроса с русского на английский модель facebook/wmt19-ru-en.\nЧтобы начать работу переводчика - нажмите на кнопку «Начать». \nPS: Это альфа-версия"


def get_file(message):
    check = False
    # global columns
    if message.text == 'Стоп':
        bot.send_message(message.from_user.id, 'Чтение запросов завершилось')
    
    elif message.text:
        bot.send_message(message.from_user.id, 'Ошибка. Вы ввели текст, вам нужно отправить json-файл')
        bot.register_next_step_handler(message, get_file)
    
    else:
        file_name = message.document.file_name
        file_id = message.document.file_name
        file_id_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_id_info.file_path)
        
        print(file_name, file_id)
        with open("db.json", 'wb') as new_file:
            new_file.write(downloaded_file)
        
        try:
            file_json = read_json_db()
            columns = [i["Name"] for i in file_json["Columns"]]
        
        except:
            check = True
        
        if check:
            bot.send_message(message.from_user.id, "Ошибка. Вы загрузили неправильный файл")
            bot.send_message(message.from_user.id, "Загрузи другой файл")
            bot.register_next_step_handler(message, get_file)
        
        else:
            print(columns)
            # bot.send_message(message.from_user.id, columns)
            bot.send_message(message.from_user.id, "Ваша таблица: \n" + " | ".join(columns))
            bot.send_message(message.from_user.id, "Напиши запрос")
            bot.register_next_step_handler(message, partial(translate_message, columns))


def translate(text, max_length=128):
    # print(text)
    input_ids = tokenizer_translator.encode(text, return_tensors="pt", max_length=max_length,
                                            padding='max_length')
    outputs = model_translator.generate(input_ids, max_length=max_length)
    decoded = tokenizer_translator.decode(outputs[0], skip_special_tokens=True)
    # print(input_ids)
    return decoded


def make_question(question, columns):
    headers = "header table : " + " | ".join(columns)

    return "translate to SQL: " + question + "\n\n" + headers


def translate_to_sql(text):
    inputs = tokenizer(text, padding='longest', max_length=64, return_tensors='pt')
    input_ids = inputs.input_ids
    attention_mask = inputs.attention_mask
    output = model.generate(input_ids, attention_mask=attention_mask, max_length=64, )

    return tokenizer.decode(output[0], skip_special_tokens=True)


# def translate_message(columns, message):
def translate_message(*args, **kwargs):
    # print("hehe\n\n", args, '\n', kwargs, "\n\nhehe")
    
    columns, message = args
    if message.text != "Стоп":

        question = message.text

        print("\nUser asked:", question, '\n')

        # print(question)
        question = translate(question)
        # print(question)

        bot.send_message(message.from_user.id, f"Eng: {question}")

        question = make_question(question, columns)

        # print(question)

        answer = translate_to_sql(question)

        bot.send_message(message.from_user.id, f"SQL: {answer}")
        bot.register_next_step_handler(message, partial(translate_message, columns))

    else:
        bot.send_message(message.from_user.id, 'Чтение запросов завершилось')
        bot.send_message(message.from_user.id, "Отправь таблицу в виде json-файла")
        bot.register_next_step_handler(message, get_file)



@bot.message_handler(commands=['start'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    
    item1 = types.KeyboardButton("Начать")
    item2 = types.KeyboardButton("Стоп")
    item3 = types.KeyboardButton("Помощь")
    
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)

    bot.send_message(message.from_user.id, hello_text)
    bot.send_message(message.chat.id, "Выберите нужную опцию", reply_markup=markup)


@bot.message_handler(content_types=['text', 'document'])
def message_reply(message):
    if message.text=="Начать":
        bot.send_message(message.from_user.id, "Отправь таблицу в виде json-файла")
        bot.register_next_step_handler(message, get_file)

    elif message.text == "Помощь":
        bot.send_message(message.from_user.id, hello_text)




while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except RemoteDisconnected as E:
        print(traceback.format_exc())
        time.sleep(10)