import unittest
from combinators import Match, NoMatch, any as p_any, char, choice, digits as p_digits, first, flattenString, many, map, neg as p_neg, pos as p_pos, seq

from . import Element, standard

@standard(
    CommonNames=(
        "Street Number Prefix",
        "Building Number Prefix",
        "House Number Prefix",
        "Site Number Prefix",
        "Structure Number Prefix"
    ),
    Definition="The portion of the Complete Address Number which precedes the Address Number itself.",
    ElementName="AddressNumberPrefix",
    Examples=(
        ("N6W2 3001 Bluemound Road",("N6W2", " 3001 Bluemound Road")),
        ("A 19 Calle 11",("A", " 19 Calle 11")),
        ("194-0 3 Fiftieth Ave",("194-0", " 3 Fiftieth Ave")),
        ("Milepost 1303 Alaska Highway",("Milepost", " 1303 Alaska Highway")),
    ),
    Section="2.2.1.1"
)
class AddressNumberPrefix(Element):
    def parse(*kargs, **kwargs):
        return address_number_prefix(*kargs, **kwargs)

    def __init__(self, prefix):
        self.prefix = prefix
    
    def __repr__(self):
        return self.prefix

prefix_only = flattenString(many(flattenString(seq(p_neg(char(' ')), p_any))))

mashed_with_number = first(seq(
    flattenString(many(choice(
        char('0'),
        flattenString(seq(p_neg(seq(p_digits, char(' '))), p_any))
    ))),
    p_pos(p_digits)
))

def address_number_prefix(document, with_address_number=False):
    if with_address_number:
        return mashed_with_number(document)
    else:
        return prefix_only(document)

class TestAddressNumberPrefix(unittest.TestCase):
    def test_anything_before_space(self):
        p = prefix_only('N6W2 ')

        self.assertIsInstance(p, Match)
        self.assertEqual(p.value, 'N6W2')
        self.assertEqual(p.remaining, ' ')
    
    def test_mashed_with_number(self):
        p = mashed_with_number('Kilometer73 ')

        self.assertIsInstance(p, Match)
        self.assertEqual(p.value, 'Kilometer')
        self.assertEqual(p.remaining, '73 ')

    def test_mashed_but_no_number(self):
        p = mashed_with_number('N6W ')

        self.assertIsInstance(p, NoMatch)

    def test_mashed_with_hyphen(self):
        p = mashed_with_number('82-4 ')

        self.assertIsInstance(p, Match)
        self.assertEqual(p.value, '82-')
        self.assertEqual(p.remaining, '4 ')
 
    def test_mashed_with_hyphen_and_zero(self):
        p = mashed_with_number( '82-04 ')

        self.assertIsInstance(p, Match)
        self.assertEqual(p.value, '82-0')
        self.assertEqual(p.remaining, '4 ')

    def test_mashed_with_hyphen_and_zeros(self):
        p = mashed_with_number( '82-0004 ')

        self.assertIsInstance(p, Match)
        self.assertEqual(p.value, '82-000')
        self.assertEqual(p.remaining, '4 ')

    def test_mashed_with_hyphen_and_letter(self):
        p = mashed_with_number( '82-A4 ')

        self.assertIsInstance(p, Match)
        self.assertEqual(p.value, '82-A')
        self.assertEqual(p.remaining, '4 ')

    def test_mashed_with_hyphen_and_letters(self):
        p = mashed_with_number( '82-ABC4 ')

        self.assertIsInstance(p, Match)
        self.assertEqual(p.value, '82-ABC')
        self.assertEqual(p.remaining, '4 ')

    def test_examples(self):
        AddressNumberPrefix.test_examples(self)