Alignfull    DS       0F            align full word boundary

Pdetail      DS       0CL110        'person detail'
Pfname       DS       CL20          first name
Plname       DS       CL20          last name
Paddress     DS       CL30          address
Pnumber      DS       CL10          phone number
Pemail       DS       CL30          email address

Var1         DS       HL20          var1 length is 20
Var2         DC       CL10'ABCDE FGHI'    var2 length is 5
Var3         DC       CL10'ABCDE FGHI                                  - 
0000000000000000000000000000000000000000'      
PRVINDEX DS   264F                                                 @L1A