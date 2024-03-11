##### DOES NOT YET WORK FOR REASONS BEYOND MY COMPREHENSION #####
# pip install azure-cognitiveservices-speech
# https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-text-to-speech
# expects SPEECH_KEY
# set|setx SPEECH_KEY the_resource_key from Keys and Endpoint section
import os
import azure.cognitiveservices.speech as speechsdk


def main():

    # ValueError: cannot construct SpeechConfig with both region and endpoint or host information
    # ValueError: either subscription key or authorization token must be given along with a region
    # https://learn.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.speech?view=azure-python
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), endpoint="https://northeurope.api.cognitive.microsoft.com/")

    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    # https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts
    speech_config.speech_synthesis_voice_name='en-US-JennyNeural'

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
