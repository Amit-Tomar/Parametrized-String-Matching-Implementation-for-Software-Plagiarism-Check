#include <stdio.h>

#define SIZE 1024

int main(int iArgCount, char * cInputArray[])
{

    if( !iArgCount > 2 )
    {
        puts("Error : No Input or output file name specified.");
        return 1;
    }

    FILE * fileReadPointer  = fopen ( cInputArray[1], "r" );
    FILE * fileWritePointer = fopen ( cInputArray[2], "w" );

    if( NULL == fileReadPointer )
    {
        puts("Error : File not opened for reading.");
        return 1;
    }

    int iHourFirst      = 0;
    int iHourNext       = 0;
    int iMinutesFirst   = 0;
    int iMinutesNext    = 0;

    char buffer[SIZE];
    int  elapsedTime[SIZE];
    int iInputCounter = 0;

    while ( NULL != fgets( buffer , SIZE , fileReadPointer) )
    {
        if( EOF == buffer[0] )
        {
            break;
        }

        else
        {
            if ( 2 == sscanf( buffer, "%d : %d", &iHourNext , &iMinutesNext ) )
            {
                if( (iHourNext >=0 && iMinutesNext >=0 && iHourNext <= 23 && iMinutesNext < 60) )
                {
                    int iminutesElapsed = (iHourNext * 60 + iMinutesNext) - (iHourFirst * 60 + iMinutesFirst)  ;

                    if( iminutesElapsed < 0 )
                        iminutesElapsed += 24*60;

                    iHourFirst = iHourNext ;
                    iMinutesFirst = iMinutesNext ;

                    elapsedTime[ iInputCounter ] = iminutesElapsed ;
                    ++ iInputCounter;
                }

                else
                {
                    //fprintf( fileWritePointer, "I1\n" );
                    //puts("\nInvalid hours/minutes input");
                }
            }

            else
            {
                //fprintf( fileWritePointer, "I2\n");
                //puts("\nInvalid input format");
            }


        }
    }

    int i;
    for ( i = 0 ; i < iInputCounter ; ++i  )
        fprintf( fileWritePointer, "%d\n", elapsedTime[i] );

    printf("\n\n");

    return 0;
}

