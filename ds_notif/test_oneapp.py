from oneapp import OneApp

oneapp = OneApp(
	username = "vcb27",
	password = "gzby82!",
	server_name = 'fe-sandbox-oneapp.futurexlabs.com',
	server_port = 443
)

def message_handler (chat_thread_id, text_content, **message):
	oneapp.send_message(
		chat_thread_id = chat_thread_id,
		text_content = 'You said: ' + text_content + '.'
		)

oneapp.on_message(message_handler, chat_thread_id = True, text_content = True)
oneapp.wait()