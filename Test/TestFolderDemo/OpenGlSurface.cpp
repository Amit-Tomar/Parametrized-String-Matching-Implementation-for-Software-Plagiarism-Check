/**
 * @file    OpenGlSurface.cpp
 * @author  Amit Tomar
 * @version 1.0
 *
 * Class definitions for class OpenGlSurface
 */

#include "OpenGlSurface.h"
#include "MathHelper.h"

/*
 * Constructor
 *
 * @param  x X coordinate of left-top corner of widget
 * @param  y Y coordinate of left-top corner of widget
 * @param  width Width of widget
 * @param  height Height of widget
 * @param  parent Pointer to parent widget
 */
OpenGlSurface::OpenGlSurface(int x , int y, int width, int height, QGLWidget *parent)
    : QGLWidget(QGLFormat(QGL::SampleBuffers), parent)
{
    setFormat(QGLFormat(QGL::DoubleBuffer | QGL::DepthBuffer));
    setGeometry(x,y,width,height);
    scale = 1;
    translateX = 0 ;
    translateY = 0 ;
    useBernsteinAlgo = true ;
    rotationAxisX    = false;
    rotationAxisY    = false;
    rotationAxisZ    = false;
    update();
    initializeGL();
    paintGL();
}


/*
 * Sets the usage of Bernstein algo for drawing
 *
 * @param  flag Tells to use or not use Bernstein algo
 */
void OpenGlSurface::setDrawingAlgoBernstein(bool flag)
{
    useBernsteinAlgo = flag;
}


/*
 * Draws the list of points on screen.
 *
 * @param  pointsList Vector of points to draw.
 * @param  red Red color % to use in drawing
 * @param  green Green color % to use in drawing
 * @param  blue Red Blue % to use in drawing
 * @param  thickness Thickness of pixels to use in drawing
 */
void OpenGlSurface::drawPointsList(std::vector<std::pair<GLfloat, GLfloat> > pointsList , GLfloat red, GLfloat green, GLfloat blue, GLfloat thickness)
{
    glPointSize(thickness);
    glBegin(GL_POINTS);
        glColor3f(red,green,blue);
        glEnable(GL_POINT_SMOOTH);
        for( int i = 0 ; i < pointsList.size() ; ++i )
        {
            glVertex3f(  pointsList[i].first,pointsList[i].second,0);
        }
    glEnd();
    update();
}



/*
 * Draws the open polygon from a list of points on screen.
 *
 * @param  curvePoints Vector of points to draw open polygon from.
 * @param  red Red color % to use in drawing
 * @param  green Green color % to use in drawing
 * @param  blue Red Blue % to use in drawing
 * @param  thickness Thickness of pixels to use in drawing
 */
void OpenGlSurface::drawPolygon(std::vector<std::pair<GLfloat , GLfloat> > curvePoints, GLfloat red, GLfloat green, GLfloat blue, GLfloat thickness)
{
    if( controlPointsList.size() > 1 )
    {
        glPointSize(thickness);
        glBegin(GL_POINTS);
            glColor3f(red,green,blue);
            glEnable(GL_POINT_SMOOTH);
            for( int i = 0 ; i < curvePointsList.size() ; ++i )
            {
                glVertex3f(  curvePointsList[i].first,curvePointsList[i].second,0);
            }
        glEnd();
    }
    update();
}


/*
 * Initializes openGL related entities.
 */
void OpenGlSurface::initializeGL()
{
    glClearColor(.15,.15,.15,1);
    glMatrixMode(GL_PROJECTION);
    glEnable(GL_POINT_SMOOTH);
    glLoadIdentity();
    glOrtho(0,1,0,1,-1,1);
    update();
}

/*
 * Overriden from OpenGlWidget, gets called on repaint events
 */
void OpenGlSurface::paintGL()
{
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(0,1,0,1,-1,1);
    draw();
    update();
}

/*
 * Overriden from OpenGlWidget, gets called on widget resize events.
 *
 * @param  width New width of the widget
 * @param  height New Height of the widget
 */
void OpenGlSurface::resizeGL(int width, int height)
{
    glViewport(0, 0, width , height );
    viewPortWidth = width ;
    viewPortHeight = height;
    update();
}

/*
 * Overriden from OpenGlWidget, gets called on mouse events.
 *
 * @param  event Pointer to the event object containing all mouse event related information.
 */
void OpenGlSurface::mousePressEvent(QMouseEvent *event)
{
    std::pair<GLfloat,GLfloat> pointClicked( (event->x()) / (float) viewPortWidth , (viewPortHeight-event->y()) / (float)viewPortHeight );
    controlPointsList.push_back(pointClicked);

    curvePointsList.clear();

    // Use Berstein Algorithm for storing points
    if( true == useBernsteinAlgo )
    {
        for( float t = 0 ; t <= 1 ; t += .0001 )
        {
            float x = 0.0;
            float y = 0.0;

            for( int i = 0 ; i < controlPointsList.size() ; ++i )
            {
                x += nCr( controlPointsList.size()-1, i ) * pow(1-t, controlPointsList.size()-1-i) * pow(t, i) * controlPointsList[i].first ;
                y += nCr( controlPointsList.size()-1, i ) * pow(1-t, controlPointsList.size()-1-i) * pow(t, i) * controlPointsList[i].second ;

            }

            std::pair<GLfloat,GLfloat > tempPoint( x,y );
            curvePointsList.push_back(tempPoint);
        }
    }

    // Use De Casteljau Algorithm for storing points
    else
    {
        for( float t = 0 ; t <= 1 ; t+= .0001 )
        {
             std::vector<std::pair<GLfloat,GLfloat> > temp ;
             for( int i = 0 ; i < controlPointsList.size() ; ++ i )
                    temp.push_back(controlPointsList[i]);

              for ( int k = 1 ; k < controlPointsList.size() ; ++ k)
              {
                    for ( int i = 0 ; i <= controlPointsList.size()-k ; ++ i )
                    {
                        temp[i].first  = ((1-t) * temp[i].first  ) + (t * temp[i+1].first)  ;
                        temp[i].second = ((1-t) * temp[i].second ) + (t * temp[i+1].second) ;
                    }
              }

              curvePointsList.push_back(temp[0]);
        }
    }

    update();
}

/*
 * Write necessary drawing code in this function.
 */
void OpenGlSurface::draw()
{
    glTranslatef(translateX,translateY,0);
    glScalef(scale,scale,1);
    glRotatef(angle,rotationAxisX,rotationAxisY,rotationAxisZ);

    // Draw Control Points
    drawPointsList(controlPointsList,1,0,0,4);

    // Draw curve
    if( true == useBernsteinAlgo )
        drawPolygon(controlPointsList,1,.5,0,1);
    else
        drawPolygon(controlPointsList,.5,.5,0,1);

    update();
}

/*
 * Sets scale to use
 * @param  scale scale value to use
 */
void OpenGlSurface::setScale(int newScale)
{
    scale = 1 + (newScale*.01);
    glScalef(scale,scale,1);
    update();
}

/*
 * Sets rotation angle to use
 * @param  axis axis to rotate about
 * @param  newAngle angle to rotate with
 */
void OpenGlSurface::setRotation(int axis, int newAngle)
{
    if( 0 == axis )
    {
        rotationAxisX = true  ;
        rotationAxisY = false ;
        rotationAxisZ = false ;
    }

    else if( 1 == axis )
    {
        rotationAxisX = false  ;
        rotationAxisY = true   ;
        rotationAxisZ = false  ;
    }

    else
    {
        rotationAxisX = false  ;
        rotationAxisY = false  ;
        rotationAxisZ = true   ;
    }

    angle = newAngle;
    update();
}

/*
 * Sets transaltion value in x direction
 * @param  distance value to translate with
 */
void OpenGlSurface::setTranslateX(int distance)
{
    distance -= 50;
    distance *= 10;
    translateX = (float)distance / viewPortWidth;
    update();
}

/*
 * Sets transaltion value in y direction
 * @param  distance value to translate with
 */
void OpenGlSurface::setTranslateY(int distance)
{
    distance -= 50;
    distance *= 10;
    translateY = (float)distance / viewPortHeight;
    update();
}
