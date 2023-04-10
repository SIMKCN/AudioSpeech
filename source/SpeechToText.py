#!/usr/bin/env python3


import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Progressbar
import speech_recognition as sr
from pathlib import Path
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import subprocess
import shutil


class Audio:
    global get_large_audio_transcription
    global r

    # create a speech recognition object
    r = sr.Recognizer()

    def get_large_audio_transcription(path):
        try:
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
            
            
                for i in chunks:
                    a += 1
                lengthi = 100/a
                folder_name = "audio-chunks"
            # create a directory to store the audio chunks
                if not os.path.isdir(folder_name):
                    os.mkdir(folder_name)
                
                    whole_text = ""
            # process each chunk
                    for i, audio_chunk in enumerate(chunks, start=1):
                    # export audio chunk and save it in
                    # the `folder_name` directory
                        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
                        audio_chunk.export(chunk_filename, format="wav")
                    # recognize the chunk
                        with sr.AudioFile(chunk_filename) as source:
                            audio_listened = r.record(source)
                        # try converting it to text
                            try: 
                                text = r.recognize_google(audio_listened, language="de-DE")
                            except sr.UnknownValueError as e:
                                print("Error:", str(e))
                            else:
                                text = f"{text.capitalize()}. "
                                print(chunk_filename, ":", text)
                                whole_text += text
                                nonsens = " "
                                datei = open("Transscript.csv", "a")
                                datei.write("\r\n" + chunk_filename + nonsens + text)
                                datei.close()
                        root3.update_idletasks()
                        pb['value'] += lengthi
        except TypeError:
            print("Error")


        root3 = tk.Tk()
        root3.title("Loading...")
        root3.geometry("200x100")
        """
        Splitting the large audio file into chunks
        and apply speech recognition on each of these chunks
        """
        # open the audio file using pydub
        
        pb = Progressbar(root3, orient=tk.HORIZONTAL, length=200, mode='determinate')
        startb = tk.Button(root3, text="Start", command=start)
        pb.grid(row=1, column=1)
        startb.grid(row=2, column=1)
        root3.mainloop()

    # return the text for all chunks detected
        
        
    
# def datei soll loadbar aufrufen welche am Ende des Aktion gestoppt werden soll
class UI:
    global root
    def datei():
        try:
            filename = askopenfilename()
            Audio(get_large_audio_transcription(filename))
        except TypeError:
            print("Error")
#test        

        
        #pb.start()
        
    def anleitung():
        root2 = tk.Tk()
        root2.geometry("700x600")
        root2.title("Anleitung")
        frame = tk.Frame(root2)
        frame.pack()
        
        sb = tk.Scrollbar(frame, orient="horizontal")
        sb.pack(fill="x")
        lb = tk.Listbox(frame, width=580, height=180, xscrollcommand=sb.set)
        lb.pack()

        lb.configure(xscrollcommand=sb.set)
        sb.config(command=lb.xview)
        
        lb.insert(0, "1.Anleitung")
        lb.insert(1, "2.Vorinformationen")
        lb.insert(2, "3.Achtung! Das Programm funktioniert nur mit .wav Datein!!!")
        lb.insert(3, "4.Sollten Sie andere Audio Formate nutzen könnte es zu Problemen kommen.")
        lb.insert(4, "")
        lb.insert(5, "6.Der Transcripter arbeitet nicht 100% perfekt und hat Probleme mit Dialekten.")
        lb.insert(6, "7.Er kann nicht zwischen Stimmen unterscheiden.")
        lb.insert(7, "8.Nach Nutzung sollte der Text nochmal korrigiert werden.")
        lb.insert(8, "9.Dazu werden während des transkribieren Audio Chunks erstellt, jeweils versähen mit dem Namen des Chunks.")
        lb.insert(9, "10.Diese Chunks werden im selben Ordner in der sich auch das Programm befindet gespeichert.")
        lb.insert(10, "11.Zusätzlich wird der Text in der Datei ""Transscript.txt"" gespeichert, welche auch im Ordner des Programms gespeichert wird.")
        lb.insert(11, "12.Begriffserklärung:")
        lb.insert(12, "Error:Eine Stelle wo keine Sprache erkannt worden ist. (Kann bei langem Atmen o.ä auftreten)")
        lb.insert(13, "-------------------------------------------------------------------")
        lb.insert(14, "1. Schritt /-/ Drücken Sie (Öffnen) und wählen sie die Wav Datei aus!")
        lb.insert(15, "2. Ein Fenster öffnet sich mit einem Ladebalken und dem Knopf 'Start'. Drücken sie diesen!")
        lb.insert(16, "Nun fängst das Programm an die Datei in Text um zuschreiben.")
        root2.mainloop()

    def close():
        try:
            root.quit()
        except TypeError:
            print("Error")
    root = tk.Tk()
    root.title("PYTranscriptor")
    root.geometry("200x100")
    anleitungb = tk.Button(root, text="Anleitung", command=anleitung, fg='#000000')
    close = tk.Button(root, text="Close", command=close, fg='#000000')
    l1 = tk.Label(root, text="Audio Datei:", fg='#000000')
    b1 = tk.Button(root, text="Öffnen", command=datei, fg='#000000')
    b1.grid(row=1, column=2, pady=10)
    l1.grid(row=1, column=1, padx=10)
    #pb.grid(row=3, column=1, padx=10, pady=10)
    close.grid(row=2, column=2)
    anleitungb.grid(row=2, column=1)
    root.mainloop()
