PADD     CSECT                                                          00010000
************                                                            00020000
* READ MSG FROM INPUT DATA STREAM AND DISPLAY INTO OP STREAM *          00030000
************                                                            00040000
         STM   14,12,12(13)                                             00050000
         BALR  12,0                                                     00060000
         USING *,12                                                     00070000
         ST    13,SAVE+4                                                00080000
         LA    13,SAVE                                                  00090000
****************                                                        00100000
* OPEN INPUT DATA FILE AND STANDARD PRINTER FILE    *                   00110000
****************                                                        00120000
         OPEN  (INFILE1,(INPUT))                                        00130000
         OPEN  (OUTFILE1,(OUTPUT))                                      00140000
*******************                                                     00150000
*      READ AND PRINT EACH RECORD                                       00160000
*******************                                                     00170000
         GET   INFILE1,INAREA                                           00180000
         PACK  BCD,INT1                                                 00190000
         CVB   5,BCD                                                    00200000
         ST    5,XX1                                                    00210000
         PACK  BCD,INT2                                                 00220000
         CVB   5,BCD                                                    00230000
         ST    5,YY1                                                    00240000
**************                                                          00250000
         L     3,XX1                                                    00260000
         A     3,YY1                                                    00270000
         ST    3,ZZ1                                                    00280000
**************                                                          00290000
         L     5,ZZ1                                                    00300000
         CVD   5,BCD                                                    00310000
         UNPK  SUM,BCD                                                  00320000
         OI    SUM+9,X'F0'                                              00330000
         PUT   OUTFILE1,OUTAREA                                         00340000
*******************                                                     00350000
INEOF    CLOSE (INFILE1)                                                00360000
         CLOSE (OUTFILE1)                                               00370000
EXIT     L     13,SAVE+4                                                00380000
         LM    14,12,12(13)                                             00390000
         RETURN (14,12),RC=0                                            00400000
***************                                                         00410000
INFILE1  DCB   DSORG=PS,MACRF=(GM),DDNAME=SYSIN,EODAD=INEOF,           *00420000
               RECFM=FB,LRECL=80,BLKSIZE=800                            00430000
OUTFILE1 DCB   DSORG=PS,MACRF=(PM),DDNAME=SYSOUT,                      *00440000
               RECFM=FBA,LRECL=133,BLKSIZE=3990                         00450000
***************                                                         00460000
INAREA   DS    0CL80                                                    00470000
         DS    CL12                                                     00480000
INT1     DS    CL3                                                      00490000
         DS    CL12                                                     00500000
INT2     DS    CL3                                                      00510000
         DS    CL50                                                     00520000
OUTAREA  DS    0CL132                                                   00530000
         DS    CL7' '                                                   00540000
         DC    C'YOUR SUM IS '                                          00550000
SUM      DS    CL10                                                     00560000
         DC    CL104' '                                                 00570000
*********                                                               00580000
BCD      DS    D                                                        00590000
XX1      DS    F                                                        00600000
YY1      DS    F                                                        00610000
ZZ1      DS    F                                                        00620000
SAVE     DS    18F                                                      00630000
         END                                                            00640000
