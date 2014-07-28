#include <QtWidgets>
#include <QtOpenGL>

#include <math.h>

#include "GLRenderer.h"

#ifndef GL_MULTISAMPLE
#define GL_MULTISAMPLE  0x809D
#endif

GLRenderer::GLRenderer(QWidget *parent)
    : QGLWidget(QGLFormat(QGL::SampleBuffers), parent)
{
    xRot = 0;
    yRot = 0;
    zRot = 0;

    qtGreen = QColor::fromCmykF(0.40, 0.0, 1.0, 0.0);
    qtPurple = QColor::fromCmykF(0.39, 0.39, 0.0, 0.0);
    setFocusPolicy(Qt::ClickFocus);

    scale = 3 ;
    translateX = 0 ;
    translateY = -.1 ;
    translateZ = 0 ;
    lightPositionX = 1.0 ;
    lightPositionY = 1.0 ;
    lightPositionZ = 1.0 ;
    lightMovementEnabled = false ;
}

GLRenderer::~GLRenderer()
{
}

QSize GLRenderer::minimumSizeHint() const
{
    return QSize(50, 50);
}

QSize GLRenderer::sizeHint() const
{
    return QSize(400, 400);
}

static void qNormalizeAngle(int &angle)
{
    while (angle < 0)
        angle += 360 * 16;
    while (angle > 360 * 16)
        angle -= 360 * 16;
}

void GLRenderer::setXRotation(int angle)
{
    qNormalizeAngle(angle);
    if (angle != xRot) {
        xRot = angle;
        emit xRotationChanged(angle);
        updateGL();
    }
}

void GLRenderer::setYRotation(int angle)
{
    qNormalizeAngle(angle);
    if (angle != yRot) {
        yRot = angle;
        emit yRotationChanged(angle);
        updateGL();
    }
}

void GLRenderer::setZRotation(int angle)
{
    qNormalizeAngle(angle);
    if (angle != zRot) {
        zRot = angle;
        emit zRotationChanged(angle);
        updateGL();
    }
}

void GLRenderer::initializeGL()
{
    qglClearColor(qtPurple.dark());
    glEnable(GL_DEPTH_TEST);
    glEnable(GL_CULL_FACE);
    glShadeModel(GL_SMOOTH);
    glEnable(GL_LIGHTING);
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST);
    glEnable(GL_MULTISAMPLE);
    glEnable(GL_LIGHT0);
}

void GLRenderer::paintGL()
{
    // Set light
    GLfloat light_position[] = { lightPositionX, lightPositionY, lightPositionZ, 0.0 };
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glEnable(GL_NORMALIZE);

    glLoadIdentity();

    if( !lightMovementEnabled )
        glLightfv(GL_LIGHT0, GL_POSITION, light_position);

    glTranslatef( 0.0, 0.0, -10.0);

    /* Normal Rotation
    glRotatef(xRot / 16.0, 1.0, 0.0, 0.0);
    glRotatef(yRot / 16.0, 0.0, 1.0, 0.0);
    glRotatef(zRot / 16.0, 0.0, 0.0, 1.0); */

    // Rotation by Quaternions

    QMatrix4x4 matrix;

    quaternion.rotateX(xRot);
    matrix.rotate(quaternion.getQuaternion());
    glMultMatrixf(matrix.constData());

    quaternion.rotateY(yRot);
    matrix.rotate(quaternion.getQuaternion());
    glMultMatrixf(matrix.constData());

    quaternion.rotateZ(zRot);
    matrix.rotate(quaternion.getQuaternion());
    glMultMatrixf(matrix.constData());

    glScalef(scale,scale,scale);
    glTranslatef(translateX,translateY,translateZ);

    if( lightMovementEnabled )
        glLightfv(GL_LIGHT0, GL_POSITION, light_position);

    float color[] = { 1.0f, 1.0f, 1.0f, 1.0f };
    glEnable(GL_COLOR_MATERIAL);
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, color);
    glBegin(GL_TRIANGLES);

    if(false)
    {
        for( int i = 0 ; i < objPLYParser.g_vpX.size() ; ++i )
        {
            if( objPLYParser.g_vnX.size() > 0 )
                glNormal3f(objPLYParser.g_vnX[i],objPLYParser.g_vnY[i],objPLYParser.g_vnZ[i]);
            else
            {
                glNormal3f(objPLYParser.g_vpX[i],objPLYParser.g_vpY[i],objPLYParser.g_vpZ[i]);
            }

            glVertex3f(objPLYParser.g_vpX[i],objPLYParser.g_vpY[i],objPLYParser.g_vpZ[i]);
        }
    }

    else
    {
        for( int i = 0 ; i < objPLYParser.g_vpX.size() ; i+=3 )
        {
            if( objPLYParser.g_vnX.size() > 0 )
                glNormal3f(objPLYParser.g_vnX[i],objPLYParser.g_vnY[i],objPLYParser.g_vnZ[i]);
            else
            {
                float vector1[3], vector2[3], vCross[3], normalizationValue;
                vector1[0] = objPLYParser.g_vpX[i] - objPLYParser.g_vpX[i+1];
                vector1[1] = objPLYParser.g_vpY[i] - objPLYParser.g_vpY[i+1];
                vector1[2] = objPLYParser.g_vpZ[i] - objPLYParser.g_vpZ[i+1];

                vector2[0] = objPLYParser.g_vpX[i] - objPLYParser.g_vpX[i+2];
                vector2[1] = objPLYParser.g_vpY[i] - objPLYParser.g_vpY[i+2];
                vector2[2] = objPLYParser.g_vpZ[i] - objPLYParser.g_vpZ[i+2];

                // Cross product
                vCross[0] = vector1[1] * vector2[2] - vector2[1] * vector1[2];
                vCross[1] = vector2[0] * vector1[2] - vector1[0] * vector2[2];
                vCross[2] = vector1[0] * vector2[1] - vector2[0] * vector1[1];

                // Value to do normalization with
                normalizationValue = sqrt( vCross[0]*vCross[0] + vCross[1]*vCross[1] + vCross[2]*vCross[2] );

                 float normal[3];
                 normal[0] = vCross[0]/normalizationValue;
                 normal[1] = vCross[1]/normalizationValue;
                 normal[2] = vCross[2]/normalizationValue;

                 glNormal3f(normal[0],normal[1],normal[2]);
            }

            glVertex3f(objPLYParser.g_vpX[i],objPLYParser.g_vpY[i],objPLYParser.g_vpZ[i]);
            glVertex3f(objPLYParser.g_vpX[i+1],objPLYParser.g_vpY[i+1],objPLYParser.g_vpZ[i+1]);
            glVertex3f(objPLYParser.g_vpX[i+2],objPLYParser.g_vpY[i+2],objPLYParser.g_vpZ[i+2]);
        }
    }

    glEnd();

    //glutSolidCone(.05,.15,22,22);

}

void GLRenderer::resizeGL(int width, int height)
{
    int side = qMin(width, height);
    glViewport((width - side) / 2, (height - side) / 2, side, side);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
#ifdef QT_OPENGL_ES_1
    glOrthof(-0.5, +0.5, -0.5, +0.5, 4.0, 15.0);
#else
    glOrtho(-0.5, +0.5, -0.5, +0.5, 4.0, 15.0);
#endif
    glMatrixMode(GL_MODELVIEW);
}

void GLRenderer::mousePressEvent(QMouseEvent *event)
{
    lastPos = event->pos();
}

void GLRenderer::keyPressEvent(QKeyEvent *keyevent)
{
    // Scale
    if( keyevent->key() == Qt::Key_P )
    {
        scale += .05;
    }

    else if( keyevent->key() == Qt::Key_Semicolon )
    {
        scale -= .05;
    }

    // Translation of object
    else if( keyevent->key() == Qt::Key_W )
    {
        translateY += .005 ;
    }

    else if( keyevent->key() == Qt::Key_A )
    {
        translateX -= .005 ;
    }

    else if( keyevent->key() == Qt::Key_D )
    {
        translateX += .005 ;
    }

    else if( keyevent->key() == Qt::Key_S )
    {
        translateY -= .005 ;
    }

    // Rotation of object
    else if( keyevent->key() == Qt::Key_T )
    {
        xRot += 15 ;
    }

    else if( keyevent->key() == Qt::Key_F )
    {
        yRot -= 15 ;
    }

    else if( keyevent->key() == Qt::Key_G )
    {
        xRot -= 15 ;
    }

    else if( keyevent->key() == Qt::Key_H )
    {
        yRot += 15 ;
    }


    // Translation of Light
    else if( keyevent->key() == Qt::Key_I )
    {
        lightPositionX += 1 ;
    }

    else if( keyevent->key() == Qt::Key_K )
    {
        lightPositionX -= 1; ;
    }

    else if( keyevent->key() == Qt::Key_L )
    {
        lightPositionY += 1 ;
    }

    else if( keyevent->key() == Qt::Key_J )
    {
        lightPositionY -= 1; ;
    }

    // Light movement enable/disable

    else if( keyevent->key() == Qt::Key_Q )
    {
       lightMovementEnabled = !lightMovementEnabled;
    }

    glDraw();
}

void GLRenderer::mouseMoveEvent(QMouseEvent *event)
{
    int dx = event->x() - lastPos.x();
    int dy = event->y() - lastPos.y();

    if (event->buttons() & Qt::LeftButton) {
        setXRotation(xRot + 8 * dy);
        setYRotation(yRot + 8 * dx);
    } else if (event->buttons() & Qt::RightButton) {
        setXRotation(xRot + 8 * dy);
        setZRotation(zRot + 8 * dx);
    }
    lastPos = event->pos();
}
