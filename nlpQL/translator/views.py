from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from .forms import TextForm
from django.shortcuts import redirect
from django.conf import settings
import json

from .apps import TranslatorConfig


def read_json(file_url):
  with open(file_url, encoding='utf-8') as f:
    return json.load(f)

class Test(TemplateView):
    template_name = 'home.html'


def get_text(request):
    columns = 'null'
    sql_text = "nothing here"
    check = False

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        data = request.POST
        question = data['text_for_translation']
        file = request.FILES['file']
        fs=FileSystemStorage()
        file_name = fs.save(str(file), file)
        file_url = settings.MEDIA_ROOT / file_name #вот тут могут начаться проблемы при запуске с пк Матвея
        
        
        try:
            file_json = read_json(file_url)
            columns = [i["Name"] for i in file_json["Columns"]]
        except:
            check = True


        print(question)
        print(file_url)
        print(columns)

        form = TextForm(request.POST)

        if check:
            sql_text = "nothing here" #меняем эту переменную
        # check whether it's valid:
        else:
            sql_engine = TranslatorConfig.modelSQL
            sql_text = sql_engine.nl2sql(question, columns)
        if form.is_valid():
            render(request, 'translation.html', {'form': form, 'sql_text':sql_text, 'columns':columns, 'check':check})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TextForm()
    return render(request, 'translation.html', {'form': form, 'sql_text':sql_text, 'columns':columns, 'check':check})