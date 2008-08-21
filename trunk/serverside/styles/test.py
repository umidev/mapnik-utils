import unittest
from cascade import ParseException, parse_stylesheet
from cascade import Selector, SelectorElement, SelectorAttributeTest
from cascade import postprocess_property, postprocess_value

class ParseTests(unittest.TestCase):
    
    def testBadSelector1(self):
        self.assertRaises(ParseException, parse_stylesheet, 'Too Many Things { }')

    def testBadSelector2(self):
        self.assertRaises(ParseException, parse_stylesheet, '{ }')

    def testBadSelector3(self):
        self.assertRaises(ParseException, parse_stylesheet, 'Illegal { }')

    def testBadSelector4(self):
        self.assertRaises(ParseException, parse_stylesheet, 'Layer foo[this=that] { }')

    def testBadSelector5(self):
        self.assertRaises(ParseException, parse_stylesheet, 'Layer foo#bar { }')

    def testBadSelector6(self):
        self.assertRaises(ParseException, parse_stylesheet, 'Layer foo.bar { }')

    def testBadProperty1(self):
        self.assertRaises(ParseException, parse_stylesheet, 'Layer { unknown-property: none; }')

    def testBadProperty2(self):
        self.assertRaises(ParseException, parse_stylesheet, 'Layer { extra thing: none; }')

    def testBadProperty3(self):
        self.assertRaises(ParseException, parse_stylesheet, 'Layer { "not an ident": none; }')

    def testRulesets1(self):
        self.assertEqual(0, len(parse_stylesheet('/* empty stylesheet */')))

    def testRulesets2(self):
        self.assertEqual(1, len(parse_stylesheet('Layer { }')))

    def testRulesets3(self):
        self.assertEqual(2, len(parse_stylesheet('Layer { } Layer { }')))

    def testRulesets4(self):
        self.assertEqual(3, len(parse_stylesheet('Layer { } /* something */ Layer { } /* extra */ Layer { }')))

class SelectorTests(unittest.TestCase):
    
    def testSpecificity1(self):
        self.assertEquals((0, 1, 0), Selector(SelectorElement(['Layer'])).specificity())
    
    def testSpecificity2(self):
        self.assertEquals((0, 2, 0), Selector(SelectorElement(['Layer']), SelectorElement(['name'])).specificity())
    
    def testSpecificity3(self):
        self.assertEquals((0, 2, 0), Selector(SelectorElement(['Layer', '.class'])).specificity())
    
    def testSpecificity4(self):
        self.assertEquals((0, 2, 0), Selector(SelectorElement(['Layer', '.class']), SelectorElement(['name'])).specificity())
    
    def testSpecificity4(self):
        self.assertEquals((1, 2, 0), Selector(SelectorElement(['Layer', '#id']), SelectorElement(['name'])).specificity())
    
    def testSpecificity4(self):
        self.assertEquals((1, 0, 0), Selector(SelectorElement(['#id'])).specificity())
    
    def testSpecificity4(self):
        self.assertEquals((1, 0, 1), Selector(SelectorElement(['#id'], [SelectorAttributeTest('a', '>', 'b')])).specificity())
    
    def testSpecificity4(self):
        self.assertEquals((1, 0, 2), Selector(SelectorElement(['#id'], [SelectorAttributeTest('a', '>', 'b'), SelectorAttributeTest('a', '<', 'b')])).specificity())

    def testMatch1(self):
        self.assertEqual(True, Selector(SelectorElement(['Layer'])).matches('foo', []))

    def testMatch2(self):
        self.assertEqual(True, Selector(SelectorElement(['#foo'])).matches('foo', []))

    def testMatch3(self):
        self.assertEqual(False, Selector(SelectorElement(['#foo'])).matches('bar', []))

    def testMatch4(self):
        self.assertEqual(True, Selector(SelectorElement(['.bar'])).matches(None, ['bar']))

    def testMatch5(self):
        self.assertEqual(True, Selector(SelectorElement(['.bar'])).matches(None, ['bar', 'baz']))

    def testMatch6(self):
        self.assertEqual(True, Selector(SelectorElement(['.bar', '.baz'])).matches(None, ['bar', 'baz']))

    def testMatch7(self):
        self.assertEqual(False, Selector(SelectorElement(['.bar', '.baz'])).matches(None, ['bar']))

class PropertyTests(unittest.TestCase):

    def testProperty1(self):
        self.assertRaises(ParseException, postprocess_property, [('IDENT', 'too-many'), ('IDENT', 'properties')])

    def testProperty2(self):
        self.assertRaises(ParseException, postprocess_property, [])

    def testProperty3(self):
        self.assertRaises(ParseException, postprocess_property, [('IDENT', 'illegal-property')])

    def testProperty4(self):
        self.assertEquals('shield', postprocess_property([('IDENT', 'shield-fill')]).group())

    def testProperty5(self):
        self.assertEquals('shield', postprocess_property([('S', ' '), ('IDENT', 'shield-fill'), ('COMMENT', 'ignored comment')]).group())

if __name__ == '__main__':
    unittest.main()