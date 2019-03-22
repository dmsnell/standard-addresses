import combinators as P
import address as A

# "asdf;lkjasdf;lkj"
#   [ "asdf" ], 5 ]
#   [ "asdf", "lkjasdf" ], 14 ]
#   [ "asdf", "lkjasdf", "lkj" ], END

# fullmatch, matches = parser( document[0:] )
# nextParser( document[ len( fullmatch ): ] )

if "__main__" == __name__:
    myParser = P.seq(
        # P.regex('123'),
        # P.regex(r'\d+'),
        # P.digits,
        P.natural_number,
        P.regex(' '),
        P.regex('Main')
    )
    document = "123 Main Street, Buffalo Lake, MN 55314"

    print(myParser(document))
    print(A.zipcode("25000-0440"))
    print(A.zipcode("00400-0001"))
    print(A.zipcode("85716"))

