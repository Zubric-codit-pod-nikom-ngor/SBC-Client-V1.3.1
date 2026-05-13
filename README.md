# SBC-Client-V1.3.1
-----------=========== ENGLISH ===========-----------

/////////////////////////////////////////

Quick mention that you agree to privacy terms of all tools and programs used in this project if you download this repo on your device!

/////////////////////////////////////////

Simple Blockchain client. Based on my other repo with core module for python, which is public for everyone. This repo contains exclusive information, code and data that was not encrypted yet. I require you to be very careful.

Also i wanted to mention that project was not supported with proper comments and the whole repo is just raw stuff from my project, that means it was not changed in any way.
Repo contains only barebones version of client, that means there are only essential files here, (i recommend not to trust the names in this repo completely, just so you know), program was not made for modding is something important to know though some things may be easily modified.

Also if you wanted to look into the logs the program was making, it's in a corresponding dirrectory but you will see that count starts from somthing like 1600 because i cleaned a bunch of logs (something like 30000 files from testing and i was resetting counter every 3000 files) and forgot to reset the counter file (which you can do by yourself ^-^ ).

A link for .exe setup: https://drive.google.com/file/d/1jcOoITVpSMfjd8BHtmOvBbsPATQgLMDF/view

A link for my core repo:  https://github.com/Zubric-codit-pod-nikom-ngor/SBC-package

A small walkthrough:

  1) sbc dirrectory is the place where the magic happens, there you can view blockchain structure, though is may be hard to navigate. Most important files for this section is base.py (which is actually the encrypted core in the base repo), essentials.py, aes256.py, deep_encoding.py. There are many other files, some of which contain a whole bunch of encodings, useless data or something used for testing. base.py file is a bridge between other mentioned files, it processes a user's connecton; essentials.py is a file filled with safety algorithms and Block, Chain classes; aes265.py is a file that makes working with encryption less painful; deep_encoding.py is a script that processes data and makes it easy to decode and encode data with multiple or one encoding even if it/they are unknown, it takes encodings from corresponding file.
  
  2) sbc_bootstrapping is the place where client finds correct sources for connecting to blockchain, it is pretty straigt forward and if you want to open your own server for bootstrapping i recommend running bootsrapping_server.py which is not in the same dirrectory we are talking about and configuring which sources would client try to connect to in sources.json file.
  
  3) UI.py is the main script that works with UI, it is made with CustomTkinter, which documentation you can see here: https://customtkinter.tomschimansky.com/
  
  4) error.vbs is a windows file that makes a simple message when program fails to load external IP through STUN, it is harmless and does nothing other than showing text
  
  5) requirements.txt is a file that lists every module you need to run this program in its raw state, it is made so that PyCharm can recoginze it and automatically load everything needed
  
  6) settings.stng is a simple file that contains base user preferences, also it does not need anything special to open, the fancy file type is just for looks
  
  7) UI.spec is a .spec file that configures compilator (pyinstaller to be exact) and you can just compile everything with ```pyinstaller UI.spec``` if you have it
  
  8) sbc setup compiler files.iss is a file from a program innoSetup, it mainly makes a setup, though the file may be incompatible with your device and you will have to manually change paths
  
  9) pictures and videos are placeholders for main menu (drawn by me and you wouldn't beleve me it was made in powerpoint)


-----------=========== РУССКИЙ ===========-----------

/////////////////////////////////////////

Быстрое напоминание: при скачивании репозитория вы соглашаетесь на Условия Конфиденциальности всех инструментов, используемых в данном проекте

/////////////////////////////////////////

Программа-клиент блокчейна SBC. Данный репозиторий основан на другом моём репозитории с модулем-ядром для Python, который открыт для всех. Этот репозиторий содержит эксклюзивную информацию, код и данные, которые ещё не были зашифрованы. Прошу вас быть очень осторожными.

Также хочу отметить, что проект не сопровождался должными комментариями, и весь репозиторий - это практически сырой (должно не отформатирован для просмотра пользователем, по функционалу он полностью рабочий) материал из моего проекта, то есть он никак не изменялся.
Репозиторий содержит только базовую версию клиента, а значит здесь находятся только самые необходимые файлы (рекомендую не слишком полагаться на имена файлов и переменныъ в этом репозитории), программа не была заточена под модификацию - важная информация которую надо упомянуть, хотя некоторые аспекты поддаются лёгкому изменению.

Если вы захотите посмотреть логи, которые создавала программа, они находятся в соответствующей директории, но вы увидите, что нумерация начинается примерно с 1600, потому что я удалил много логов (около 30000 файлов за время тестирования и сбрасывал счётчик каждые 3000 файлов) и забыл сбросить файл-счётчик (вы можете сделать это самостоятельно ^-^).

Ссылка на .exe установщик: https://drive.google.com/file/d/1jcOoITVpSMfjd8BHtmOvBbsPATQgLMDF/view

Ссылка на репозиторий с модулем-ядром:  https://github.com/Zubric-codit-pod-nikom-ngor/SBC-package

Небольшое руководство:

  1) sbc - директория, где происходит всё самое интересное. Здесь вы можете увидеть структуру блокчейна, хотя ориентироваться в ней может быть сложно. Самые важные файлы в этом разделе: base.py (на самом деле это зашифрованное ядро из основного репозитория), essentials.py, aes256.py, deep_encoding.py. Есть и много других файлов, некоторые из которых содержат множество кодировок, бесполезные данные или то, что использовалось для тестирования. base.py - это мост между узлом и другими скриптами в этой директории, он позволяет обрабатывать подключения; essentials.py - файл, который включает в себя большинство алгоритмов, связанных с защитой данных, включает в себя классы Block и Chain; aes256.py - файл, который делает работу с криптографической функцией AES256 менее тяжёлой; deep_encoding.py - скрипт, который позволяет обработать данные, кодируя и декодируя их в различных кодировках, что делает работу с данными, которые включают одну редкую или несколько любых кодировок проще, алгоритм подбирает анализом все подходящие кодировки, даже если они неизвестны и выполняет различные операции над данными и этой кодировкой.

  2) sbc_bootstrapping - здесь клиент находит правильные источники для подключения к блокчейну. Всё довольно просто. Если вы хотите поднять свой собственный сервер для bootstrapping-а, рекомендую запустить bootsrapping_server.py (который находится не в той же директории, о которой мы говорим) и настроить в файле sources.json источники, к которым клиент будет пытаться подключиться, он будет соотвественно способен подключиться к новым источникам только после запуска именно вашей программы, остальные клиенты не будут способны обратиться к вашему источнику.

  3) UI.py - главный скрипт, который работает с интерфейсом. Он сделан с помощью customtkinter, документацию можно посмотреть здесь: https://customtkinter.tomschimansky.com/

  4) error.vbs - это файл windows, который выводит простое сообщение, когда программе не удаётся получить внешний IP через STUN. Он безвреден и ничего не делает, кроме отображения текста.

  5) requirements.txt - файл со списком всех модулей, необходимых для запуска программы в её нескомпилированном виде. Он сделан так, чтобы PyCharm мог его распознать и автоматически загрузить всё нужное.

  6) settings.stng - простой файл с базовыми пользовательскими настройками. Для его открытия не требуется ничего особенного, необычное расширение - просто для красоты.

  7) UI.spec - это файл типа .spec, который настраивает компилятор (точнее pyinstaller). Вы можете просто скомпилировать всё командой ```pyinstaller UI.spec```, если он у вас установлен.
  
  8) sbc setup compiler files.iss - файл программы innoSetup, он используется для создания установщика программы, возможно вам прийдётся поменять пути в файле вручную

  9) картинки и видио - это заставки для главного меню (нарисованы мной, и вы не поверите, но это было сделано в PowerPoint).
