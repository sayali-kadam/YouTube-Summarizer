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
    return text  

def transcript_text(video_id):
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
                    result = SpeechRecognition()
                    os.remove(filename)
                    os.remove("transcript.wav")
    src_lang = translator.detect(result)
    translation = translator.translate(result, src=src_lang.lang, dest="en")
    translation = translation.text
    return translation

def summarized_text(transcript, video_id):
    # model = T5ForConditionalGeneration.from_pretrained("t5-base")
    # tokenizer = T5Tokenizer.from_pretrained("t5-base")
    # num_ite = int(len(transcript)/2000)
    # summarized_text = ""
    # for i in range(0, num_ite+1):
    #     st = i * 2000
    #     end = (i+1) * 2000
    #     inputs = tokenizer.encode("summarize: " + transcript[st:end], return_tensors="pt", max_length=2000, truncation=True)
    #     outputs = model.generate(inputs, max_length=500, min_length=100, length_penalty=2.0, num_beams=4, early_stopping=True)
    #     temp = tokenizer.decode(outputs[0])
    #     summarized_text += ' ' + temp

    # return summarized_text
    from sumy.parsers.html import HtmlParser
    from sumy.parsers.plaintext import PlaintextParser
    from sumy.nlp.tokenizers import Tokenizer
    from sumy.summarizers.lsa import LsaSummarizer as Summarizer
    from sumy.nlp.stemmers import Stemmer
    from sumy.utils import get_stop_words

    LANGUAGE = "english"
    SENTENCES_COUNT = 3
    import nltk;  
    nltk.download('punkt')

    parser = PlaintextParser.from_string(transcript, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    s = ""
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
      s += (str)(sentence)
    return s


@app.route('/api/summarize/<string:youtube_video>', methods=['GET','POST'])
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