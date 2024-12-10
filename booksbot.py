# -*- coding: cp1251 -*-
import telebot
from telebot import types


booksbot = telebot.TeleBot(token);
chats = set();




@booksbot.message_handler(commands = ["start"])
def start(message):

	way = ".\\";
	if message.chat.id not in chats:
		chats.add(message.chat.id);
		with open("chats.txt", "a") as fp:
			fp.write(message.chat.id);
			fp.write("\n");

	markup = types.InlineKeyboardMarkup();
	btn = [];
	btn.append(types.InlineKeyboardButton("Поддержать проект", url = "https://www.donationalerts.com/r/booksbot"));
	i = 1;
	with open (way + "list.txt") as fp:
		for line in fp:
			str1, str2 = line.strip().split('/');
			btn.append(types.InlineKeyboardButton(str1, callback_data = way + str2));
			markup.row(btn[i]);
			i += 1;
	markup.row(btn[0]);

	booksbot.send_message(
		message.chat.id, 
		"""Здравствуйте! В этом боте вы сможете найти интересующую вас образовательную литературу и учебные материалы по разным наукам и дисциплинам. Наша база данных пополняется новыми книгами и конспектами.

Ознакомиться со списком команд вы сможете по команде /help, вернуться в главное меню -- /mainmenu или /main, сообщить о проблеме или предложить идею -- /report

Наш проект планирует развиваться: в будущем мы хотим набрать старые книги в Латехе, чтобы повысить визуальное качество материала, избавиться от артефактов сканеров. Для хранения книг и автоматизации процессов нам нужны сервера. А потому нам очень нужны ваши пожертвования, даже самые маленькие. По соответствующей кнопке вы можете перевести нам эквивалент чашки кофе, это очень нам поможет :)
 
Литературу по какой науке вы желаете найти?""",
		reply_markup = markup
	);





@booksbot.message_handler(commands = ["mainmenu", "main"])
def mainmenu(message):
	way = ".\\";

	markup = types.InlineKeyboardMarkup();
	btn = [];
	btn.append(types.InlineKeyboardButton("Поддержать проект", url = "https://www.donationalerts.com/r/booksbot"));
	i = 1;
	with open (way + "list.txt") as fp:
		for line in fp:
			str1, str2 = line.strip().split('/');
			btn.append(types.InlineKeyboardButton(str1, callback_data = way + str2));
			markup.row(btn[i]);
			i += 1;
	markup.add(btn[0]);

	booksbot.send_message(
		message.chat.id, 
		"Литературу по какой науке вы желаете найти?",
		reply_markup = markup
	);
	



@booksbot.callback_query_handler(func = lambda callback: True)
def callback_message(callback):
	way = callback.data.split("\\");

	if (callback.data == "main"):
		mainmenu(callback.message);
	elif (len(way) == 2) or ((len(way) == 4) and (way[3] == "back")):
		callback_message1(callback);
	elif ((len(way) == 3) or ((len(way) == 5) and (way[4] == "back"))):
		callback_message2(callback);
	elif ((len(way) == 4) or ((len(way) == 6) and (way[5] == "back"))):
		callback_message3(callback);
	else:
		callback_message4(callback);




def callback_message1(callback):
	way = callback.data;
	if (way.rsplit("\\", 1)[1] == "back"):
		way = callback.data.rsplit("\\", 2)[0];

	markup = types.InlineKeyboardMarkup();
		
	btn = [];
	btn.append(types.InlineKeyboardButton("Поддержать проект", url = "https://www.donationalerts.com/r/booksbot"));
	btn.append(types.InlineKeyboardButton("Главное меню", callback_data = "main"));
	i = 2;

	try:
		with open (way + "\\list.txt") as fp:		
			for line in fp:
				str1, str2 = line.strip().split('/');
				btn.append(types.InlineKeyboardButton(str1, callback_data = way + "\\" + str2));
				markup.row(btn[i]);
				i += 1;
		markup.add(btn[0], btn[1]);
		if (len(btn) == 2):
			booksbot.send_message(
				callback.message.chat.id, 
				"Кажется, тут пока пусто :(",
				reply_markup = markup
			);
		else:
			booksbot.send_message(
				callback.message.chat.id, 
				"Какой раздел вас интересует?",
				reply_markup = markup
			);

	except FileNotFoundError:
		
		markup.add(btn[0], btn[1]);
		booksbot.send_message(
			callback.message.chat.id, 
			"Этот каталог либо временно недоступен, либо уже не существует :(",
			reply_markup = markup
		);




def callback_message2(callback):
	way = callback.data;
	if (way.rsplit("\\", 1)[1] == "back"):
		way = callback.data.rsplit("\\", 2)[0];

	markup = types.InlineKeyboardMarkup();
	btn = [];
	btn.append(types.InlineKeyboardButton("Поддержать проект", url = "https://www.donationalerts.com/r/booksbot"));
	btn.append(types.InlineKeyboardButton("Шаг назад", callback_data = way + "\\back"));
	btn.append(types.InlineKeyboardButton("Главное меню", callback_data = "main"));
	i = 3;

	try:
		strlist = "";
		with open (way + "\\list.txt") as fp:
			for line in fp:
				str1, str2 = line.strip().split('/');
				strlist += str1 + "\n\n"
				btn.append(types.InlineKeyboardButton(str1, callback_data = way + "\\" + str2));
				markup.row(btn[i]);
				i += 1;
		markup.add(btn[0]);
		markup.row(btn[1], btn[2]);
		if (len(btn) == 3):
			booksbot.send_message(
				callback.message.chat.id, 
				"Кажется, тут пока пусто :(",
				reply_markup = markup
			);
		else:
			booksbot.send_message(
				callback.message.chat.id, 
				"У нас тут есть следующая литература:\n\n<em>" + strlist + "</em>",
				parse_mode = "html", reply_markup = markup
			);

	except FileNotFoundError:
		markup.add(btn[0]);
		markup.add(btn[1], btn[2]);
		booksbot.send_message(
			callback.message.chat.id, 
			"Этот каталог либо временно недоступен, либо уже не существует :(",
			reply_markup = markup
		);




def callback_message3(callback):
	way = callback.data;
	if (way.rsplit("\\", 1)[1] == "back"):
		way = callback.data.rsplit("\\", 2)[0];

	markup = types.InlineKeyboardMarkup();

	btn = [];
	btn.append(types.InlineKeyboardButton("Поддержать проект", url = "https://www.donationalerts.com/r/booksbot"));
	btn.append(types.InlineKeyboardButton("Шаг назад", callback_data = way + "\\back"));
	btn.append(types.InlineKeyboardButton("Главное меню", callback_data = "main"));
	i = 3;

	try:
		strlist = "";
		with open (way + "\\list.txt") as fp:
			for line in fp:
				str1, str2 = line.strip().split('/');
				strlist += str1 + "\n\n";
				btn.append(types.InlineKeyboardButton(str1, callback_data = way + "\\" + str2));
				markup.row(btn[i]);
				i += 1;
		markup.add(btn[0]);
		markup.add(btn[1], btn[2]);
		if (len(btn) == 3):
			booksbot.send_message(
				callback.message.chat.id, 
				"Кажется, тут пока пусто :(",
				reply_markup = markup
			);
		else:
			booksbot.send_message(
				callback.message.chat.id, 
				"Какая книга Вас интересует?\n\n<em>" + strlist + "</em>",
				parse_mode = "html", reply_markup = markup
			);

	except FileNotFoundError:
		markup.add(btn[0]);
		markup.add(btn[1], btn[2]);
		booksbot.send_message(
			callback.message.chat.id, 
			"Этот каталог либо временно недоступен, либо уже не существует :(",
			reply_markup = markup
		);




def callback_message4(callback):
	way = callback.data;

	try:
		with open(way, "rb") as fp:
			booksbot.send_document(callback.message.chat.id, fp, timeout = 100);
		booksbot.send_message(callback.message.chat.id,	"Ваш файл!");
	except FileNotFoundError:
		booksbot.send_message(callback.message.chat.id, "Этот файл либо временно недоступен, либо уже не существует :(");
	except:
		booksbot.send_message(callback.message.chat.id, "Кажется, с этим файлом какие-то проблемы. Попробуйте немного позже.");

	markup = types.InlineKeyboardMarkup();
	btn = [];
	btn.append(types.InlineKeyboardButton("Поддержать проект", url = "https://www.donationalerts.com/r/booksbot"));
	btn.append(types.InlineKeyboardButton("Шаг назад", callback_data = way + "\\back"));
	btn.append(types.InlineKeyboardButton("Главное меню", callback_data = "main"));
	markup.row(btn[0]);
	markup.row(btn[1], btn[2]);
	booksbot.send_message(
		callback.message.chat.id, 
		"Вы можете поддержать наш проект разовым или регулярным пожертвованием -- это поможет нам оставаться на плаву :3",
		reply_markup = markup
	);




@booksbot.message_handler(commands = ["help"])
def help(message):
	markup = types.InlineKeyboardMarkup();
	btn = [];
	btn.append(types.InlineKeyboardButton("Поддержать проект", url = "https://www.donationalerts.com/r/booksbot"));
	btn.append(types.InlineKeyboardButton("Главное меню", callback_data = "main"));
	markup.row(btn[0]);
	markup.row(btn[1]);

	booksbot.send_message(message.chat.id, """<b>Актуaльный список команд:</b>

/start <em>--- начало работы с ботом</em>

/main, /mainmenu <em>--- главное меню</em>

/report <em>--- сообщить о проблеме или предложить идею</em>

/help <em>--- список команд</em>""", parse_mode = "html", reply_markup = markup);




@booksbot.message_handler(commands = ["report"], content_types = ["text"])
def report(message):
	booksbot.send_message(message.chat.id, "Введите ваше сообщение");
	booksbot.register_next_step_handler(message, reportwrite);


def reportwrite(message):
	markup = types.InlineKeyboardMarkup();
	btn = [];
	btn.append(types.InlineKeyboardButton("Поддержать проект", url = "https://www.donationalerts.com/r/booksbot"));
	btn.append(types.InlineKeyboardButton("Главное меню", callback_data = "main"));
	markup.row(btn[0]);
	markup.row(btn[1]);

	fp = open(".\\reports.txt", "a");
	fp.write(str(message.chat.id));
	fp.write("\n");
	fp.write(message.from_user.username);
	fp.write("\n\n");
	try:
		fp.write(message.text);
		fp.write("\n\n\n");
		fp.close();
		booksbot.send_message(message.chat.id, "Ваше сообщение записано!", reply_markup = markup);
	except:
		fp.write("None");
		fp.write("\n\n\n");
		fp.close();
		booksbot.send_message(message.chat.id, "Ваше сообщение не записано :(\nПопробуйте ещё раз: /report. Не прикрепляйте фотографии, аудио, стикеры и прочее.", reply_markup = markup);




@booksbot.message_handler(commands = ["rassilka"])
def rassilka(message):
	if (message.chat.id == 1124197418):
		with open("text.txt", "r") as fp:
			for line in fp:
				text += line;
		text = text.strip();
		if (text != ""): 
			with open ("chats.txt", "r") as fp:
				chats = set();
				for i in fp:
					chats.add(i.strip());
				for i in chats:
					booksbot.send_message(i, text);




booksbot.polling(none_stop = True)