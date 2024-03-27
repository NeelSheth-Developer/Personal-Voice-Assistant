##############-------Natasha Romanoff------------------------------

import google.generativeai as genai
from time import time as t
from GoogleNews import GoogleNews
from rich import print
from glob import glob
import concurrent.futures
from random import randint
import face_recognition
import smtplib
import cv2
import requests
from PIL import Image
from os import system
import google.generativeai as genai
import pyttsx3
import speech_recognition as sr
import datetime
import eel
import sys
import webbrowser
import subprocess
import keyboard
import psutil 
import time
import pyautogui
import os
import random
import pywhatkit as kit
import pyperclip
from pytube import YouTube

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Global variable to keep track of the currently displayed image index
current_image_index = 0
# Initialize the Eel application
def link():
    eel.init('web')
    # Start the Eel application
    eel.init(r'C:\Users\neelsheth\Downloads\scientific_prog')
    eel.start('index.html')         
def lock():
     # Load known face images and encodings
    known_faces = []
    known_encodings = []

    for i in range(1, 11):
        known_image_path = f"C:\\Users\\neelsheth\\Downloads\\personal_ai\\gui\\facelock\\sample_folder\\captured_image_{i}.jpg"
        known_image = face_recognition.load_image_file(known_image_path)
        face_encodings = face_recognition.face_encodings(known_image)
        
        if len(face_encodings) > 0:
            known_face_encoding = face_encodings[0]
            known_faces.append(known_image)
            known_encodings.append(known_face_encoding)
        else:
            print(f"No face detected in {known_image_path}. Skipping.")

    # Initialize video capture
    video_capture = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        # Find all face locations and encodings in the current frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        if len(face_encodings) > 0:
            for face_encoding in face_encodings:
                # Compare each face encoding found in the frame with the known face encodings
                matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
                
                if True in matches:
                    # If a match is found, unlock
                    print("Face recognized. Access granted!")
                    speak("Access granted!")
                    # Implement your unlocking mechanism here
                    # Release video capture and close all windows
                    video_capture.release()
                    cv2.destroyAllWindows()
                    return("unlock")
                else:
                    print("Face not matched")
                    speak("Access Denied!")

        # Display the resulting image
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()
    return "lock"

# Function to speak text
def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("Error occurred during speech synthesis:", e)

# Function to recognize speech
def speechrecog():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    try:
        print("Recognizing....")
        query = recognizer.recognize_google(audio, language="en")
        print("User said:", query)
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        speak("Could not request results; {0}".format(e))
        return ""
    
 # Function to wish the user
def wish():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning !")
    elif 12 <= hour < 18:
        speak("Good Afternoon !")
    else:
        speak("Good Evening !")
        
#function to generate image
def generate_image(prompt: str):
    global current_image_index
    speak("It takes some time to generate.....")
    # Run the Bing Image Creator tool to generate an image
    #subprocess.run(['python', '-m', 'BingImageCreator', '--prompt', gen_img, '-U','1AtMs-hZdRztHj_tkOvidBqCPPSZKKz5j6UjRwO_WyLc7qA3P93fsZz3Ci6uR_Y0OUKHHr60uaj_mh5-VGKcQ8uifrnH6ZN-Izz7EO9Rx3jCHkRfA4tduVvQYYv8adnKVSmV6_oBmn6kdCSLw9vvujWRfnMXTsmRyLfbA6l7opltx8f-8xNxn63S-cUw8yrJt2CeiGiLSpvZz8LJEnuzPXw'])
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.content

    def save_image(image_bytes, filename):
        with open(filename, 'wb') as f:
            f.write(image_bytes)

    def process_image(index, prompt, seed):
        image_bytes = query({"inputs": f"{prompt}={seed}"})
        filename = f"output/image_prompt_{prompt}_seed_{seed}_index_{index}.jpg"
        save_image(image_bytes, filename)
        print(f"Image {index} saved with seed {seed} and prompt '{prompt}'")

    def generate_images_and_save(num_images, prompt):
        os.makedirs("output", exist_ok=True)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            seed_list = [randint(0, 100000) for _ in range(num_images)]
            futures = [executor.submit(process_image, i, prompt, seed) for i, seed in enumerate(seed_list)]
            for future in concurrent.futures.as_completed(futures):
                future.result()

    generate_images_and_save(4, prompt)
    output_folder = 'output'
    image_files = glob(os.path.join(output_folder, '*'))

    if image_files:
        # Sort image files by modification time to get the most recent ones
        sorted_images = sorted(image_files, key=os.path.getmtime, reverse=True)

        # Display the first four non-corrupted images
        displayed_images = 0
        for image_file in sorted_images:
            try:
                with Image.open(image_file) as img:
                    img.show()
                    displayed_images += 1
                    if displayed_images >= 3:
                        break
            except (OSError, IOError):
                print(f"Skipping corrupted image: {image_file}")

        if displayed_images == 0:
                print("No non-corrupted images found in the output folder.")
    else:
           print("No images found in the output folder.")
           speak("No images found in the output folder.")
                
    return f"Image of {prompt} generated successfully"
          
#news:
def get_news_by_category(category):
    # Create a GoogleNews object
    gn = GoogleNews()

    # Set the language and region (optional)
    gn.set_lang('en')
    gn.set_period('1d')  # Set the period to 1 day for today's news

    # Search for news articles related to the category
    gn.search(category)

    # Get the top news results
    top_news = gn.results()
    print(f"Top {category.capitalize()} News:")
    for i, news in enumerate(top_news, start=1):
        a=(f"{i}. {news['title']}")
        print(a)
        speak(a)
        
# Function to write and save a message in Notepad
def write_and_save_message(message):
    try:
        with open("temp_message.txt", "w") as file:
            file.write(message)
        speak("Message written in Notepad. Do you want to save it?")
        response = speechrecog()
        time.sleep(1)
        if "yes" in response:
            speak("Please specify the filename.")
            filename = speechrecog()  # Ask for the filename using speech recognition
            if filename:
                filename = filename.strip().replace(" ", "_")  # Clean the filename
                filename += ".txt"  # Add file extension
                os.rename("temp_message.txt", filename)  # Rename the file with the specified filename
                speak(f"Message saved as {filename}")
                time.sleep(1)
                return(f"Message saved as {filename}")
    except Exception as e:
        print("Error occurred while writing or saving the message:", e)
        speak("Sorry, I encountered an error while writing or saving the message.")

        
# Function to play random music on YouTube
def play(query):
    query_without_spaces = query.replace(" ", "")  # Remove spaces from the query
    print(query)
    kit.playonyt(query_without_spaces)
    speak(f"Playing {query_without_spaces} on YouTube")
# Function to handle window actions with speech
def handle_window_action(action):
    try:
        if action == "minimize":
            pyautogui.hotkey('win', 'm')  # Minimize active window
            speak("Window minimized") #minimized the window
            time.sleep(1)
        elif action == "maximize":
            pyautogui.hotkey('alt', 'tab')    # Maximize active window
            speak("Window maximized")
            time.sleep(1)
        elif action == "up":
            pyautogui.hotkey('win', 'up')  # for shifting tab to up
            speak("up tab")
            time.sleep(1)
        elif action == "down":
            pyautogui.hotkey('win','down')  # for shifting tab to down
            speak("down tab")
            time.sleep(1)
        elif action == "alt_tab":
            pyautogui.hotkey('alt', 'tab')  # alt tab
            speak("changing tab")
            time.sleep(1) 
        elif action == "next":
            pyautogui.hotkey('ctrl', 'tab')  # ctrl tab
            speak("changing browser tab")
            time.sleep(1)   
        elif action=="close":
            pyautogui.hotkey("ctrl","w") #ctrl w
            speak("Closing the tab")
            time.sleep(1) 
    except Exception as e:
        print("Error occurred during window action:", e)
#function to take photo

def capture_single_photo(output_filename):
    # Open the default camera (usually webcam)
    cap = cv2.VideoCapture(0)

    # Capture a single photo
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture photo")
        return

    # Save the captured frame as an image
    cv2.imwrite(output_filename, frame)
    speak(f"Photo is captured and save as {output_filename}")
    # Release the camera and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

# Function to download YouTube video
def download_video():
    try:
        speak("Downloading initiated")
        time.sleep(1)
        # Hotkey to copy the current URL
        keyboard.press_and_release('ctrl + l')
        time.sleep(0.5)
        keyboard.press_and_release('ctrl + c')  # Copy the URL
        time.sleep(0.5)

        url= pyperclip.paste()  # Get the copied URL from the clipboard
        print("Natasha: Please focus on the browser where YouTube is open.")
        print("Natasha: Current URL:", url)
        
        video = YouTube(url)
        stream = video.streams.get_highest_resolution()
        time.sleep(1)
        if stream:
            stream.download()
            print("Downloaded successfully!")
            speak("Downloaded successfully!")
            time.sleep(1)
        else:
            print("No suitable streams found for download.")
            speak("No suitable streams found for download.")
            time.sleep(1)
    except Exception as e:
        print("Error occurred during download:", e)
        speak("Sorry, I encountered an error during the download.")   
# Function to download a song from YouTube
def download_song_from_youtube():
    try:
        speak("Downloading initiated")
        time.sleep(1)
        
        # Hotkey to copy the current URL
        keyboard.press_and_release('ctrl + l')
        time.sleep(0.5)
        keyboard.press_and_release('ctrl + c')  # Copy the URL
        time.sleep(0.5)

        url = pyperclip.paste()  # Get the copied URL from the clipboard
        print("Natasha: Please focus on the browser where YouTube is open.")
        print("Natasha Romanoff: Current URL:", url)
        
        video = YouTube(url)
        audio_stream = video.streams.filter(only_audio=True).first()
        if audio_stream:
            # Create a folder named "my_music" if it doesn't exist
            folder_name = "my_music"
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            
            # Download the audio file and save it in the "my_music" folder
            file_path = os.path.join(folder_name, f"{video.title}.mp3")
            audio_stream.download(filename=file_path)
            
            print("Audio downloaded successfully!")
            speak("Audio downloaded successfully and saved in the 'my_music' folder.")
            time.sleep(1)
            return True
        else:
            print("No audio stream available for this video.")
            speak("Sorry, no audio stream available for this video.")
            time.sleep(1)
            return False
    except Exception as e:
        print("Error occurred during song download:", e)
        speak("Sorry, I encountered an error while downloading the song.")
        time.sleep(1)        
#----------------------------------------------------------------------------   
    #gemini
generation_config = {
 "temperature": 0.7,
 "top_p": 1,
 "top_k": 1,
 "max_output_tokens": 300,
}

safety_settings = [
 {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_ONLY_HIGH"
 },
 {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_ONLY_HIGH"
 },
 {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_ONLY_HIGH"
 },
 {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_ONLY_HIGH"
 },
]

model = genai.GenerativeModel(
 model_name="gemini-pro",
 generation_config=generation_config,
 safety_settings=safety_settings)

genai.configure(api_key="AIzaSyAXvR-ZT0cNgwcXdE5SXKfipn7vz0zvu_Y")

messages = [
    {
        "parts": [
            {
                "text": "You are a Powerful AI Assistant Named Natasha Romanoff. Hello, How are you?"
            }
        ],
        "role": "user"
    },
    {
        "parts": [
            {
                "text": "Hello, I am doing well. How can I help you?"
            }
        ],
        "role": "model"
    },
    
   
]

def Gemini(prompt):
    global messages
    messages.append({
    "parts": [
      {
        "text": prompt + "***reply in less tokens***"
      }
    ],
    "role": "user"
    })
    
    response = model.generate_content(messages)
    
    messages.append({
    "parts": [
      {
        "text": response.text
      }
    ],
    "role": "model"})
    print(messages)
    return response.text
# Function to take a screenshot
def take_screenshot():
    try:
        speak("Taking a screenshot. Please specify the filename.")
        filename = speechrecog()  # Ask for the filename using speech recognition
        time.sleep(1)
        if filename:
            filename = filename.strip().replace(" ", "_")  # Clean the filename
            filename += ".png"  # Add file extension
            screenshot = pyautogui.screenshot()  # Capture the screenshot
            screenshot.save(filename)  # Save the screenshot with the specified filename
            speak(f"Screenshot saved as {filename}")
            time.sleep(1)
            return (f"Screenshot saved as {filename}")
    except Exception as e:
        print("Error occurred while taking the screenshot:", e)
        speak("Sorry, I encountered an error while taking the screenshot.")  
def close_media_players():
    speak("Closing media player.....")
    time.sleep(1)
    media_player_processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        if "exe" in proc.info['name'].lower() and "media" in proc.info['name'].lower():
            media_player_processes.append(proc)
    
    if not media_player_processes:
        print("No media player processes found.")
        return

    for proc in media_player_processes:
        proc.terminate()
        print(f"Closed {proc.info['name']}") 
        
@eel.expose
def terminate():
        speak("Terminating the program in 3 seconds")
        for i in range(1,4):
            speak(i)
        speak("Exit")
        sys.exit(0)     
#function to send email
def email_sender(emailer,message_email):
    emailer = emailer.replace(" ", "").lower()
    sender_email = "neeldemo2050@gmail.com"
    receiver_email = emailer
    subject = "Message from Neel sheth"
    body = message_email

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    try:
        # Login to your Gmail account
        server.login(sender_email, "bmby ttlr ampu dilj")
        
        # Create the email message
        message = f"Subject: {subject}\n\n{body}"
        
        # Send the email
        server.sendmail(sender_email, receiver_email, message)
        print("Email sent successfully!")
        speak("Email sent successfully!")
    except :
        print("An error occurred")
        speak("Sorry some error occurred")
    finally:
        # Close the connection to the SMTP server
        server.quit()
                 
#-----------------------------------------------
# Function to process user input
def brain(mess):
    query=mess.lower()
    print("query:",query)
    if "Natasha" in query:
        speak("How can i help you ?")
        time.sleep(1)
        return "How can i help you?"
    
  
    elif "what's the time" in query:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
        time.sleep(1)
        return (f"The current time is {current_time}")
    elif "today's date" in query:
        today_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {today_date}")
        time.sleep(1)
        return (f"Today's date is {today_date}")
    elif "today's day" in query:
        today_day = datetime.datetime.now().strftime("%A")
        speak(f"Today is {today_day}")
        time.sleep(1)
        return (f"Today is {today_day}")
    elif "google opened" in query or "open google" in query or "opening google" in query:   
        webbrowser.open("https://www.google.com")
        speak("Opening Google")
        time.sleep(3)
        return ("Opening Google")
    elif "youtube opened" in query or  "open youtube" in query or "opening youtube" in query:   

        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")
        time.sleep(3)
        return ("Opening YouTube")
    elif "search youtube for " in query:
        search_query = query.split("for", 1)[1].strip()
        print("search query", search_query)
        webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        speak(f"Searching YouTube for '{search_query}'")
        time.sleep(3)
        return (f"Searching YouTube for '{search_query}'")
   
    elif "jupyter" in query or "jupiter" in query:
       subprocess.Popen(['jupyter', 'notebook'])
       speak("Opening Jupiter notebook")
       return "Jupyter opened"
    elif "cmd" in query or "command prompt" in query:
      os.system("start /B start cmd.exe @cmd /k mycommand...")
      return "cmd opened"
    elif "vs code" in query:
      # Path to the Visual Studio Code executable
      vscode_path = "C:\\Users\\neelsheth\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
      # Open Visual Studio Code
      subprocess.Popen([vscode_path])
      return ("VS code opened")

   

    elif "notepad opened" in query or "open notepad" in query or "opening notepad" in query:
        subprocess.Popen(["notepad.exe"])
        speak("Opening Notepad")
        time.sleep(3)
        return ("Opening Notepad")
    elif "close notepad" in query or "closing notepad" in query:
        for proc in psutil.process_iter():
            if "notepad" in proc.name().lower():
                proc.terminate()
                speak("Notepad has been closed.")
                time.sleep(1)
                break  
        return ("Notepad has been closed.")
    elif "news" in query:
        try:
            category=query.split("of", 1)[1].strip()
            get_news_by_category(category)
            return("News are spoken by Natasha..........")  

        except:
            speak("Sorry, can you speak again")    
    elif "search google for" in query:
        search_query = query.split("for", 1)[1].strip()
        search_url = f"https://www.google.com/search?q={search_query}"
        webbrowser.open(search_url)
        speak(f"Searching Google for {search_query}")
        time.sleep(1)
        return(f"Searching Google for {search_query}")
    elif "minimizing the tab" in query or "minimise the tab" in query or "minimize  tab" in query:
        handle_window_action("minimize")
        return "minimizing the tab"
    elif "maximizing the tab" in query or "maximise the tab" in query or "maximize tab" in query:
        handle_window_action("maximize")
        return "maximizing the tab"
    elif "up the tab" in query:
        handle_window_action("up")
        return "up the tab"
    elif "drag the tab" in query:
        handle_window_action("down") 
        return "drag the tab"
    elif "change tab" in query:
        handle_window_action("alt_tab") 
        return "change tab"
    elif "next tab" in query:
        handle_window_action("next") 
        return "next tab"
    elif "close tab" in query:
        handle_window_action("close")  
        return "close tab"
    elif "sleep" in query:
        speak("You want to turn sleep mode ?")
        time.sleep(1)
        a= speechrecog()
        if "yes" in a:
            speak("Turn the laptop in sleep mode in 3 seconds")
            time.sleep(2)
            for i in range(1,4):
                speak(i)
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            exit()
    elif "shutdown" in query or "shut down" in query:
        speak("You want to shutdown your laptop ?")
        time.sleep(1)
        a= speechrecog()
        if "yes" in a:
            speak("Initiating shutdown in 3 seconds")
            time.sleep(2)
            for i in range(1,4):
                speak(i)
            os.system("shutdown /s /t 1")
            exit()
            
    elif "screenshot" in query:
        ans=take_screenshot()  # Call the function to take a screenshot        
        return ans
    elif "pause" in query:
        keyboard.press_and_release('space')  # Press spacebar to pause the video
        speak("Video paused")
        time.sleep(1)  
        return "pausing the video"
    elif "message" in query:
        speak("Sure, please tell me what message you want to write.")
        time.sleep(1)
        message = speechrecog()
        if message:
            ans=write_and_save_message(message)  # Call the function to write and save the message
            return ans
    #image generation
    elif "generate image of" in query:
      gen_img = query.split("of", 1)[1].strip()
      speak("sure")
      time.sleep(1)
      ans=generate_image(gen_img)
      return ans
    #email sending
    elif "send email" in query:
        speak("Give email id:")
        emailer=speechrecog()
        speak(f"what message you want to send to {emailer}")
        message_email=speechrecog()
        email_sender(emailer,message_email)
        return(f"Email sent successfully to {emailer}")        
    elif query == "who are you" or query == "What is your name" or query == "tell me your name":
        speak("I am Natalia Alianovna Romanova, more commonly known as Natasha Romanoff, developed by Neel Sheth. My name is inspired by the fictional character primarily portrayed by Scarlett Johansson in the Marvel Cinematic Universe.")
        time.sleep(1)
        return ("I am Natalia Alianovna Romanova, developed by Neel Sheth. My name is inspired by the fictional character primarily portrayed by Scarlett Johansson in the Marvel Cinematic Universe.")
    elif "open cv" in query:
        search_url = f"https://digitalcv-neel-sheth.streamlit.app/"
        webbrowser.open(search_url)  
        speak("Opening your Digital CV")
        time.sleep(1)      
        return("Opening your Digital CV")
    elif "play" in query:
        query1=query.split("play")[-1]
        play(query1)
        return (f"playing {query1}")
    elif "download video" in query:
        download_video()  
        return("Video Downloaded")  
    elif "can you download song" in query:
        speak("Yes")
        time.sleep(0.3)
        download_song_from_youtube()  
        return("Song Downloaded")
    elif "take photo" in query:
      capture_single_photo(f"{query}.jpg")
      return (f"Photo saved as {query}.jpg")  
    elif "who created you" in query:
      speak("Neel sheth")
      time.sleep(1)  
      return"Neel Sheth"     
    #elif "what" in query or "how" in query or "who" in query:
    elif "start saved music" in query:
      speak("Starting Music.............")
      song_dir=r"C:\Users\neelsheth\Downloads\personal_ai\my_music"
      songs=os.listdir(song_dir)
      os.startfile(os.path.join(song_dir,songs[0]))  
      return("Starting Music.............")
    elif "turnoff media" in query:
              close_media_players()
              return("turnoff media player")
    else:
           output=Gemini(query)
           output = output.replace('*', '').replace('\n', ',')
           speak(output)
           time.sleep(1)
           return(output)

  # Main loop

# Define your backend functions
@eel.expose
def listen_and_send():  
        
                user_response = speechrecog()  
                
                text=brain(user_response)
                return text
@eel.expose
def interact():
    speak("Yes sir!")
                
if __name__=="__main__": 
  speak("ready for face authentication")     
  time.sleep(0.5)

  speak("Align your face to camera to unlock system")  
  check=lock()            
  if check=="unlock":
    speak("Welcome back Neel sir")
    wish()
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"It's {current_time}")
    speak("I am Natasha sir. Your personal assistant")
    link()