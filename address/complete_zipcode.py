import unittest
import combinators as P

from . import Element, standard

@standard()
class CompleteZipcode(Element):
    def parse(document):
        return zipcode(document)

    def __init__(self, zip5, zip4 = None):
        self.zip5 = zip5
        self.zip4 = zip4
    
    def __repr__(self):
        return self.zip5 if self.zip4 is None else self.zip5 + '-' + self.zip4
    
    # @staticmethod
    # def fromString( s ):
    #     return zipcode( s, 0 )

# def zip5_helper( s ):
#     if len( s ) != 5:
#         raise ValueError()
#     return s

# zip5 = P.map( P.digits, zip5_helper )
zip5 = P.regex(r'\d{5}')

zip4 = P.regex(r'\d{4}')

zipcode = P.choice(
    P.map(P.seq(zip5, P.char('-'), zip4), lambda v: CompleteZipcode(v[0], v[2])),
    P.map(zip5, CompleteZipcode)
)

class TestCompleteZipcode(unittest.TestCase):
    def test_matches_five_digits(self):
        self.assertIsInstance(zip5("12345"), P.Match)

    def test_matches_full_zipcode(self):
        z = zipcode("12345-6789")

        self.assertIsInstance(z.value, CompleteZipcode)
        self.assertEqual(z.value.zip5, "12345")
        self.assertEqual(z.value.zip4, "6789")

        z = zipcode("85716")

        self.assertIsInstance(z.value, CompleteZipcode)
        self.assertEqual(z.value.zip5, "85716")
        self.assertIsNone(z.value.zip4)

    def test_fails_to_match_four_digits(self):
        self.assertIsInstance(zip5("2345"), P.NoMatch)
    
    def test_fails_to_match_only_zip4(self):
        self.assertIsInstance(zipcode("6789"), P.NoMatch)
        self.assertIsInstance(zipcode("-6789"), P.NoMatch)