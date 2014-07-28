#include "dstring.h"
#include <stdlib.h>
#include <string.h>

// Create a new dstring using the given input return a pointer to the same
// this function should do the malloc for dstring and return its pointer
// after proper initialization of data

dstring * dstrcreate( char *buf, int length )
{
    dstring * tempDstring = (dstring *)malloc( sizeof(int) + sizeof(char*));

    if( NULL != tempDstring )
    {
        tempDstring->length = length;
        tempDstring->buf = (char*)malloc(sizeof(char)*length);
        memcpy( tempDstring->buf, buf, sizeof(char)*length );
        return tempDstring;
    }

    // Set Error code

    return tempDstring;
}

// Free an existing dstring
void dstrfree( dstring *str )
{
    if( NULL != str )
    {
        if( NULL != str->buf )
        {
            free( str->buf );
        }
        free( str );
        return ;
    }

    // Set Error code
}

// Analogous to strcpy but watch out for deep copy vs shallow copy
dstring *dstrcpy( dstring *dest, dstring *src )
{
    if( NULL != dest->buf )
    {
        free(dest->buf);
    }

    if( NULL != dest && NULL != src )
    {
        dest->length = src->length;
        dest->buf = (char *) malloc( sizeof(char) * (src->length) );
        if( NULL != dest && NULL != src )
        {
            memcpy( dest->buf, src->buf, sizeof(char) * (src->length) );
        }

        return dest;
    }

    // Set Error code
    return dest;
}

// Analogous to strcmp
int dstrcmp( dstring *str1, dstring *str2 )
{
    int max ;

    if( NULL != str1 && NULL != str2 )
    {
        if( str1->length > str2->length )
            max = str2->length;
        else
            max = str1->length;

        int i;
        for( i = 0 ; i < max ; ++ i)
        {
            if( str1->buf[i] > str2->buf[i] )
                return 1;
            else if( str1->buf[i] < str2->buf[i] )
                return -1;
        }

        if( str1->length > str2->length )
        return 1;
        else if ( str1->length < str2->length  )
        return -1;
        else
        return 0;
    }

    // Set the respective error code

    return 0;
}

// Analogous to strcat
dstring *dstrcat( dstring *str1, dstring *str2 )
{
    if( NULL != str1 && NULL != str2 )
    {
        dstring * tempString = (dstring*) malloc ( sizeof(dstring) );
        tempString->length = str1->length + str2->length ;

        if( NULL != tempString )
        {
            tempString->buf = (char*) malloc( sizeof(char) * tempString->length );

            if( NULL != tempString->buf )
            {
                int i ;
                for(  i = 0; i < str1->length ; ++i )
                {
                    tempString->buf[i] = str1->buf[i];
                }

                int j ;
                for ( j = 0 ; i < tempString->length ; ++ i, ++ j )
                {
                    tempString->buf[i] = str2->buf[j];
                }

                return tempString;
            }
        }
    }

    // Set Error code
    return NULL;
}

// Analogous to strlen
int dstrlen( dstring *str )
{
    if( NULL != str )
        return str->length;
    else return -1;
}

