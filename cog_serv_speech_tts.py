# pip install azure-cognitiveservices-speech
# https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-text-to-speech
# list of voices: https://learn.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.synthesisvoicesresult?view=azure-python
# list of voices: https://stackoverflow.com/questions/54858307/how-to-get-a-list-of-available-voices-for-azure-text-to-speech
# list of voices (REST): https://learn.microsoft.com/en-us/azure/ai-services/speech-service/rest-text-to-speech?tabs=streaming#get-a-list-of-voices
# expects SPEECH_KEY
# set|setx SPEECH_KEY the_resource_key from Keys and Endpoint section
import os
import azure.cognitiveservices.speech as speechsdk


def main():
    # NOTE: it seems that the internal construction of the endpoint is broken, the endpoint given in Azure portal is wrong and you have to derive the the endpoint from the REST API docs
    region = "northeurope"
    guessed_endpoint = "https://" + region + ".api.cognitive.microsoft.com/sts/v1.0/issuetoken"

    # ValueError: cannot construct SpeechConfig with both region and endpoint or host information
    # ValueError: either subscription key or authorization token must be given along with a region
    # https://learn.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.speech?view=azure-python
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), endpoint=guessed_endpoint)

    # let the voice speak directly
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    # save to file: audio_config = speechsdk.audio.AudioOutputConfig(filename="path/to/write/file.wav")

    # https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts
    speech_config.speech_synthesis_voice_name='de-DE-ElkeNeural'

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    TEXT = input("Enter the text to be speech-synthesised: ")
    speech_synthesis_result = speech_synthesizer.speak_text_async(TEXT).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(TEXT))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

if __name__ == "__main__":
    main()
    print("Script ran standalone and was not imported.")
