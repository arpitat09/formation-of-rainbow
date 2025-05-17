from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import math
import time

# Rainbow colors (VIBGYOR)
rainbow_colors = {
    "VIOLET": (148 / 255, 0, 211 / 255),
    "INDIGO": (75 / 255, 0, 130 / 255),
    "BLUE": (0, 0, 1),
    "GREEN": (0, 1, 0),
    "YELLOW": (1, 1, 0),
    "ORANGE": (1, 127 / 255, 0),
    "RED": (1, 0, 0)
}
color_order = list(rainbow_colors.keys())

# Global control variables
running = True
visible_color_count = 0
total_colors = len(color_order)
selected_color = "ALL"
angle = 0

def draw_cloud(x, y, scale):
    glColor3f(1.0, 1.0, 1.0)  # White color
    glPushMatrix()
    glTranslatef(x, y, 0)
    glScalef(scale, scale, 1)

    for cx, cy in [(-0.1, 0), (0, 0.05), (0.1, 0), (0.05, -0.02), (-0.05, -0.02)]:
        glBegin(GL_POLYGON)
        for angle in range(360):
            rad = math.radians(angle)
            glVertex2f(cx + 0.07 * math.cos(rad), cy + 0.07 * math.sin(rad))
        glEnd()
    glPopMatrix()
    
def draw_arc():
    global angle, visible_color_count
    base_radius = 0.5
    band_width = 0.05

    if running and visible_color_count < total_colors:
        visible_color_count += 1
        time.sleep(0.7)
        glutPostRedisplay()

    glPushMatrix()
    glTranslatef(0, -0.2, 0)
    glRotatef(angle, 0, 1, 0)

    for i, color_name in enumerate(color_order[:visible_color_count]):
        if selected_color != "ALL" and color_name != selected_color:
            continue

        inner_radius = base_radius + i * band_width
        outer_radius = inner_radius + band_width

        glColor3f(*rainbow_colors[color_name])
        glBegin(GL_TRIANGLE_STRIP)
        for theta in range(0, 181):
            rad = math.radians(theta)
            x_inner = math.cos(rad) * inner_radius
            y_inner = math.sin(rad) * inner_radius
            x_outer = math.cos(rad) * outer_radius
            y_outer = math.sin(rad) * outer_radius
            glVertex2f(x_outer, y_outer)
            glVertex2f(x_inner, y_inner)
        glEnd()

    glPopMatrix()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_cloud(-0.6, 0.6, 1.0)
    draw_cloud(0.5, 0.65, 0.8)
    draw_cloud(0.0, 0.75, 0.9)
    draw_arc()
    glutSwapBuffers()

def idle():
    glutPostRedisplay()

def menu_func(option):
    global running, visible_color_count, selected_color

    if option == 0:  # Stop
        running = False
    elif option == 1:  # Resume full
        running = True
    elif option == 2:  # Show only first color
        running = False
        visible_color_count = 1
    elif option == 3:  # Show only first 3 colors
        running = False
        visible_color_count = 3
    elif option == 4:  # VIOLET
        selected_color = "VIOLET"
    elif option == 5:  # INDIGO
        selected_color = "INDIGO"
    elif option == 6:  # BLUE
        selected_color = "BLUE"
    elif option == 7:  # GREEN
        selected_color = "GREEN"
    elif option == 8:  # YELLOW
        selected_color = "YELLOW"
    elif option == 9:  # ORANGE
        selected_color = "ORANGE"
    elif option == 10:  # RED
        selected_color = "RED"
    elif option == 11:  # Reset and resume
        visible_color_count = 0
        running = True

def create_menu():
    glutCreateMenu(menu_func)
    glutAddMenuEntry("Stop", 0)
    glutAddMenuEntry("Resume Full Rainbow", 1)
    glutAddMenuEntry("Show First 1 Color", 2)
    glutAddMenuEntry("Show First 3 Colors", 3)
    glutAddMenuEntry("Show VIOLET Only", 4)
    glutAddMenuEntry("Show INDIGO Only", 5)
    glutAddMenuEntry("Show BLUE Only", 6)
    glutAddMenuEntry("Show GREEN Only", 7)
    glutAddMenuEntry("Show YELLOW Only", 8)
    glutAddMenuEntry("Show ORANGE Only", 9)
    glutAddMenuEntry("Show RED Only", 10)
    glutAddMenuEntry("Reset and Restart", 11)
    glutAttachMenu(GLUT_RIGHT_BUTTON)

def init():
    glClearColor(0.678, 0.847, 0.902, 1.0)  # Light sky blue background
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Rainbow Formation with Pause/Resume")
    init()
    create_menu()
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()
