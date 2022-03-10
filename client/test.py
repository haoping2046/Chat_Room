import tkinter

def test():
    window = tkinter.Tk()

    login_bt = tkinter.Button(window, name='login')
    login_bt['text'] = 'login'
    login_bt.grid(row=0, column=1)

    reset_bt = tkinter.Button(window, name='reset')
    reset_bt['text'] = 'reset'
    reset_bt.grid(row=0, column=0)

    window.mainloop()

if __name__ == '__main__':
    test()