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
    parse = P.natural_number

    def __init__(self, prefix):
        self.prefix = prefix
    
    def __repr__(self):
        return self.prefix

class TestAddressNumber(unittest.TestCase):
    def test_examples(self):
        AddressNumber.test_examples(self)