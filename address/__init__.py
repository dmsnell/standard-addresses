import combinators as P
from functools import wraps

def standard(
    CommonNames=(),
    Definition="",
    ElementName=None,
    Examples=(),
    Section=None,
    Standard="FGDC-STD-016-2011"
):
    @wraps(standard)
    def inner(cls):
        cls.CommonNames = CommonNames
        cls.Definition  = Definition
        cls.ElementName = ElementName
        cls.Examples    = Examples
        cls.Section     = Section
        cls.Standard    = Standard

        def test_examples(self):
            for example in Examples:
                p = cls.parse(example[0])
                self.assertIsInstance(p, P.Match)
                self.assertEqual(p.value, example[1][0])
                self.assertEqual(p.remaining, example[1][1])

        cls.test_examples = test_examples

        return cls

    return inner

class Element:
    pass

from .address_number_prefix import AddressNumberPrefix, TestAddressNumberPrefix
from .address_number import AddressNumber, TestAddressNumber
from .complete_zipcode import CompleteZipcode, TestCompleteZipcode
