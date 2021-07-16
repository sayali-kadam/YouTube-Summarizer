from flask import Flask, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from googletrans import Translator
from transformers import T5ForConditionalGeneration, T5Tokenizer
import speech_recognition as sr
from pydub import AudioSegment
from youtube_dl import YoutubeDL
import os

app = Flask(__name__)
CORS(app)
translator = Translator()
audio_downloader = YoutubeDL({'format':'m4a'})
formats_to_convert = ['.m4a']

def SpeechRecognition():
    r = sr.Recognizer()
    with sr.AudioFile('transcript.wav') as source:
        audio = r.record(source)
        text = r.recognize_google(audio)
        print('Working....')
        print(text)
    return text  

def transcript_text(video_id):
    print(video_id)
    result = ""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        for i in transcript:
            result += ' ' + i['text']
    except Exception as e:
        URL = "https://www.youtube.com/watch?v="+video_id
        audio_downloader.extract_info(URL)
        for (dirpath, dirnames, filenames) in os.walk("D:/Projects/YouTube-Summarizer/", topdown=True):
            for filename in filenames:
                if filename.endswith(tuple(formats_to_convert)):
                    sound = AudioSegment.from_file(filename, "m4a").set_frame_rate(441)
                    sound.export("transcript.wav", format="wav", bitrate='32k')
                    print(filename)
                    result = SpeechRecognition()
                    os.remove(filename)
                    os.remove("transcript.wav")
    translation = translator.translate(result, dest="en")
    translation = translation.text
    print(translation)
    print(len(translation))
    return translation

def summarized_text(transcript, video_id):
    model = T5ForConditionalGeneration.from_pretrained("t5-base")
    tokenizer = T5Tokenizer.from_pretrained("t5-base")
    num_ite = int(len(transcript)/2000)
    summarized_text = ""
    for i in range(0, num_ite+1):
        st = i * 2000
        end = (i+1) * 2000
        inputs = tokenizer.encode("summarize: " + transcript[st:end], return_tensors="pt", max_length=2000, truncation=True)
        outputs = model.generate(inputs, max_length=500, min_length=100, length_penalty=2.0, num_beams=4, early_stopping=True)
        temp = tokenizer.decode(outputs[0])
        summarized_text += ' ' + temp

    print(len(summarized_text))
    print(summarized_text)
    return summarized_text


@app.route('/api/summarize/<string:youtube_video>', methods=['GET'])
def YouTube_Video(youtube_video):
    transcript = transcript_text(youtube_video)
    summary = summarized_text(transcript, youtube_video)
    res = {
        "Video ID": youtube_video,
        "Transcript": transcript,
        "Summary": summary
    }
    return jsonify(res)

if __name__ == "__main__":
    app.run(debug=True)