from tkinter import Tk, Label, Button


def click(num):
    txt.append(num)
    dis.configure(text=txt)


def back():
    if txt:
        txt.pop()
    dis.configure(text=txt)


def out():
    inp = ""
    for i in txt:
        inp += str(i)
    dis.configure(text=eval(inp))


def draw():
    dis.grid(row=1, column=4)
    temp = 0
    for i in range(3):
        for j in range(3):
            temp += 1
            btn = Button(
                root, text=temp, width=5, height=5, command=lambda n=temp: click(n)
            )
            btn.grid(row=i, column=j)

    for i, j in enumerate(ops):
        btn = Button(root, text=j, width=5, height=5, command=lambda n=j: click(n))
        btn.grid(row=i, column=3)

    btn = Button(root, text="Backspace", width=12, height=5, command=back)
    btn.grid(row=3, column=1, columnspan=2)

    btn = Button(root, text=0, width=5, height=5, command=lambda: click(0))
    btn.grid(row=3, column=0)

    btn = Button(root, text="Enter", width=10, height=5, command=out)
    btn.grid(row=3, column=4)


root = Tk()
root.geometry("300x400")

txt = []
dis = Label(root)
ops = ["+", "-", "*", "/"]

draw()
root.mainloop()
