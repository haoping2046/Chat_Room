from tkinter import Tk, Label, Entry, Frame, Button, LEFT, END

class WindowLogin(Tk):
    def __init__(self):
        super(WindowLogin, self).__init__()

        # set window property
        self.window_init()

        # set widgets
        self.add_widgets()

        # self.on_click_login(lambda: print(self.get_username()))
        # self.on_click_reset(lambda: self.clear())

    def window_init(self):
        self.title('Login')
        self.resizable(width=False, height=False)

        window_width, window_height = 255, 95
        pos_x, pos_y = (self.winfo_screenwidth() - window_width) / 2, (self.winfo_screenheight() - window_height) / 2
        self.geometry('%dx%d+%d+%d' % (window_width, window_height, pos_x, pos_y))

    def add_widgets(self):
        username_label = Label(self)
        username_label['text'] = 'Username:'
        username_label.grid(row=0, column=0, padx=10, pady=5)

        username_entry = Entry(self, name='username_entry')
        username_entry['width'] = 15
        username_entry.grid(row=0, column=1)

        password_label = Label(self)
        password_label['text'] = 'Password:'
        password_label.grid(row=1, column=0)

        password_entry = Entry(self, name='password_entry')
        password_entry['width'] = 15
        password_entry['show'] = '*'
        password_entry.grid(row=1, column=1)

        button_frame = Frame(self, name='button_frame')
        button_frame.grid(row=2, columnspan=2, pady=5)

        reset_button = Button(button_frame, name='reset_button')
        reset_button['text'] = ' reset '
        reset_button.pack(side=LEFT, padx=20)

        login_button = Button(button_frame, name='login_button')
        login_button['text'] = ' login '
        login_button.pack(side=LEFT)

        # login_button['command'] =

    def on_click_reset(self, command):
        reset_button = self.children['button_frame'].children['reset_button']
        reset_button['command'] = command

    def on_click_login(self, command):
        login_button = self.children['button_frame'].children['login_button']
        login_button['command'] = command

    def clear(self):
        self.children['username_entry'].delete(0, END)
        self.children['password_entry'].delete(0, END)

    def get_username(self):
        return self.children['username_entry'].get()

    def get_password(self):
        return self.children['password_entry'].get()

    def on_window_closed(self, command):
        print('close')
        self.protocol('WM_DELETE_WINDOW', command)

if __name__ == '__main__':
    window = WindowLogin()
    window.mainloop()