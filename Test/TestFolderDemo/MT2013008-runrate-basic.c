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

        char buffer[SIZE];
        int  iRuns = 0;
        char cBallType;

        int iTotalRuns = 0;
        int iTotalValidBalls = 0;
        int iTotalPlayedBalls = 0;

        float iRunRate[SIZE];

        while ( NULL != fgets( buffer , SIZE , fileReadPointer) )
        {
            if( '\n' == buffer[0] )
            {
                break;
            }

            else
            {
                float fRuns;
                if ( 1 == sscanf( buffer, "%f", &fRuns ) )
                {
                    iRuns = fRuns ;

                    if( iRuns == fRuns )
                    {
                        if( iRuns <= 6 && iRuns >=0)
                        {
                            iTotalRuns += iRuns  ;
                            ++ iTotalValidBalls  ;

                            if( iTotalValidBalls == 0 )
                                iRunRate[iTotalPlayedBalls] = 0.0;

                            else
                                iRunRate[iTotalPlayedBalls] = (float)iTotalRuns / ( ((int)iTotalValidBalls/6) + (float)(iTotalValidBalls % 6 ) / 6 ) ;

                            ++ iTotalPlayedBalls ;

                            printf(" [%d] ", iRuns) ;
                        }
                    }
                }

                else if ( 2 == sscanf( buffer, "%c%f", &cBallType,  &fRuns ) )
                {

                    if ( 'W' == cBallType || 'N' == cBallType )
                    {
                        iRuns = fRuns ;

                        if( iRuns == fRuns )
                        {
                            if( iRuns != 0 )
                            {
                                iTotalRuns += iRuns  ;

                                if( 0 == iTotalValidBalls)
                                    iRunRate[iTotalPlayedBalls] = 0.0;
                                else
                                {
                                    iRunRate[iTotalPlayedBalls] = (float)iTotalRuns / ( ((int)iTotalValidBalls/6) + (float)(iTotalValidBalls % 6 ) / 6 ) ;
                                }

                                ++ iTotalPlayedBalls ;
                            }
                        }
                    }

                    else
                    {
                        puts("\nInvalid input format");
                    }

                }

                else
                {
                    puts("\nInvalid input format");
                }
            }
        }

        int  i;

        for ( i = 0 ; i < iTotalPlayedBalls ; ++i)
        {
            fprintf( fileWritePointer, "%.1f\n", iRunRate[i]);
        }

    return 0;
}
