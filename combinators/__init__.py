import re

class Match:
    def __init__( self, value, nextOffset ):
        self.value = value
        self.nextOffset = nextOffset
    
    def __repr__( self ):
        return str( self.value ) + ' ending at ' + str( self.nextOffset )

class NoMatch:
    def __repr__( self ):
        return "! no match"

def regexMatch( pattern ):
    def parser( document, offset ):
        match = re.match( '^' + pattern, document[offset:] )

        if match is None:
            return NoMatch()
        
        if match.start( 0 ) != 0:
            return NoMatch()
        
        return Match( match.group( 0 ), offset + match.end( 0 ) )

    return parser

def choice( *parsers ):
    def parser( document, offset ):
        for p in parsers:
            match = p( document, offset )

            if isinstance( match, Match ):
                return match
        
        return NoMatch()

    return parser

###
# takes a parser and a transformer function
#   - if the parser matches its content
#   - take the value that matched
#   - run it through the transformer
#   - return a new match with the transformed value
#   - but if it errors with an exception, make it fail the parse
###
def map( parser, transformer ):
    def transformed( document, offset ):
        match = parser( document, offset )

        if isinstance( match, NoMatch ):
            return NoMatch()
        
        try:
            # Any transformed value is legitimate,
            # even `None` and `False` - consider
            # for instance a JSON parser, which
            # could contain these values
            new_value = transformer( match.value )
        except Exception as e:
            # Uncomment to raise error
            # raise e

            # If we throw an exception though that's
            # qualitatively different - we cannot
            # store exceptions in a string - they
            # only exist at runtime
            return NoMatch()

        return Match( new_value, match.nextOffset )

    return transformed

def seq( *parsers ):
    def parser( document, offset ):
        matches = []
        nextOffset = offset

        for p in parsers:
            match = p( document, nextOffset )

            if isinstance( match, NoMatch ):
                return NoMatch()
            
            matches.append( match.value )
            nextOffset = match.nextOffset
        
        return Match( matches, nextOffset )
    
    return parser

### Common parsers

def char( c ):
    def parser( document, offset ):
        if len( document ) <= offset or c == document[ offset ]:
            return Match( c, offset + 1 )
        else:
            return NoMatch()
    
    return parser

digits = regexMatch( r'\d+' )

natural_number = map( digits, int )
