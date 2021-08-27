from google.cloud import texttospeech
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Instantiates a client
client = texttospeech.TextToSpeechClient()

@csrf_exempt
def tts(request):
    # Set the text input to be synthesized
    print(request.GET)
    text=request.GET.get('text')
    print(type(text))
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
    name="en-IN-Wavenet-C",language_code="en-IN", ssml_gender=texttospeech.SsmlVoiceGender.MALE
    )
    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    # The response's audio_content is binary.
    with open("gtts.mp3", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')

    return HttpResponse(' hey')    