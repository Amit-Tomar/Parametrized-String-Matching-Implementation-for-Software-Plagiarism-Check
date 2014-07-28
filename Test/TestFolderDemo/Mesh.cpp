#include "Mesh.h"

Mesh::Mesh()
{
    numberOfFaces    = 0;
    numberOfVertices = 0;
    subdivisionLevel = 0;
    selectedControlMeshVertex = 0;
    parsedOnce = false;
}

void Mesh::printMeshInformation()
{
    std::cout << "-------------- Mesh Information ---------------" << std::endl ;
    std::cout << "Total Faces    : " << totalFaces()   << std::endl ;
    std::cout << "Total Vertices : " << totalVertices() << std::endl ;

    for( int i = 0 ; i < totalFaces() ; ++ i )
    {
        std::cout << "Face " << i << " : " ;

        for( int j = 0 ; j < faceList[i].getBoundingVerticesList().size() ; ++j  )
        {
             std::cout << faceList[i].getBoundingVerticesList()[j] << " " ;
        }

        std::cout << "Neighboring Faces : " ;

        for( int j = 0 ; j < faceList[i].getNeighborFacesList().size() ; ++ j )
        {
            std::cout << " " <<  faceList[i].getNeighborFacesList()[j];
        }

        std::cout << std::endl ;
    }

    std::cout << "-----------------------------------------------" << std::endl ;

    for( int i = 0 ; i < totalVertices() ; ++ i )
    {
        std::cout << "Vertex " << i << " : Faces : " ;

        for( int j = 0 ; j < vertexList[i].getFacesVertexBelongToList().size() ; ++j  )
        {
             std::cout << vertexList[i].getFacesVertexBelongToList()[j] << " ";
        }
        std::cout << std::endl ;
    }

    std::cout << "-----------------------------------------------" << std::endl ;

}

bool Mesh::areFacesNeighbors(Face face1, Face face2)
{
    unsigned int count = 0 ;
    for( int i =0 ; i < face1.getBoundingVerticesList().size() ; ++ i )
    {
        if(std::find(face2.getBoundingVerticesList().begin(), face2.getBoundingVerticesList().end(), face1.getBoundingVerticesList()[i]) != face2.getBoundingVerticesList().end())
        {
            ++ count;
        }
    }

    if( count >= 2 )
        return true;
    else
        return false;
}

void Mesh::subdivideByLoop()
{
    ++ subdivisionLevel;
    std::vector<Vertex>::iterator vertexListIterator;
    std::vector<Edge>::iterator edgeListIterator;

    std::vector<Vertex> newVerticesList;
    std::vector<Face> newFacesList;
    std::vector<Edge> subdividedEdgesList;

    for(unsigned int i = 0 ; i < faceList.size() ; ++i )
    {
       int vNumber1 = faceList[i].getBoundingVerticesList()[0];
       int vNumber2 = faceList[i].getBoundingVerticesList()[1];
       int vNumber3 = faceList[i].getBoundingVerticesList()[2];

       Vertex *newV1 ;
       Vertex *newV2 ;
       Vertex *newV3 ;

       Vertex * newVertex4;
       Vertex * newVertex5;
       Vertex * newVertex6;

       Edge edge1(vNumber1,vNumber2);
       Edge edge2(vNumber2,vNumber3);
       Edge edge3(vNumber1,vNumber3);

       int oppositeVertexNumberInNeighbor;

       double v1X;
       double v1Y;
       double v1Z;

       for(unsigned int j = 0 ; j < faceList[i].getNeighborFacesList().size() ; ++ j )
       {
            if( faceList[faceList[i].getNeighborFacesList()[j]].hasEdge(edge1) )
            {
                edgeListIterator = std::find(subdividedEdgesList.begin(), subdividedEdgesList.end(), edge1 ) ;
                if( edgeListIterator == subdividedEdgesList.end())
                {
                    oppositeVertexNumberInNeighbor =  faceList[faceList[i].getNeighborFacesList()[j]].vertexOppositeToEdge(edge1);

                    v1X = (1.0/8.0 * (vertexList[vNumber3].X() + vertexList[oppositeVertexNumberInNeighbor].X())) + ( 3.0/8.0 * (vertexList[vNumber1].X() + vertexList[vNumber2].X()) );
                    v1Y = (1.0/8.0 * (vertexList[vNumber3].Y() + vertexList[oppositeVertexNumberInNeighbor].Y())) + ( 3.0/8.0 * (vertexList[vNumber1].Y() + vertexList[vNumber2].Y()) );
                    v1Z = (1.0/8.0 * (vertexList[vNumber3].Z() + vertexList[oppositeVertexNumberInNeighbor].Z())) + ( 3.0/8.0 * (vertexList[vNumber1].Z() + vertexList[vNumber2].Z()) );

                    newVertex4 = new Vertex ( v1X , v1Y , v1Z );
                    edge1.getSubDividedVertex() = *newVertex4;
                    subdividedEdgesList.push_back(edge1);
                }

                else
                {
                    newVertex4 = new Vertex ( (*edgeListIterator).getSubDividedVertex().X(),(*edgeListIterator).getSubDividedVertex().Y(),(*edgeListIterator).getSubDividedVertex().Z() );
                }
            }



            else if( faceList[faceList[i].getNeighborFacesList()[j]].hasEdge(edge2) )
            {
                edgeListIterator = std::find(subdividedEdgesList.begin(), subdividedEdgesList.end(), edge2 ) ;
                if( edgeListIterator == subdividedEdgesList.end())
                {
                    oppositeVertexNumberInNeighbor =  faceList[faceList[i].getNeighborFacesList()[j]].vertexOppositeToEdge(edge2);

                    v1X = (1.0/8.0 * (vertexList[vNumber1].X() + vertexList[oppositeVertexNumberInNeighbor].X())) + ( 3.0/8.0 * (vertexList[vNumber3].X() + vertexList[vNumber2].X()) );
                    v1Y = (1.0/8.0 * (vertexList[vNumber1].Y() + vertexList[oppositeVertexNumberInNeighbor].Y())) + ( 3.0/8.0 * (vertexList[vNumber3].Y() + vertexList[vNumber2].Y()) );
                    v1Z = (1.0/8.0 * (vertexList[vNumber1].Z() + vertexList[oppositeVertexNumberInNeighbor].Z())) + ( 3.0/8.0 * (vertexList[vNumber3].Z() + vertexList[vNumber2].Z()) );

                    newVertex5 = new Vertex ( v1X , v1Y , v1Z );
                    edge2.getSubDividedVertex() = *newVertex5;
                    subdividedEdgesList.push_back(edge2);
                }

                else
                {
                    newVertex5 = new Vertex ( (*edgeListIterator).getSubDividedVertex().X(),(*edgeListIterator).getSubDividedVertex().Y(),(*edgeListIterator).getSubDividedVertex().Z() );
                }
            }

            else if( faceList[faceList[i].getNeighborFacesList()[j]].hasEdge(edge3) )
            {
                edgeListIterator = std::find(subdividedEdgesList.begin(), subdividedEdgesList.end(), edge3 ) ;
                if( edgeListIterator == subdividedEdgesList.end())
                {
                    oppositeVertexNumberInNeighbor =  faceList[faceList[i].getNeighborFacesList()[j]].vertexOppositeToEdge(edge3);

                    v1X = (1.0/8.0 * (vertexList[vNumber2].X() + vertexList[oppositeVertexNumberInNeighbor].X())) + ( 3.0/8.0 * (vertexList[vNumber1].X() + vertexList[vNumber3].X()) );
                    v1Y = (1.0/8.0 * (vertexList[vNumber2].Y() + vertexList[oppositeVertexNumberInNeighbor].Y())) + ( 3.0/8.0 * (vertexList[vNumber1].Y() + vertexList[vNumber3].Y()) );
                    v1Z = (1.0/8.0 * (vertexList[vNumber2].Z() + vertexList[oppositeVertexNumberInNeighbor].Z())) + ( 3.0/8.0 * (vertexList[vNumber1].Z() + vertexList[vNumber3].Z()) );

                    newVertex6 = new Vertex ( v1X , v1Y , v1Z );
                    edge3.getSubDividedVertex() = *newVertex6;
                    subdividedEdgesList.push_back(edge3);
                }

                else
                {
                    newVertex6 = new Vertex ( (*edgeListIterator).getSubDividedVertex().X(),(*edgeListIterator).getSubDividedVertex().Y(),(*edgeListIterator).getSubDividedVertex().Z() );
                }
            }

            else
            {
                std::cerr << "Not possible" << std::endl ;
            }

      }

       // Find new coordiantes even

       double beta1 = 0.0 ;
       double beta2 = 0.0 ;
       double beta3 = 0.0 ;

       // beta 1
       if( 3 == vertexList[vNumber1].getNeighboringVerticesList().size() )
       {
           beta1 = 3.0 / 16.0;
       }

       else
       {
           beta1 = 3.0 / ( 8.0 * vertexList[vNumber1].getNeighboringVerticesList().size() );
       }

       // beta 2
       if( 3 == vertexList[vNumber2].getNeighboringVerticesList().size() )
       {
           beta2 = 3.0 / 16.0;
       }

       else
       {
           beta2 = 3.0 / ( 8.0 * vertexList[vNumber2].getNeighboringVerticesList().size() );
       }

       // beta 3
       if( 3 == vertexList[vNumber3].getNeighboringVerticesList().size() )
       {
           beta3 = 3.0 / 16.0;
       }

       else
       {
           beta3 = 3.0 / ( 8.0 * vertexList[vNumber3].getNeighboringVerticesList().size() );
       }

       // Cal even vertex 1

       double vX = 0.0, vY = 0.0, vZ = 0.0;

       for(unsigned int i = 0 ; i < vertexList[vNumber1].getNeighboringVerticesList().size() ; ++ i )
       {
           vX += vertexList[vertexList[vNumber1].getNeighboringVerticesList()[i]].X();
           vY += vertexList[vertexList[vNumber1].getNeighboringVerticesList()[i]].Y();
           vZ += vertexList[vertexList[vNumber1].getNeighboringVerticesList()[i]].Z();
       }

       vX *=  beta1 ;
       vX +=  (1.0- ( vertexList[vNumber1].getNeighboringVerticesList().size() * beta1)) * vertexList[vNumber1].X();

       vY *=  beta1 ;
       vY +=  (1.0- ( vertexList[vNumber1].getNeighboringVerticesList().size() * beta1)) * vertexList[vNumber1].Y();

       vZ *=  beta1 ;
       vZ +=  (1.0- ( vertexList[vNumber1].getNeighboringVerticesList().size() * beta1)) * vertexList[vNumber1].Z();

       newV1 = new Vertex( vX, vY, vZ );


       // Cal even vertex 2

       vX = 0.0; vY = 0.0; vZ = 0.0;

       for(unsigned int i = 0 ; i < vertexList[vNumber2].getNeighboringVerticesList().size() ; ++ i )
       {
           vX += vertexList[vertexList[vNumber2].getNeighboringVerticesList()[i]].X();
           vY += vertexList[vertexList[vNumber2].getNeighboringVerticesList()[i]].Y();
           vZ += vertexList[vertexList[vNumber2].getNeighboringVerticesList()[i]].Z();
       }

       vX *=  beta2 ;
       vX +=  (1.0- ( vertexList[vNumber2].getNeighboringVerticesList().size() * beta2)) * vertexList[vNumber2].X();

       vY *=  beta2 ;
       vY +=  (1.0- ( vertexList[vNumber2].getNeighboringVerticesList().size() * beta2)) * vertexList[vNumber2].Y();

       vZ *=  beta2 ;
       vZ +=  (1.0- ( vertexList[vNumber2].getNeighboringVerticesList().size() * beta2)) * vertexList[vNumber2].Z();

       newV2 = new Vertex( vX, vY, vZ );

       // Cal even vertex 3

       vX = 0.0; vY = 0.0; vZ = 0.0;


       for( unsigned int i = 0 ; i < vertexList[vNumber3].getNeighboringVerticesList().size() ; ++ i )
       {
           vX += vertexList[vertexList[vNumber3].getNeighboringVerticesList()[i]].X();
           vY += vertexList[vertexList[vNumber3].getNeighboringVerticesList()[i]].Y();
           vZ += vertexList[vertexList[vNumber3].getNeighboringVerticesList()[i]].Z();
       }

       vX *=  beta3 ;
       vX +=  (1.0- ( vertexList[vNumber3].getNeighboringVerticesList().size() * beta3)) * vertexList[vNumber3].X();

       vY *=  beta3 ;
       vY +=  (1.0- ( vertexList[vNumber3].getNeighboringVerticesList().size() * beta3)) * vertexList[vNumber3].Y();

       vZ *=  beta3 ;
       vZ +=  (1.0- ( vertexList[vNumber3].getNeighboringVerticesList().size() * beta3)) * vertexList[vNumber3].Z();

       newV3 = new Vertex( vX, vY, vZ );

       vertexListIterator = std::find(newVerticesList.begin(), newVerticesList.end(), *newV1 ) ;
       if( vertexListIterator == newVerticesList.end())
       {
            newVerticesList.push_back(*newV1);
       }

       vertexListIterator = std::find(newVerticesList.begin(), newVerticesList.end(), *newV2 ) ;
       if( vertexListIterator == newVerticesList.end())
       {
            newVerticesList.push_back(*newV2);
       }

       vertexListIterator = std::find(newVerticesList.begin(), newVerticesList.end(), *newV3 ) ;
       if( vertexListIterator == newVerticesList.end())
       {
            newVerticesList.push_back(*newV3);
       }

       vertexListIterator = std::find(newVerticesList.begin(), newVerticesList.end(), *newVertex4 ) ;
       if( vertexListIterator == newVerticesList.end())
       {
            newVerticesList.push_back(*newVertex4);
       }

       vertexListIterator = std::find(newVerticesList.begin(), newVerticesList.end(), *newVertex5 ) ;
       if( vertexListIterator == newVerticesList.end())
       {
            newVerticesList.push_back(*newVertex5);
       }

       vertexListIterator = std::find(newVerticesList.begin(), newVerticesList.end(), *newVertex6 ) ;
       if( vertexListIterator == newVerticesList.end())
       {
            newVerticesList.push_back(*newVertex6);
       }


       Face objFace1;

       int pos1 = findVertexPosition(newVerticesList,*newV1);
       int pos2 = findVertexPosition(newVerticesList,*newV2);
       int pos3 = findVertexPosition(newVerticesList,*newV3);
       int pos4 = findVertexPosition(newVerticesList,*newVertex4);
       int pos5 = findVertexPosition(newVerticesList,*newVertex5);
       int pos6 = findVertexPosition(newVerticesList,*newVertex6);


       objFace1.getBoundingVerticesList().push_back(pos1);
       objFace1.getBoundingVerticesList().push_back(pos4);
       objFace1.getBoundingVerticesList().push_back(pos6);

       newFacesList.push_back(objFace1);

       newVerticesList[pos1].getNeighboringVerticesList().push_back(pos4);
       newVerticesList[pos1].getNeighboringVerticesList().push_back(pos6);
       newVerticesList[pos4].getNeighboringVerticesList().push_back(pos1);
       newVerticesList[pos4].getNeighboringVerticesList().push_back(pos6);
       newVerticesList[pos6].getNeighboringVerticesList().push_back(pos4);
       newVerticesList[pos6].getNeighboringVerticesList().push_back(pos1);

       Face objFace2;

       objFace2.getBoundingVerticesList().push_back(pos2);
       objFace2.getBoundingVerticesList().push_back(pos4);
       objFace2.getBoundingVerticesList().push_back(pos5);

       newFacesList.push_back(objFace2);

       newVerticesList[pos2].getNeighboringVerticesList().push_back(pos4);
       newVerticesList[pos2].getNeighboringVerticesList().push_back(pos5);
       newVerticesList[pos4].getNeighboringVerticesList().push_back(pos2);
       newVerticesList[pos4].getNeighboringVerticesList().push_back(pos5);
       newVerticesList[pos5].getNeighboringVerticesList().push_back(pos2);
       newVerticesList[pos5].getNeighboringVerticesList().push_back(pos1);

       Face objFace3;

       objFace3.getBoundingVerticesList().push_back(pos3);
       objFace3.getBoundingVerticesList().push_back(pos5);
       objFace3.getBoundingVerticesList().push_back(pos6);

       newFacesList.push_back(objFace3);

       newVerticesList[pos3].getNeighboringVerticesList().push_back(pos5);
       newVerticesList[pos3].getNeighboringVerticesList().push_back(pos6);
       newVerticesList[pos5].getNeighboringVerticesList().push_back(pos3);
       newVerticesList[pos5].getNeighboringVerticesList().push_back(pos6);
       newVerticesList[pos6].getNeighboringVerticesList().push_back(pos3);
       newVerticesList[pos6].getNeighboringVerticesList().push_back(pos5);

       Face objFace4;

       objFace4.getBoundingVerticesList().push_back(pos4);
       objFace4.getBoundingVerticesList().push_back(pos5);
       objFace4.getBoundingVerticesList().push_back(pos6);

       newFacesList.push_back(objFace4);

       newVerticesList[pos5].getNeighboringVerticesList().push_back(pos4);
       newVerticesList[pos5].getNeighboringVerticesList().push_back(pos6);
       newVerticesList[pos4].getNeighboringVerticesList().push_back(pos5);
       newVerticesList[pos4].getNeighboringVerticesList().push_back(pos6);
       newVerticesList[pos6].getNeighboringVerticesList().push_back(pos4);
       newVerticesList[pos6].getNeighboringVerticesList().push_back(pos5);

       delete newV1;
       delete newV2;
       delete newV3;
       delete newVertex4;
       delete newVertex5;
       delete newVertex6;

    }

    vertexList.clear();
    faceList.clear();

    for(unsigned int i = 0 ; i < newVerticesList.size() ; ++ i )
        vertexList.push_back(newVerticesList[i]);
    for(unsigned int j = 0 ; j < newFacesList.size() ; ++ j )
        faceList.push_back(newFacesList[j]);

    numberOfVertices = vertexList.size();
    numberOfFaces    = faceList.size();

    // Fill the neighboring faces information in face list
    for(unsigned int i = 0 ; i < faceList.size() ; ++ i)
    {
        for(unsigned int j = 0 ; j < faceList.size() ; ++ j )
        {
            if( i != j && areFacesNeighbors( getFaceList()[i],  getFaceList()[j]))
            {
                getFaceList()[i].getNeighborFacesList().push_back(j);
            }
        }
    }

    // Fill the face information in vertex list
    for(unsigned int i = 0 ; i < totalFaces() ; ++ i)
    {
        for(unsigned int j = 0 ; j < getFaceList()[i].getBoundingVerticesList().size() ; ++ j )
        {
            unsigned int vertexNumber = getFaceList()[i].getBoundingVerticesList()[j] ;
            getVertexList()[vertexNumber].getFacesVertexBelongToList().push_back(i);
        }
    }
}

int Mesh::findVertexPosition(std::vector<Vertex> &verList , Vertex ver)
{
    for(unsigned int i = 0 ; i < verList.size() ; ++ i )
    {
        if(verList[i] == ver)
        {
            return i;
        }
    }

    std::cerr << "Error :::::: Vertex not found" << std::endl;
    return -1;
}

void Mesh::reset()
{
    vertexList.clear();
    faceList.clear();
}
