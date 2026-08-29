import pygame
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# Constants and Variables
screen_height = 400
screen_width = 800
graph_height = 300
rocket_height = 80
rocket_width = 40
cen = [screen_width // 2, screen_height // 2]

gravity = 0.2
wind_max = 0.1

time = 0
vx, vy = 0, 0

# Store history of Position, Velocity and Time
xs, ys, vxs, vys, ts = [0], [0], [0], [0], [0]

clock = pygame.time.Clock()

rocket = pygame.Rect(
    cen[0] - rocket_width // 2,
    cen[1] - rocket_height // 2,
    rocket_width,
    rocket_height,
)

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height + graph_height))


def draw_graphs():
    fig, ax = plt.subplots(2, 2, figsize=(8, 3))
    ax[0, 0].plot(ts, xs)
    ax[0, 0].set_ylabel("X")

    ax[0, 1].plot(ts, ys)
    ax[0, 1].set_ylabel("Y")

    ax[1, 0].plot(ts, vxs)
    ax[1, 0].set_ylabel("Vx")

    ax[1, 1].plot(ts, vys)
    ax[1, 1].set_ylabel("Vy")

    fig.tight_layout()

    canvas = FigureCanvas(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.buffer_rgba()
    size = canvas.get_width_height()
    surf = pygame.image.frombuffer(raw_data, size, "RGBA")
    plt.close(fig)
    return surf


class Pid:
    def __init__(self, kp, ki, kd, setpoint):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.integral = 0
        self.prev_error = 0

    def control(self, measurement):
        error = self.setpoint - measurement
        self.integral += error
        der = error - self.prev_error
        self.prev_error = error
        return self.kp * error + self.ki * self.integral + self.kd * der


pid_x = Pid(kp=0.02, ki=0.001, kd=0.5, setpoint=0)
pid_y = Pid(kp=0.09, ki=0.004, kd=0.3, setpoint=0)

# Game Loop
run = True
while run:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update Velocity
    vx += random.uniform(-wind_max, wind_max)
    vy += gravity

    # PID Control
    vx += pid_x.control(xs[-1])
    vy += pid_y.control(ys[-1])

    # Update Position
    rocket.x += vx
    rocket.y += vy

    # Store the Variables
    ts.append(time)
    xs.append(rocket.x - cen[0] + rocket_width // 2)
    ys.append(rocket.y - cen[1] + rocket_height // 2)
    vxs.append(vx)
    vys.append(vy)
    time += 1

    if len(ts) > 100:
        ts.pop(0)
        xs.pop(0)
        ys.pop(0)
        vxs.pop(0)
        vys.pop(0)

    # Draw
    pygame.draw.line(
        screen,
        (255, 255, 255),
        (cen[0], 0),
        (cen[0], screen_height),
    )
    pygame.draw.line(
        screen,
        (255, 255, 255),
        (0, cen[1]),
        (screen_width, cen[1]),
    )
    pygame.draw.rect(screen, (30, 150, 180), rocket)
    screen.blit(draw_graphs(), (0, screen_height))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
