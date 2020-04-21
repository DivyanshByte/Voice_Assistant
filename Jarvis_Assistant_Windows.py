import speech_recognition as sr
import os
import sys
import re
import smtplib
import requests
import playsound
from gtts import gTTS
import wolframalpha # to calculate strings into formula 
import os.path
import datetime

num = 1
def assistant_speaks(output):
	"Speaks the assistant outputs"
	global num 

	# num to rename every audio file 
	# with different name to remove ambiguity 
	num += 1
	print("Jarvis : ", output) 

	toSpeak = gTTS(text = output, lang ='en', slow = False) 
	# saving the audio file given by google text to speech 
	file = str(num)+".mp3 "
	toSpeak.save(file) 
	
	# playsound package is used to play the same file. 
	playsound.playsound(file, True) 
	os.remove(file) 

def get_audio(): 

	rObject = sr.Recognizer() 
	audio = ""

	with sr.Microphone() as source: 
		print("Speak...") 
		
		# recording the audio using speech recognition 
		audio = rObject.listen(source, phrase_time_limit = 5) 
	print("Stop.") # limit 5 secs 

	try: 

		text = rObject.recognize_google(audio, language ='en-IN') 
		print("You : ", text) 
		return text

	except: 

		assistant_speaks("Could not understand your audio, PLease try again !") 

noten = 1
def note(notew):
	"Makes a Note"
	global noten
	noten += 1
	file_name =  "note" + str(noten) + ".txt"
	with open(file_name, "w") as f:
		f.write(notew)
	os.system("notepad " + file_name) 

def process_text(input): 
	"Process The Text"

	try: 
		if "search" in input: 
			
			search_web(input) 
			return

		elif "who are you" in input or "define yourself" in input: 
			speak = '''Hello, I am Jarvis. Your personal Assistant. 
			I am here to make your life easier. You can command me to perform 
			various tasks such as calculating sums or opening applications '''
			assistant_speaks(speak) 
			return

		elif "who made you" in input or "created you" in input: 
			speak = "I have been created by Divyansh Agrawal."
			assistant_speaks(speak) 
			return

		elif "calculate" in input: 
			
			# write your wolframalpha app_id here 
			app_id = "divyansh042009@gmail.com"
			client = wolframalpha.Client(app_id) 

			assistant_speaks("What Do You Want to Calculate")
			query = get_audio()
			res = client.query(" ".join(query)) 
			answer = next(res.results).text 
			assistant_speaks("The answer is " + answer) 
			return

		elif "launch" in input: 
			
			# another function to open 
			# different application availaible 
			open_application(input.lower()) 
			return
		
		elif "make a note" in input or "write a note" in input or "write" in input or "remember this" in input:
				assistant_speaks("What would you want me to write down ?")
				write = get_audio()
				note(write)
				assistant_speaks("I have Made a note of that")
				return
		
		elif "poweroff" in input or "shutdown" in input:
			assistant_speaks("Do you really want to shudown your computer ?")
			ans = get_audio() 
			if "yes" in str(ans) or "yeah" in str(ans) or "ya" in str(ans): 
				os.system("poweroff")
			return

		elif "reboot" in input or "restart" in input:
			assistant_speaks("Do you really want to restart your computer ?")
			ans = get_audio() 
			if "yes" in str(ans) or "yeah" in str(ans) or "ya" in str(ans): 
				os.system("reboot")
			return

		elif "time" in input:
			now = datetime.datetime.now()
			assistant_speaks("Current time is %d hours %d minutes" % (now.hour , now.minute))	
			return

		elif "email" in input or "send email" in input or "write email" in input:
			assistant_speaks("Whom do you want to send email ? ")
			recipent = get_audio()
			if "Recipent_1" in recipent:
				assistant_speaks("What should I Write to Him ?")
				content = get_audio()
				mail = smtplib.SMTP('smtp.gmail.com', 587)
				mail.ehlo()
				mail.starttls()
				mail.login('sender_email', 'sender_pass')
				mail.sendmail('sender_email', 'reciever_email', content)
				mail.close()
				assistant_speaks("Mail had been send to Reciepent 1.")
			else:
				assistant_speaks("Cannot find any Recipent")
			return
		
		elif "open" in input:
			assistant_speaks("Tell me website domain name, you want to open.")
			domain = get_audio()
			os.system("chrome " + "https://www." + domain)
		
		elif "help me" in input:
			assistant_speaks(""" 
			You Can use These Commands in Jarvis:
			1. Search to search anyting on web.
			2. Calculate
			3. Launch any application
			4. Write Down
			5. Email
			6. Open any website
			7. Restart your Computer
			8. Shutdown your Computer
			9. Time
			""")
			return

		else: 

			assistant_speaks("I can search the web for you, Do you want to continue?") 
			ans = get_audio() 
			if "yes" in str(ans) or "yeah" in str(ans) or "ya" in str(ans): 
				search_web(input) 
			else: 
				return
	except : 

		assistant_speaks("I don't understand, I can search the web for you, Do you want to continue?") 
		ans = get_audio() 
		if "yes" in str(ans) or "yeah" in str(ans) or "ya" in str(ans): 
			search_web(input) 
def search_web(input): 
 

	if "youtube" in input.lower(): 

		assistant_speaks("Opening in youtube") 
		indx = input.lower().split().index('youtube') 
		query = input.split()[indx + 1:] 
		os.system("chrome " + "http://www.youtube.com/results?search_query =" + "+".join(query)) 
		return

	elif "wikipedia" in input.lower(): 

		assistant_speaks("Opening Wikipedia") 
		indx = input.lower().split().index("wikipedia") 
		query = input.split()[indx + 1:] 
		os.system( "chrome " + "https://en.wikipedia.org/wiki/" + "_".join(query)) 
		return

	else: 

		if "google" in input: 

			indx = input.lower().split().index("google") 
			query = input.split()[indx + 1:] 
			os.system("chrome " + "https://www.google.com/search?q =" + "+".join(query)) 

		elif "search" in input: 

			indx = input.lower().split().index("google") 
			query = input.split()[indx + 1:] 
			os.system("chrome "+"https://www.google.com/search?q =" + "+".join(query)) 

		else: 

			os.system("chrome "+"https://www.google.com/search?q =" + "+".join(input.split())) 

		return


# function used to open application 
# present inside the system. 
def open_application(input): 

	if "chrome" in input: 
		assistant_speaks("Google Chrome") 
		os.system("chrome")
		return

	elif "firefox" in input or "mozilla" in input: 
		assistant_speaks("Opening Mozilla Firefox") 
		os.system("firefox")
		return

	elif "code" in input: 
		assistant_speaks("Opening Visual Studio Code") 
		os.system("code")
		return

	elif "Command Prompt" in input: 
		assistant_speaks("Opening Command Prompt") 
		os.system("cmd")
		return
	
	elif "File Browser" in input:
		assistant_speaks("Opening File Browser")
		os.system("C:")
		return

	else: 

		assistant_speaks("Application not available") 
		return

if __name__ == "__main__": 
	assistant_speaks("What's your name, Human?") 
	name = ""
	name = get_audio() 
	assistant_speaks("Hello, " + str(name) ) 
	while(1): 
		assistant_speaks("What can I do for you?") 
		text = str(get_audio()).lower() 
		if text == 0: 
			continue
		if "exit" in str(text) or "bye" in str(text) or "sleep" in str(text): 
			assistant_speaks("Ok bye, "+ name+'.') 
			break
		process_text(text)


