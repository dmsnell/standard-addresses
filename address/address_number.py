import unittest
import combinators as P

from . import Element, standard

@standard(
    CommonNames=(
        "Street Number",
        "Building Number",
        "House Number",
        "Site Number",
        "Structure Number"
    ),
    Definition="The numeric identifier for a land parcel, house, building, or other location along a thoroughfare or within a community.",
    ElementName="ADDRstandard.AddressNumber",
    Examples=(
        ("123 Main Street",(123, " Main Street")),
        ("15 B Highway 88",(15, " B Highway 88")),
    ),
    Section="2.2.1.2"
)
class AddressNumber(Element):
    @staticmethod
    def parse(document):
        return P.map(P.natural_number, AddressNumber)(document)

    def __init__(self, number):
        self.number = number
    
    def __repr__(self):
        return self.number

class TestAddressNumber(unittest.TestCase):
    def test_examples(self):
        AddressNumber.test_examples(self, lambda m: m.number)