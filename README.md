# YouTube-Summarizer
It is helpful for generate the summary of YouTube videos.

### Features:
1. Handle the videos with as well as without subtitles
2. Also it can create summary in english from any language of videos
3. create complete new sentence with importance of words

### Project stages:
![s1](https://user-images.githubusercontent.com/62012906/138927706-fe70fb0b-7f27-4a34-8c74-85a446e713a9.png)

### Implementation details:
#### Server side:
It ia a simple flask app, which has a API/api/summarize?youtube_video='url' which can be used to get the summary of desired youtube video by simple making a GET HTTP request.
1. Technology used: Python flask framework 
2. First create a transcript of the video
    a. With subtitles: Simply use YouTubeTranscriptApi library of python and create transcript
    b. Without subtitles:
          i. Convert video to .wav file format (Audio format)
          ii. By using speech recognition, processes on .wav file and convert it into text form
3. Now transcript is ready and time to make summary of it
4. For summarization Huggingface transformers is available in python
5. By using pipeline API and T5 transformer model in Python with Huggingface transformers and Pytorch library we can summarize a long text into small summary.
6. There are two different approaches that are widely used for text summarization:
        a. Extractive Summarization: This is where the model identifies the important sentences and phrases from the original text and only outputs those.
        b. Abstractive Summarization: The model produces a completely different text that is shorter than the original, it generates new sentences in a new form, just like humans do. In this tutorial, we will use transformers for this approach.
7. According to the above methods flask API can create a summary for the video

#### Client side:
It is a chrome extension which will render the summary of the youtube video by making use of the above API. Just click on summarize button and it will show the summary of the youtube video.
1. Working of chrome extension:
![s2](https://user-images.githubusercontent.com/62012906/138928025-48faf828-0f22-4322-be57-4826c694644b.png)
2. On clicking the summarize button on the popup, if the url is of form https://www.youtube.com/watch?v=* the popup js makes a GET request to our Server API.
3. A pop up will come on the screeen after calling the API. 
4. For that after the text is received, it is passed to the content js which then changes the content and show the pop up.
5. It can be used by loading unpacked from chrome://extensions/.

### Result of the project
