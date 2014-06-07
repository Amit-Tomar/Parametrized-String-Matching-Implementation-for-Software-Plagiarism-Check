#ifndef MATCH_H
#define MATCH_H

typedef enum
{
    eFullMatch,
    ePartialMatch,
    eNoMatch

}matchType;

typedef enum
{
    eStringLarger,
    eSuffixLarger,
    eStringSuffixSame

}stringSuffixLengthMatchType;


typedef struct
{
    int position;
    matchType matchingType;
    stringSuffixLengthMatchType lengthMatchType;

}Match;

#endif // MATCH_H
