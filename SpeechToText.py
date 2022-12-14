#!/usr/bin/env python3


from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Progressbar
import speech_recognition as sr
from pathlib import Path
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import subprocess
import logging
import shutil


class Audio:
    global get_large_audio_transcription
    global r
    logging.basicConfig(filename="SpeechToLog.log", filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)
    # create a speech recognition object
    r = sr.Recognizer()
    logging.info("create a speech recogniton object")
    def get_large_audio_transcription(path):
        def start():
            a = 0
            sound = AudioSegment.from_wav(path)
            # split audio sound where silence is 700 miliseconds or more and get chunks
            chunks = split_on_silence(sound,

                # adjust this per requirement
                silence_thresh = sound.dBFS-14,
                # keep the silence for 1 second, adjustable as well
                keep_silence=500,
            )
            logging.info("Splited Audio in Chunks")
            
            for i in chunks:
                a += 1
            lengthi = 100/a
            folder_name = "audio-chunks"
            # create a directory to store the audio chunks
            if not os.path.isdir(folder_name):
                os.mkdir(folder_name)
                logging.info("Created Folder for Chunks")
                whole_text = ""
            # process each chunk
                for i, audio_chunk in enumerate(chunks, start=1):
                    # export audio chunk and save it in
                    # the `folder_name` directory
                    chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
                    audio_chunk.export(chunk_filename, format="wav")
                    logging.info("Exported Chunk ")
                    # recognize the chunk
                    with sr.AudioFile(chunk_filename) as source:
                        audio_listened = r.record(source)
                        # try converting it to text
                        logging.info("Recognized the Chunk")
                        try: 
                            text = r.recognize_google(audio_listened, language="de-DE")
                            logging.info("Recognized it with Google")
                        except sr.UnknownValueError as e:
                            print("Error:", str(e))
                            logging.warning("The chunk could not be rewritten - Chunk is empty ")
                        else:
                            text = f"{text.capitalize()}. "
                            print(chunk_filename, ":", text)
                            logging.info("Printed chunk text")
                            whole_text += text
                            nonsens = " "
                            datei = open("Transscript.txt", "a")
                            datei.write("\r\n" + chunk_filename + nonsens + text)
                            datei.close()
                            logging.info("wrote Transcript")
                    root3.update_idletasks()
                    pb['value'] += lengthi
                    logging.info("Updated Progressbar")
            exit_code = subprocess.call("./Finish.sh")
            logging.info("Called ./Finish.sh")

        root3 = Tk()
        root3.title("Loading...")
        root3.geometry("200x100")
        """
        Splitting the large audio file into chunks
        and apply speech recognition on each of these chunks
        """
        # open the audio file using pydub
        
        pb = Progressbar(root3, orient=HORIZONTAL, length=200, mode='determinate')
        startb = Button(root3, text="Start", command=start)
        pb.grid(row=1, column=1)
        startb.grid(row=2, column=1)
        root3.mainloop()

    # return the text for all chunks detected
        
        
    
# def datei soll loadbar aufrufen welche am Ende des Aktion gestoppt werden soll
class UI:
    global root
    def datei():
        filename = askopenfilename()
        logging.info("asked for filename")
        Audio(get_large_audio_transcription(filename))
        
        

        
        #pb.start()
        
    def anleitung():
        logging.info("Opened anleitung()")
        root2 = Tk()
        root2.geometry("700x600")
        root2.title("Anleitung")
        frame = Frame(root2)
        frame.pack()
        
        sb = Scrollbar(frame, orient=HORIZONTAL)
        sb.pack(fill=X)
        lb = Listbox(frame, width=580, height=180, xscrollcommand=sb.set)
        lb.pack()

        lb.configure(xscrollcommand=sb.set)
        sb.config(command=lb.xview)
        
        lb.insert(0, "1.Anleitung")
        lb.insert(1, "2.Vorinformationen")
        lb.insert(2, "3.Achtung! Das Programm funktioniert nur mit .wav Datein!!!")
        lb.insert(3, "4.Sollten sie andere Audio Formate nutzen k??nnte es zu Problemen kommen.")
        lb.insert(4, "5.Das Programm ben??tigt eine Internetverbindung da es auf eine Datenbank zugreift.")
        lb.insert(5, "6.Der Transcripter arbeitet nicht 100% perfekt und hat Probleme mit Dialekten.")
        lb.insert(6, "7.Er kann nicht zwischen Stimmen unterscheiden.")
        lb.insert(7, "8.Nach Nutzung sollte der Text nochmal korrigiert werden.")
        lb.insert(8, "9.Dazu werden w??hrend des transkribieren Audio Chunks erstellt, jeweils vers??hen mit dem Namen des Chunks.")
        lb.insert(9, "10.Diese Chunks werden im selben Ordner in der sich auch das Programm befindet gespeichert.")
        lb.insert(10, "11.Zus??tzlich wird der Text in der Datei ""Transscript.txt"" gespeichert welche auch im Ordner des Programms gespeichert wird.")
        lb.insert(11, "12.Begriffserkl??rung:")
        lb.insert(12, "Error:Eine Stelle wo keine Sprache erkannt worden ist. (Kann bei langem Atmen o.?? auftreten)")
        lb.insert(13, "-------------------------------------------------------------------")
        lb.insert(14, "1. Schritt /-/ Dr??cken sie ??ffnen und w??hlen sie die Wav Datei aus!")
        lb.insert(15, "2. Ein Fenster ??ffnet sich mit einem Ladebalken und dem Knopf 'Start'. Dr??cken sie diesen!")
        lb.insert(16, "Nun f??ngst das Programm an die Datei in Text um zuschreiben.")
        root2.mainloop()

    def close():

        root.quit()

    logging.info("User logged in")

    root = Tk()
    root.title("PYTranscriptor")
    root.geometry("200x100")
    #global pb
    #pb = Progressbar(root, orient='horizontal', mode='indeterminate', length=280)

    anleitungb = Button(root, text="Anleitung", command=anleitung, fg='#b0d597')
    close = Button(root, text="Close", command=close, fg='#b0d597')
    l1 = Label(root, text="Audio Datei:", fg='#b0d597')
    b1 = Button(root, text="??ffnen", command=datei, fg='#b0d597')
    b1.grid(row=1, column=2, pady=10)
    l1.grid(row=1, column=1, padx=10)
    #pb.grid(row=3, column=1, padx=10, pady=10)
    close.grid(row=2, column=2)
    anleitungb.grid(row=2, column=1)
    root.mainloop()
