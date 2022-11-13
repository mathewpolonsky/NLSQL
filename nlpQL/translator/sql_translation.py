from transformers import FSMTForConditionalGeneration, FSMTTokenizer, AutoTokenizer, T5ForConditionalGeneration

import time

start = time.time()

CKPT_translator = "facebook/wmt19-ru-en"
tokenizer_translator = FSMTTokenizer.from_pretrained(CKPT_translator)
model_translator = FSMTForConditionalGeneration.from_pretrained(CKPT_translator)

CKPT = '../models/t5-base-finetuned-only-spider'
tokenizer = AutoTokenizer.from_pretrained(CKPT)
model = T5ForConditionalGeneration.from_pretrained(CKPT)

print(f"Loading models took {time.time() - start} seconds")


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


def nl2sql(question, columns):
    # print(question)
    question = translate(question)
    # print(question)

    print(f"Eng: {question}")

    question = make_question(question, columns)

    # print(question)

    answer = translate_to_sql(question)   

    return answer