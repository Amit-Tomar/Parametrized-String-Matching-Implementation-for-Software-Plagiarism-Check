#include "Edge.h"

Edge::Edge(int v1, int v2): subdividedVertex(0.0,0.0,0.0)
{
    this->v1 = v1;
    this->v2 = v2;
}

bool Edge::operator==(Edge rightEdge)
{
    if( (v1 == rightEdge.V1() && v2 == rightEdge.V2()) || (v1 == rightEdge.V2() && v2 == rightEdge.V1() ) )
        return true;
    else
        return false;
}
