# SBC-Client-V1.3.1
Simple Blockchain client. Based on my other repo with core module for python, which is public for everyone. This repo contains exclusive information, code and data that was not encrypted yet. I require you to be very careful.

Also i wanted to mention that project was not supported with proper comments and the whole repo is just raw stuff from my project, that means it was not changed in any way.
Repo contains only barebones version of client, that means there are only essential files here, (i recommend not to trust the names in this repo completely, just so you know).

A small walkthrough:

  sbc dirrectory is the place where the magic happens, there you can view blockchain structure, though is may be hard to navigate. Most important files for this section is base.py (which is actually the encrypted core in the base repo), essentials.py, aes256.py, deep_encoding.py. There are many other files, some of which contain a whole bunch of encodings, useless data or something used for testing.
  
  sbc_bootstrapping is the place where client finds correct sources for connecting to blockchain, it is pretty straigt forward and if you want to open your own server for bootstrapping i recommend running bootsrapping_server.py which is not in the same dirrectory we are talking about and configuring which sources would client try to connect to in sources.json file.
  
  UI.py is the main script that works with UI, it is made with CustomTkinter, which documentation you can see here: https://customtkinter.tomschimansky.com/
  
  error.vbs is a windows file that makes a simple message when program fails to load external ip through STUN, it is harmless and does nothing other than showing text
  
  requirements.txt is a file that lists every module you need to run this program in its raw state, it is made so that pycharm can recoginze it and automatically load everything needed
  
  settings.stng is a simple file that contains base user preferences, also it does not need anything special to open, the fancy file type is just for looks
  
  UI.spec is a .spec file that configures compilator (pyinstaller to be exact) and you can just compile everything with ```pyinstaller UI.spec``` if you have it
  
  pictures and videos are placeholders for main menu (drawn by me and you wouldn't beleve me it was made in powerpoint)

  
