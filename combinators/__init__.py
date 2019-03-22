import re

class Result:
    pass

class Match(Result):
    def __init__(self, value, remaining):
        self.value     = value
        self.remaining = remaining
    
    def __repr__(self):
        return "( " + str(self.value) + " )"

class NoMatch(Result):
    def __repr__(self):
        return "()"

def regex(pattern):
    def parser(document):
        match = re.match('^' + pattern, document)

        if match is None:
            return NoMatch()
        
        if match.start(0) != 0:
            return NoMatch()
        
        return Match(match.group(0), document[match.end(0):])

    return parser

def choice(*parsers):
    def parser(document):
        for p in parsers:
            match = p(document)

            if isinstance(match, Match):
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
def map(parser, transformer):
    def transformed(document):
        match = parser(document)

        if not isinstance(match, Match):
            return NoMatch()
        
        try:
            # Any transformed value is legitimate,
            # even `None` and `False` - consider
            # for instance a JSON parser, which
            # could contain these values
            new_value = transformer(match.value)
        except Exception as e:
            # Uncomment to raise error
            # raise e

            # If we throw an exception though that's
            # qualitatively different - we cannot
            # store exceptions in a string - they
            # only exist at runtime
            return NoMatch()

        return Match(new_value, match.remaining)

    return transformed

def seq(*parsers):
    def parser(document):
        matches = []
        remaining = document

        for p in parsers:
            match = p(remaining)

            if not isinstance(match, Match):
                return NoMatch()
            
            matches.append(match.value)
            remaining = match.remaining
        
        return Match(matches, remaining)
    
    return parser

### Common parsers

def char(c):
    def parser(document):
        if len(document) == 0 or c != document[0]:
            return NoMatch()
        else:
            return Match(c, document[1:])
    
    return parser

digits = regex(r'\d+')

natural_number = map(digits, int) 
