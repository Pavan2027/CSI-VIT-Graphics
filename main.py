import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import json

# Global variables
rotation_x = 0.0
rotation_y = 0.0

token = input("Enter token: ")

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glShadeModel(GL_SMOOTH)

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def draw_model(data, scale_factor):
    if token in data:
        for path in data[token][0]['paths']:
            glBegin(GL_LINE_STRIP)
            for i in range(0, len(path), 3):  # iterate by 3 to get x, y, z for each point
                glVertex3f(path[i] * scale_factor, path[i+1] * scale_factor, path[i+2] * scale_factor)
            glEnd()
    else:
        print("Invalid Token!")

def display():
    global rotation_x, rotation_y
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glTranslatef(0.0, 0.0, -10.0)

    # Apply rotation
    glRotatef(rotation_x, 1.0, 0.0, 0.0)
    glRotatef(rotation_y, 0.0, 1.0, 0.0)

    glColor3f(1.0, 1.0, 1.0)
    draw_model(data, 10)
    
    glutSwapBuffers()

def special_key_pressed(key, x, y):
    global rotation_x, rotation_y
    
    # Rotate model using arrow keys
    if key == GLUT_KEY_UP:
        rotation_x -= 5.0
    elif key == GLUT_KEY_DOWN:
        rotation_x += 5.0
    elif key == GLUT_KEY_LEFT:
        rotation_y -= 5.0
    elif key == GLUT_KEY_RIGHT:
        rotation_y += 5.0

    glutPostRedisplay()

def main():
    global data
    filename = 'data.json'
    data = json.load(open(filename, 'r'))

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b'3D Model Viewer')
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutSpecialFunc(special_key_pressed)  # Register special key callback
    glutMainLoop()

if __name__ == "__main__":
    main()