import combinators as P
import address as A

def runParser( parser, document ):
    return parser( document, 0 )

# "asdf;lkjasdf;lkj"
#   [ "asdf" ], 5 ]
#   [ "asdf", "lkjasdf" ], 14 ]
#   [ "asdf", "lkjasdf", "lkj" ], END

# fullmatch, matches = parser( document[0:] )
# nextParser( document[ len( fullmatch ): ] )

if "__main__" == __name__:
    myParser = P.seq(
        # P.regexMatch( '123' ),
        # P.regexMatch( r'\d+' ),
        # P.digits,
        P.natural_number,
        P.regexMatch( ' ' ),
        P.regexMatch( 'Main' )
    )
    document = "123 Main Street, Buffalo Lake, MN 55314"

    print( runParser( myParser, document ) )
    print( runParser( A.zipcode, "25000-0440" ) )
    print( runParser( A.zipcode, "00400-0001" ) )
    print( runParser( A.zipcode, "85716" ) )
    # print( A.CompleteZipcode.fromString( "15468" ) )
