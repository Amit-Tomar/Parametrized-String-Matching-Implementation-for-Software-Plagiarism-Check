#include "Quaternions.h"

Quaternions::Quaternions()
{
}

void Quaternions::rotateX(int xRot)
{
    QVector3D rotationAxisX(1,0,0);
    rotation = QQuaternion::fromAxisAndAngle(rotationAxisX, xRot/25);
}

void Quaternions::rotateY(int yRot)
{
    QVector3D rotationAxisY(0,1,0);
    rotation = QQuaternion::fromAxisAndAngle(rotationAxisY, yRot/25);
}

void Quaternions::rotateZ(int zRot)
{
    QVector3D rotationAxisZ(0,0,1);
    rotation = QQuaternion::fromAxisAndAngle(rotationAxisZ, zRot/25);
}

QQuaternion Quaternions::getQuaternion()
{
    return rotation;
}
