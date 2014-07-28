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

    if( NULL == fileWritePointer )
    {
        puts("Error : File not opened for writing.");
        return 1;
    }

       char buffer[SIZE];

       float fReal1 = 0.0;
       float fReal2 = 0.0;
       float fImag1 = 0.0;
       float fImag2 = 0.0;

       float fOutput[SIZE][2];
       int iInputCount=0;

       char cBraceLeft1,cBraceLeft2, cComma1, cComma2, cBraceRight1,cBraceRight2, cOperator;

       while ( NULL != fgets( buffer , SIZE , fileReadPointer) )
       {
           if( '\n' == buffer[0] )
           {
               break;
           }

           else
           {
               if ( 11 == sscanf( buffer, "%c %f %c %f %c %c %c %f %c %f %c", &cBraceLeft1 , &fReal1 , &cComma1, &fImag1 , &cBraceRight1 , &cOperator , &cBraceLeft2, &fReal2, &cComma2, &fImag2 , &cBraceRight2 ) )
               {
                   if( '(' == cBraceLeft1 && '(' == cBraceLeft2 && ')' == cBraceRight1 && ')' == cBraceRight2 && ',' == cComma1 && ',' == cComma2)
                   {
                        float real , imag ;

                        if( '+' == cOperator )
                        {
                            real = fReal1 + fReal2;
                            imag = fImag1 + fImag2;

                            fOutput[iInputCount][0] = real;
                            fOutput[iInputCount][1] = imag;

                            ++iInputCount;
                        }

                        else if( '-' == cOperator )
                        {
                            real = fReal1 - fReal2;
                            imag = fImag1 - fImag2;

                            fOutput[iInputCount][0] = real;
                            fOutput[iInputCount][1] = imag;

                            ++iInputCount;
                        }

                        else if( '*' == cOperator )
                        {
                            real = fReal1*fReal2 - fImag1 *fImag2;
                            imag = fReal1 * fImag2 + fImag1 * fReal2 ;

                            fOutput[iInputCount][0] = real;
                            fOutput[iInputCount][1] = imag;

                            ++iInputCount;
                        }

                        else if( '/' == cOperator )
                        {
                            if( fReal2 != 0 && fImag2 != 0 )
                            {
                                real = (fReal1*fReal2 + fImag1 *fImag2) / ( fReal2 * fReal2 + fImag2 * fImag2 ) ;
                                imag = (fReal2 * fImag1 - fImag2 * fReal1) / ( fReal2 * fReal2 + fImag2 * fImag2 ) ;

                                fOutput[iInputCount][0] = real;
                                fOutput[iInputCount][1] = imag;

                                ++iInputCount;
                            }

                            else
                            {
                                //puts("\nDivision operation is not defined if both real and imaginary part of second number are 0");
                            }
                        }

                        else
                        {
                            //puts("\nInvalid input format");
                        }
                   }

                   else
                   {
                       //puts("\nInvalid input format");
                   }
               }

               else
               {
                   //puts("\nInvalid input format");
               }
           }
       }

       int  i;

       for ( i = 0 ; i < iInputCount ; ++i)
       {
           fprintf( fileWritePointer, "(%.2f,%.2f) \n\n", fOutput[i][0], fOutput[i][1] );
       }

    return 0;
}
