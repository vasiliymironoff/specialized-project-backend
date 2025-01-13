from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import NewsData
from datetime import datetime
from django.conf import settings
import json

import torch                
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import requests 
import pickle
from .lstm import LSTM

# load home.html
@csrf_protect
@csrf_exempt
def home(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text', '')
        print(text)

        # summarization
        tokenizer = AutoTokenizer.from_pretrained('t5-base')                        
        model = AutoModelForSeq2SeqLM.from_pretrained('t5-base', return_dict=True)                   
        inputs = tokenizer.encode("summarize: " + text,                  
            return_tensors='pt',              
            max_length=512,             
            truncation=True)                   
        
        summary_ids = model.generate(inputs, max_length=400, min_length=80, length_penalty=5., num_beams=2)                   
        description = tokenizer.decode(summary_ids[0]).replace('<pad> ', '').replace('</s>', '')                
        print(description)
        # классифицируем
        model_id = "sentence-transformers/all-MiniLM-L6-v2"
        hf_token = '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'

        api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
        headers = {"Authorization": f"Bearer {hf_token}"}

        def query(texts):
            response = requests.post(api_url, headers=headers, json={"inputs": texts})
            return response.json()
       
        with open('model_lstm.pkl', 'rb') as dump_in:
            model_lstm = pickle.load(dump_in)
        inp = torch.tensor(query(description))
        print('get embedding')
        inp = inp.unsqueeze(0).unsqueeze(0)
        out = model_lstm(inp)
        print('model prepared')
        result = torch.argmax(out, 1).item()
        index_to_label = {0: 'U.S. NEWS', 1: 'COMEDY', 2: 'PARENTING', 3: 'WORLD NEWS', 4: 'CULTURE & ARTS', 5: 'TECH', 6: 'SPORTS', 7: 'ENTERTAINMENT', 8: 'POLITICS', 9: 'WEIRD NEWS', 10: 'ENVIRONMENT', 11: 'EDUCATION', 12: 'CRIME', 13: 'SCIENCE', 14: 'WELLNESS', 15: 'BUSINESS', 16: 'STYLE & BEAUTY', 17: 'FOOD & DRINK', 18: 'MEDIA', 19: 'QUEER VOICES', 20: 'HOME & LIVING', 21: 'WOMEN', 22: 'BLACK VOICES', 23: 'TRAVEL', 24: 'MONEY', 25: 'RELIGION', 26: 'LATINO VOICES', 27: 'IMPACT', 28: 'WEDDINGS', 29: 'COLLEGE', 30: 'PARENTS', 31: 'ARTS & CULTURE', 32: 'STYLE', 33: 'GREEN', 34: 'TASTE', 35: 'HEALTHY LIVING'}
        category= index_to_label[result]
        print(category)

        # text-to-audio
        #pipe = pipeline("text-to-speech", model="suno/bark-small")
        #output = pipe(f'{category} - {description}')
        #print(output)
        #audio_data = output["audio"]
        #sampling_rate = output["sampling_rate"]

        #path_audio = f'./{NewsData.objects.count()}.wav'
        #with open(path_audio, "wb") as f:
        #   f.write(audio_data)

        # Сохраняем в базу данных
        news = NewsData(
            text=text,
            description=description,
            category=category,
            path_audio=''
        )                
                        
        # Коммитим
        news.save()
        return JsonResponse({
            'success': True, 
            'description': description,
            'category': category,
        })

    return render(request, 'home.html')


# load report.html
def report(request):
    # take data from database
    news_data = NewsData.objects.all()
    return render(request, 'report.html', {'news_data': news_data})
