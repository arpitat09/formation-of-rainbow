from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Animation state
sun_alpha = 0.0
cloud_x = -1.5
rain_drops = []
rain_active = False
rain_timer = 0
rainbow_alpha = 0.0

# Rainbow colors
colors = [
    (1.0, 0.0, 0.0),
    (1.0, 0.5, 0.0),
    (1.0, 1.0, 0.0),
    (0.0, 1.0, 0.0),
    (0.0, 0.0, 1.0),
    (0.29, 0.0, 0.51),
    (0.56, 0.0, 1.0)
]

def init():
    glClearColor(0.5, 0.7, 1.0, 1.0)  # Sky blue

def draw_sun():
    global sun_alpha
    glColor4f(1.0, 1.0, 0.0, sun_alpha)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(0.7, 0.7)
    for i in range(361):
        angle = math.radians(i)
        x = 0.1 * math.cos(angle)
        y = 0.1 * math.sin(angle)
        glVertex2f(0.7 + x, 0.7 + y)
    glEnd()

def draw_cloud(x, y):
    glColor4f(1.0, 1.0, 1.0, 0.8)
    for dx in [-0.05, 0, 0.05]:
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(x + dx, y)
        for i in range(361):
            angle = math.radians(i)
            cx = 0.1 * math.cos(angle)
            cy = 0.05 * math.sin(angle)
            glVertex2f(x + dx + cx, y + cy)
        glEnd()

def draw_rain():
    glColor4f(1.0, 1.0, 1.0, 0.6)
    glBegin(GL_LINES)
    for i in range(len(rain_drops)):
        x, y = rain_drops[i]
        glVertex2f(x, y)
        glVertex2f(x, y - 0.05)
        rain_drops[i] = (x, y - 0.02)
    glEnd()

def draw_rainbow():
    global rainbow_alpha
    band_width = 0.05
    glTranslatef(0.0, -0.4, 0.0)
    for i in range(len(colors)):
        glColor4f(*colors[i], rainbow_alpha)
        draw_arc(0.2 + i * band_width, 0.2 + (i + 1) * band_width)

def draw_arc(inner_radius, outer_radius):
    segments = 100
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(segments + 1):
        theta = math.pi * i / segments
        x = math.cos(theta)
        y = math.sin(theta)
        glVertex2f(x * outer_radius, y * outer_radius)
        glVertex2f(x * inner_radius, y * inner_radius)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    draw_sun()
    draw_cloud(cloud_x, 0.7)
    draw_cloud(cloud_x + 0.4, 0.65)

    if rain_active:
        draw_rain()

    if rainbow_alpha > 0:
        draw_rainbow()

    glutSwapBuffers()

def update(value):
    global sun_alpha, cloud_x, rain_active, rain_timer, rainbow_alpha, rain_drops

    # Sun fade in
    if sun_alpha < 1.0:
        sun_alpha += 0.005

    # Clouds move
    if cloud_x < 0.2:
        cloud_x += 0.003

    # After clouds arrive, start rain
    elif not rain_active and rain_timer < 100:
        rain_timer += 1
    elif not rain_active and rain_timer >= 100:
        rain_active = True
        rain_drops = [(random.uniform(-1.0, 1.0), random.uniform(0.0, 1.0)) for _ in range(300)]

    # After rain starts, show rainbow
    elif rain_active and rainbow_alpha < 1.0:
        rainbow_alpha += 0.005

    # Recycle raindrops
    rain_drops = [(x, y if y > -1.0 else random.uniform(0.8, 1.2)) for x, y in rain_drops]

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Sun-Rain-Rainbow Animation")
    init()
    glutDisplayFunc(display)
    glutTimerFunc(0, update, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()