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
    def inner(cls):
        def test_examples(self, transformer=lambda x: x):
            for example in Examples:
                p = cls.parse(example[0])
                self.assertIsInstance(p, P.Match)
                self.assertEqual(transformer(p.value), example[1][0])
                self.assertEqual(p.remaining, example[1][1])

        return type(
            cls.__name__,
            (cls,),
            {
                'CommonNames': CommonNames,
                'Definition': Definition,
                'ElementName': ElementName,
                'Examples': Examples,
                'Section': Section,
                'Standard': Standard,
                'test_examples': staticmethod(test_examples),
            }
        )

    return inner

class Element:
    pass

from .address_number_prefix import AddressNumberPrefix, TestAddressNumberPrefix
from .address_number import AddressNumber, TestAddressNumber
from .complete_zipcode import CompleteZipcode, TestCompleteZipcode
