'''
	Created By: Shashank S Shirol on 3/11/18

	License: MIT License
	
	Written in: Python 3.6.4
	
	Description of the Script:
	A Command-line based application to download files off of http://resource.mitfiles.com/
	Uses 'requests' to get retrieve content/web pages.
	Uses 'BeautifulSoup' to handle the retrieved web pages.
	Uses 'os' to make and handle directory creation.

	A Note from the creator:
	Feel free to use this as you please, under the guidelines of MIT License.

	Happy Coding!!

'''



from bs4 import BeautifulSoup
import requests
import json
import os

main_url = "http://resource.mitfiles.com/"

newFolder = str(os.path.dirname(os.path.realpath(__file__))) + "\\mitFiles-Downloads"
newFolder = newFolder[2:]
newFolder = newFolder.replace("\\", "/")

r = requests.get(main_url)

soup = BeautifulSoup(r.content, 'html.parser')

with open("keep_track.json", "r") as jfile:
	data = json.load(jfile)

reset = input("Do You Want to reset the Download tracker? y/n \n")
if reset is 'y':
	data["tracker"] = str(0)
	with open("keep_track.json", "w") as jfile:
		json.dump(data, jfile)

	with open("keep_track.json", "r") as jfile:
		data = json.load(jfile)


k = int(data["tracker"])
while(True):
	listDict = dict()
	keys = 1
	print("----------------------------------------------------------")
	for link in soup.find_all('a'):
		if(not link.get('href')[0].isalpha()):	
			continue
		listDict[str(keys)] = link.get('href').replace('%20', ' ')
		print(str(keys)+". "+listDict[str(keys)])
		keys = keys + 1
	print("Enter -1 to exit")
	if(main_url.count('/')>3):
		print("Enter -2 to go back by one page")
	choice = input("Enter Choice: (case-sensitive)\n")

	while(main_url.count('/')<=3 and choice == '-2'):
		choice = input("Enter appropriate choice:\n")

	while(int(choice)<-2 or int(choice)>len(listDict)):
		choice = input("Enter appropriate choice:\n")

	if(choice == '-1'):
		break

	if (choice == '-2'):
		main_url = main_url[:main_url.rfind('/', 0, -1)+1]
	else:
		choice = listDict[choice]
		choice = choice.replace(' ', '%20')
		main_url = main_url + choice

	try:
		print("Accessing: "+main_url)
		r = requests.get(main_url)
		if(str(r.status_code).startswith('5')):
			print("Internal Server Error")
			break
		elif(str(r.status_code).startswith('4')):
			print("Page not found.")
			break
		
		if 'html' in r.headers.get('content-type').lower():
			soup = BeautifulSoup(r.content, 'html.parser')
		else:
			parsed = main_url[main_url.rfind('/')+1:]
			parsed = parsed.replace('%20', ' ')
			newFile = newFolder+"/mitFiles_download_"+str(k)+"_"+parsed
			os.makedirs(os.path.dirname(newFile), exist_ok = True)
			downloader = open(newFile, 'wb')
			downloader.write(r.content)
			downloader.close()
			k = k + 1
			main_url = main_url[:main_url.rfind('/')+1]
	except requests.exceptions as e:
		print(e)
		break

data["tracker"] = str(k)
with open("keep_track.json", "w") as jfile:
	json.dump(data, jfile)