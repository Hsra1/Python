from tkinter import Tk, Canvas
from Vectors import vector
from math import floor
from random import randint


class ball:

    def __init__(self, x, y, dia, mass, vel):
        self.draw = world.create_oval(
            x,
            y,
            x + dia,
            y + dia,
            fill="#0D8B31",
            outline="#000000",
            width=5,
        )
        self.vel = vel
        self.rad = dia / 2
        self.mass = mass

    def box(self):
        return world.coords(self.draw)

    def pos(self):
        return vector([self.box()[0] + self.rad, self.box()[1] + self.rad])


def move(ball):
    world.move(ball.draw, ball.vel[0], ball.vel[1])


def accel(ball):
    ball.vel += acc


def conserve(b1, b2, v1, v2):
    vf1 = (v1 * (b1.mass - b2.mass) + (v2 * 2 * b2.mass)) / (b1.mass + b2.mass)
    vf2 = (v2 * (b2.mass - b1.mass) + (v1 * 2 * b1.mass)) / (b1.mass + b2.mass)
    return [vf1, vf2]


def item_collision(balls):
    for i, b1 in enumerate(balls):
        for b2 in balls[i + 1 :]:
            rel = b1.pos() - b2.pos()
            if rel.mod() < (b1.rad + b2.rad):
                shift = rel * ((b1.rad + b2.rad) / rel.mod()) - rel
                v1 = b1.vel.projection(rel)
                v2 = b2.vel.projection(rel)
                world.move(b1.draw, shift[0], shift[1])
                temp = conserve(b1, b2, v1, v2)
                b1.vel += temp[0] - v1
                b2.vel += temp[1] - v2


def wall_collision(ball):
    x1, y1, x2, y2 = ball.box()
    if x2 > side:
        world.move(ball.draw, side - x2, 0)
        ball.vel[0] *= -1
    if x1 < 0:
        world.move(ball.draw, -x1, 0)
        ball.vel[0] *= -1
    if y2 > side:
        world.move(ball.draw, 0, side - y2)
        ball.vel[1] *= -1
    if y1 < 0:
        world.move(ball.draw, 0, -y1)
        ball.vel[1] *= -1


def dis(balls):
    temp = ""
    for i in balls:
        temp += f"{floor(i.vel.vec[0])} {floor(i.vel.vec[1])}\n"
    world.itemconfig(txt, text=temp)


def update(balls):
    dis(balls)
    for i in balls:
        accel(i)
        move(i)
        wall_collision(i)
    item_collision(balls)
    root.after(tick, lambda: update(balls))


acc = vector([0, 1])
side = 600
tick = 50

root = Tk()
root.title("Collisions")
root.geometry(f"{side}x{side}")

world = Canvas(height=side, width=side, bg="#2695BA")
world.pack()

txt = world.create_text(60, 60)

b1 = ball(300, 300, 50, 1, vector([]))
b2 = ball(300, 300, 50, 1, vector([]))
b3 = ball(300, 300, 50, 1, vector([]))

balls = [b1, b2, b3]
for i in balls:
    i.vel.vec = [randint(1, 5), randint(0, 5)]

update(balls)
root.mainloop()
