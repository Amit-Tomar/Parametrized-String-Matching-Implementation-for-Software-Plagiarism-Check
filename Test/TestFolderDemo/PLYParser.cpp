#include "PLYParser.h"

PLYParser::PLYParser()
{

}

void PLYParser::importFile(std::string sFilePath)
{
    const aiScene* scene = aiImportFile (sFilePath.c_str(), aiProcess_Triangulate); // TRIANGLES!

    if (!scene)
    {
        std::cerr << "ERROR: reading mesh %s\n" << sFilePath << std::endl;
        return;
    }

    printf ("  %i animations\n", scene->mNumAnimations);
    printf ("  %i cameras\n", scene->mNumCameras);
    printf ("  %i lights\n", scene->mNumLights);
    printf ("  %i materials\n", scene->mNumMaterials);
    printf ("  %i meshes\n", scene->mNumMeshes);
    printf ("  %i textures\n", scene->mNumTextures);

      for (unsigned int m_i = 0; m_i < scene->mNumMeshes; m_i++)
      {
          const aiMesh* mesh = scene->mMeshes[m_i];
          printf ("    %i vertices in mesh\n", mesh->mNumVertices);
          g_point_count = mesh->mNumVertices;
          for (unsigned int v_i = 0; v_i < mesh->mNumVertices; v_i++)
          {
            if (mesh->HasPositions ())
            {
              const aiVector3D* vp = &(mesh->mVertices[v_i]);
              //printf ("      vp %i (%f,%f,%f)\n", v_i, vp->x, vp->y, vp->z);
              g_vpX.push_back (vp->x);
              g_vpY.push_back (vp->y);
              g_vpZ.push_back (vp->z);
            }
            if (mesh->HasNormals ())
            {
              const aiVector3D* vn = &(mesh->mNormals[v_i]);
              //printf ("      vn %i (%f,%f,%f)\n", v_i, vn->x, vn->y, vn->z);
              g_vnX.push_back (vn->x);
              g_vnY.push_back (vn->y);
              g_vnZ.push_back (vn->z);
            }
            if (mesh->HasTextureCoords (0))
            {
              const aiVector3D* vt = &(mesh->mTextureCoords[0][v_i]);
              //printf ("      vt %i (%f,%f)\n", v_i, vt->x, vt->y);
              g_vt.push_back (vt->x);
              g_vt.push_back (vt->y);
            }
            if (mesh->HasTangentsAndBitangents ())
            {
              // NB: could store/print tangents here
            }

            if( mesh->HasFaces() )
            {
                const struct aiFace * vf = &(mesh->mFaces[m_i]);
                if (vf->mNumIndices == 3)
                {
                   //printf ("      vf (%u,%u,%u)\n", vf->mIndices[0],vf->mIndices[1], vf->mIndices[2]);
                }
            }
          }
        }

      std::cout << "Parsing over" << std::endl ;
}

void PLYParser::startParsing(std::string path)
{
    if(path.length() == 0)
        importFile( "../plyFiles/bunny.ply" );
    else
        importFile( path );
}
