from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
from transformers import T5ForConditionalGeneration, T5Tokenizer, pipeline
import json
from flask import Flask, jsonify, request, abort, Response  
import flask as f
from http import HTTPStatus

app = Flask(__name__)

@app.route('/')
def mainpage():
    resp = f.Response("Hello there")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization, X-CSRF-Token'
    return resp

def Transcript_To_Text(transcript):
    formatter = JSONFormatter()
    json_formatted = formatter.format_transcript(transcript)
    with open('transcript_file.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json_formatted)   
    speech_text = json.loads(json_formatted)
    speech_text_string = ""
    for i in speech_text: 
        speech_text_string += i['text']
        speech_text_string += " "
    return speech_text_string

def Text_Summary_Small_Tokenizer(script):
    model = T5ForConditionalGeneration.from_pretrained("t5-base")
    tokenizer = T5Tokenizer.from_pretrained("t5-base")
    inputs = tokenizer.encode("summarize: " + script, return_tensors="pt", max_length=512,truncation=True)
    outputs = model.generate(  
    inputs, 
    max_length=150,
    min_length=50,
    length_penalty=2.0, 
    num_beams=4, 
    early_stopping=True)
    return tokenizer.decode(outputs[0])

def Text_Summary_Small(script):
    summarizer = pipeline('summarization', model="t5-base", truncation=True)
    num_iters = int(len(script)/4000)
    summarized_text = []
    for i in range(0, num_iters + 1):
        start = 0
        start = i * 4000
        end = (i + 1) * 4000
        out = summarizer(script[start:end])
        out = out[0]  
        out = out['summary_text'] 
        summarized_text.append(out)
    return " ".join(summarized_text)

def Text_Summary_Medium(script):
    summarizer = pipeline('summarization', model="t5-base", truncation=True)
    num_iters = int(len(script)/2000)
    summarized_text = []
    for i in range(0, num_iters + 1):
        start = 0
        start = i * 2000
        end = (i + 1) * 2000
        out = summarizer(script[start:end])
        out = out[0]  
        out = out['summary_text'] 
        summarized_text.append(out)
    return " ".join(summarized_text)
    
def Text_Summary_Large(script):
    summarizer = pipeline('summarization',model="t5-base", truncation=True)
    num_iters = int(len(script)/1000)
    summarized_text = []
    for i in range(0, num_iters + 1):
        start = 0
        start = i * 1000
        end = (i + 1) * 1000
        out = summarizer(script[start:end])
        out = out[0]  
        out = out['summary_text'] 
        summarized_text.append(out)
    return " ".join(summarized_text)

@app.errorhandler(404)
def handle_exception(e):
    return f'Bad Request! Error: {HTTPStatus(e.code)}, {HTTPStatus(e.code).phrase}'
    
@app.route('/api/summarize1', methods=['GET'])
def api1():
    url_yt = request.args.get('youtube_url', None)
    if url_yt==None:
        abort(404)
    x = url_yt.split("v=")
    v_id = str(x[1])
    transcript = YouTubeTranscriptApi.get_transcript(v_id)
    script = Transcript_To_Text(transcript)
    resp = f.Response(Text_Summary_Medium(script))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization, X-CSRF-Token'
    return resp

@app.route('/api/summarize2', methods=['GET'])
def api2():
    url_yt = request.args.get('youtube_url', None)
    if url_yt==None:
        abort(404)
    x = url_yt.split("v=")
    v_id = str(x[1])
    transcript = YouTubeTranscriptApi.get_transcript(v_id)
    script = Transcript_To_Text(transcript)
    resp = f.Response(Text_Summary_Large(script))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization, X-CSRF-Token'
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
