from youtube_transcript_api import YouTubeTranscriptApi


def get_transcript(url):
    video_id = url[::-1][:11][::-1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])

    full_script = ""
    for j in transcript:
        full_script += j["text"] + " "
    return full_script
