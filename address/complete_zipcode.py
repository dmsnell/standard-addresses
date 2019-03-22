import unittest
import combinators as P

from . import Element, standard

@standard(
    Examples=(
        ("12345", (("12345", None), "")),
        ("12345-6789", (("12345", "6789"), "")),
    )
)
class CompleteZipcode(Element):
    @staticmethod
    def parse(document):
        return P.map(zipcode, lambda zs: CompleteZipcode(zs[0], zs[1]))(document)

    def __init__(self, zip5, zip4=None):
        self.zip5 = zip5
        self.zip4 = zip4
    
    def __repr__(self):
        return self.zip5 if self.zip4 is None else self.zip5 + '-' + self.zip4
 
zip5 = P.regex(r'\d{5}')

zip4 = P.regex(r'\d{4}')

zipcode = P.choice(
    P.seq(zip5, P.skip(P.char('-')), zip4),
    P.map(zip5, lambda z: (z,None))
)

class TestCompleteZipcode(unittest.TestCase):
    def test_fails_to_match_four_digits(self):
        self.assertIsInstance(zip5("2345"), P.NoMatch)
    
    def test_fails_to_match_only_zip4(self):
        self.assertIsInstance(zipcode("6789"), P.NoMatch)
        self.assertIsInstance(zipcode("-6789"), P.NoMatch)
    
    def test_examples(self):
        CompleteZipcode.test_examples(self, lambda m: (m.zip5, m.zip4))