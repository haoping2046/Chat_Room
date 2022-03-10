from tkinter import Toplevel, Text, Button, END, UNITS
from tkinter.scrolledtext import ScrolledText
from time import localtime, strftime, time

class WindowChat(Toplevel):
    def __init__(self):
        super(WindowChat, self).__init__()

        # set window property
        self.window_init()

        # set widgets
        self.add_widgets()

        # self.on_click_send_btn(lambda: self.append_msg('Hao', 'Hello'))

    def window_init(self):
        self.resizable(width=False, height=False)
        self.geometry('%dx%d' % (795, 505))

    def add_widgets(self):
        # chat area
        chat_text_area = ScrolledText(self)
        chat_text_area['width'] = 110
        chat_text_area['height'] = 30
        chat_text_area.grid(row=0, column=0, columnspan=2)
        chat_text_area.tag_config('user', foreground='green')
        chat_text_area.tag_config('me', foreground='blue')
        self.children['chat_text_area'] = chat_text_area

        # input area
        chat_input_area = Text(self, name='chat_input_area')
        chat_input_area['width'] = 100
        chat_input_area['height'] = 7
        chat_input_area.grid(row=1, column=0)

        # button
        send_button = Button(self, name='send_button')
        send_button['text'] = 'send'
        send_button['width'] = 5
        send_button['height'] = 2
        send_button.grid(row=1, column=1, pady=10)

    def set_title(self, name):
        self.title('Welcome %s' % name)

    def on_click_send_btn(self, command):
        self.children['send_button']['command'] = command

    def get_input(self):
        return self.children['chat_input_area'].get(0.0, END)

    def clear(self):
        self.children['chat_input_area'].delete(0.0, END)

    def append_msg(self, sender, msg):
        send_time = strftime('%m-%d-%Y %H:%M:%S', localtime(time()))
        send_info = '%s： %s\n' % (sender, send_time)
        if sender == 'Me':
            self.children['chat_text_area'].insert(END, send_info, 'me')
        else:
            self.children['chat_text_area'].insert(END, send_info, 'user')
        self.children['chat_text_area'].insert(END, ' ' + msg + '\n')

        # scroll down 3 lines
        self.children['chat_text_area'].yview_scroll(3, UNITS)

    def on_window_closed(self, command):
        self.protocol('WM_DELETE_WINDOW', command)

# if __name__ == '__main__':
#     window = WindowChat()
#     window.mainloop()