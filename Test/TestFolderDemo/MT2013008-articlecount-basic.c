#include <stdio.h>

#define TRUE  1
#define FALSE 0

typedef enum
{
    eSTATE_BEG,
    eSTATE_A,
    eSTATE_AN,
    eSTATE_FINAL,
    eSTATE_T,
    eSTATE_TH,
    eSTATE_THE,
    eSTATE_JUNK
}STATE;

const char *states[] = {"BEG","A","AN","FINAL","T","TH","THE","JUNK"};

typedef enum
{
  eINPUT_a,
  eINPUT_n,
  eINPUT_t ,
  eINPUT_h ,
  eINPUT_e ,
  eINPUT_SPACE ,
  eINPUT_other
} characterRead;

STATE stateBeginning[] = { eSTATE_A,eSTATE_JUNK, eSTATE_T, eSTATE_JUNK, eSTATE_JUNK, eSTATE_BEG, eSTATE_JUNK            } ;
STATE stateA[]         = { eSTATE_JUNK, eSTATE_AN, eSTATE_JUNK, eSTATE_JUNK, eSTATE_JUNK, eSTATE_FINAL, eSTATE_JUNK    } ;
STATE stateAN[]        = { eSTATE_JUNK, eSTATE_JUNK, eSTATE_JUNK, eSTATE_JUNK, eSTATE_JUNK, eSTATE_FINAL, eSTATE_JUNK            } ;
STATE stateJunk[]      = { eSTATE_JUNK, eSTATE_JUNK,eSTATE_JUNK, eSTATE_JUNK, eSTATE_JUNK, eSTATE_BEG, eSTATE_JUNK      } ;
STATE stateT[]         = { eSTATE_JUNK, eSTATE_JUNK,eSTATE_JUNK, eSTATE_TH, eSTATE_JUNK, eSTATE_BEG, eSTATE_JUNK       } ;
STATE stateTH[]        = { eSTATE_JUNK, eSTATE_JUNK,eSTATE_JUNK, eSTATE_JUNK, eSTATE_THE, eSTATE_BEG, eSTATE_JUNK      } ;
STATE stateTHE[]       = { eSTATE_JUNK, eSTATE_JUNK,eSTATE_JUNK, eSTATE_JUNK, eSTATE_JUNK, eSTATE_FINAL, eSTATE_JUNK    } ;
STATE stateFinal[]     = { eSTATE_A, eSTATE_JUNK,eSTATE_T, eSTATE_JUNK, eSTATE_JUNK, eSTATE_BEG, eSTATE_JUNK            } ;

STATE parsingStateCurrent = eSTATE_BEG;
STATE parsingStateNext    = eSTATE_BEG;

int isSpace( char cInputCharacter );
STATE getnextState( STATE currentState , characterRead inputChar );
void printState(STATE state);
void HandleStateChange(STATE currentState, STATE nextState, int* iArticlesCount, int* iWordsCount );

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


    int iArticlesCount=0;
    int iWordsCount=0;
    char * cFilePath;

    if( NULL != fileReadPointer  )
    {
        while ( 1 )
        {
            char cReadCharacter = fgetc(fileReadPointer);

            if( EOF == cReadCharacter )
                break;

            else
            {
                if( 'a' == cReadCharacter || 'A' == cReadCharacter)
                {
                    parsingStateNext = getnextState( parsingStateCurrent, eINPUT_a );
                    HandleStateChange( parsingStateCurrent, parsingStateNext, &iArticlesCount, &iWordsCount );
                    parsingStateCurrent = parsingStateNext ;
                }

                else if( 'n' == cReadCharacter )
                {
                    parsingStateNext = getnextState( parsingStateCurrent, eINPUT_n );
                    HandleStateChange( parsingStateCurrent, parsingStateNext, &iArticlesCount , &iWordsCount);
                    parsingStateCurrent = parsingStateNext ;
                }

                else if( 't' == cReadCharacter || 'T' == cReadCharacter )
                {
                    parsingStateNext = getnextState( parsingStateCurrent, eINPUT_t );
                    HandleStateChange( parsingStateCurrent, parsingStateNext, &iArticlesCount, &iWordsCount );
                    parsingStateCurrent = parsingStateNext ;
                }

                else if( 'h' == cReadCharacter )
                {
                    parsingStateNext = getnextState( parsingStateCurrent, eINPUT_h );
                    HandleStateChange( parsingStateCurrent, parsingStateNext, &iArticlesCount, &iWordsCount );
                    parsingStateCurrent = parsingStateNext ;
                }

                else if( 'e' == cReadCharacter )
                {
                    parsingStateNext = getnextState( parsingStateCurrent, eINPUT_e    );
                    HandleStateChange( parsingStateCurrent, parsingStateNext, &iArticlesCount , &iWordsCount);
                    parsingStateCurrent = parsingStateNext ;
                }

                else if( isSpace(cReadCharacter) )
                {
                    parsingStateNext = getnextState( parsingStateCurrent, eINPUT_SPACE);
                    HandleStateChange( parsingStateCurrent, parsingStateNext, &iArticlesCount , &iWordsCount);
                    parsingStateCurrent = parsingStateNext ;
                }

                else
                {
                    parsingStateNext = getnextState( parsingStateCurrent, eINPUT_other);
                    HandleStateChange( parsingStateCurrent, parsingStateNext, &iArticlesCount, &iWordsCount );
                    parsingStateCurrent = parsingStateNext ;
                }

                // Enable for debugging
                // printState( parsingStateNext );
            }
       }
  }

    else
    {
        puts("File couldnt be opened for reading") ;
    }

    fprintf( fileWritePointer, "%d\n%d\n%.2f\%\n" , iWordsCount, iArticlesCount, (float)(iArticlesCount * 100 ) / (iWordsCount) );

return 0;

}


int isSpace( char cInputCharacter  )
{
    if( ' ' == cInputCharacter || '\n' == cInputCharacter || '\t' == cInputCharacter || '\v' == cInputCharacter || '\r' == cInputCharacter || '\f' == cInputCharacter  )
        return TRUE;
    else
        return FALSE;
}

STATE getnextState( STATE currentState , characterRead inputChar )
{
    if ( eSTATE_BEG == currentState )
        return stateBeginning[ inputChar ];

    else if ( eSTATE_A == currentState )
        return stateA[ inputChar ];

    else if ( eSTATE_AN == currentState )
        return stateAN[ inputChar ];

    else if ( eSTATE_T == currentState )
        return stateT[ inputChar ];

    else if ( eSTATE_TH == currentState )
        return stateTH[ inputChar ];

    else if ( eSTATE_THE == currentState )
        return stateTHE[ inputChar ];

    else if ( eSTATE_JUNK == currentState )
        return stateJunk[ inputChar ];

    else if ( eSTATE_FINAL == currentState )
        return stateFinal[ inputChar ];

    else
    { printf("ERROR"); }
}

void printState(STATE state)
{
    printf("State: %s\n", states[state] );
}

void HandleStateChange(STATE currentState, STATE nextState, int* iArticlesCount, int* iWordsCount )
{
    if ( eSTATE_FINAL == nextState )
        ++ (*iArticlesCount);

    if(
        ( eSTATE_A == currentState && eSTATE_FINAL == nextState )
     || ( eSTATE_JUNK == currentState && eSTATE_BEG == nextState )
     || ( eSTATE_AN == currentState && eSTATE_BEG == nextState )
     || ( eSTATE_T == currentState && eSTATE_BEG == nextState )
     || ( eSTATE_TH == currentState && eSTATE_BEG == nextState )
     || ( eSTATE_THE == currentState && eSTATE_FINAL == nextState )
      )
        ++ (*iWordsCount);
}
