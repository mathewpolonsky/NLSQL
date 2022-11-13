from django.apps import AppConfig

from transformers import FSMTForConditionalGeneration, FSMTTokenizer, AutoTokenizer, T5ForConditionalGeneration
import time


class ModelSQL:
    def __init__(self):
        start = time.time()

        CKPT_translator = "facebook/wmt19-ru-en"
        self.tokenizer_translator = FSMTTokenizer.from_pretrained(CKPT_translator)
        self.model_translator = FSMTForConditionalGeneration.from_pretrained(CKPT_translator)

        CKPT = '../models/t5-base-finetuned-only-spider'
        self.tokenizer = AutoTokenizer.from_pretrained(CKPT)
        self.model = T5ForConditionalGeneration.from_pretrained(CKPT)

        print(f"Loading models took {time.time() - start} seconds")

    def translate(self, text, max_length=128):
        # print(text)
        input_ids = self.tokenizer_translator.encode(text, return_tensors="pt", max_length=max_length,
                                                padding='max_length')
        outputs = self.model_translator.generate(input_ids, max_length=max_length)
        decoded = self.tokenizer_translator.decode(outputs[0], skip_special_tokens=True)
        # print(input_ids)
        return decoded


    def make_question(self, question, columns):
        headers = "header table : " + " | ".join(columns)

        return "translate to SQL: " + question + "\n\n" + headers


    def translate_to_sql(self, text):
        inputs = self.tokenizer(text, padding='longest', max_length=64, return_tensors='pt')
        input_ids = inputs.input_ids
        attention_mask = inputs.attention_mask
        output = self.model.generate(input_ids, attention_mask=attention_mask, max_length=64, )

        return self.tokenizer.decode(output[0], skip_special_tokens=True)


    def nl2sql(self, question, columns):
        # print(question)
        question = self.translate(question)
        # print(question)

        print(f"Eng: {question}")

        question = self.make_question(question, columns)

        # print(question)

        answer = self.translate_to_sql(question)   

        return answer


class TranslatorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'translator'

    modelSQL = ModelSQL()


