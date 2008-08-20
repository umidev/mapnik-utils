import unittest
from cascade import ParseException, parse_stylesheet
from cascade import Selector, SelectorElement, SelectorAttributeTest

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
        self.assertEquals('0000 0001 0000', Selector(SelectorElement(['Layer'])).specificity())
    
    def testSpecificity2(self):
        self.assertEquals('0000 0002 0000', Selector(SelectorElement(['Layer']), SelectorElement(['name'])).specificity())
    
    def testSpecificity3(self):
        self.assertEquals('0000 0002 0000', Selector(SelectorElement(['Layer', '.class'])).specificity())
    
    def testSpecificity4(self):
        self.assertEquals('0000 0002 0000', Selector(SelectorElement(['Layer', '.class']), SelectorElement(['name'])).specificity())
    
    def testSpecificity4(self):
        self.assertEquals('0001 0002 0000', Selector(SelectorElement(['Layer', '#id']), SelectorElement(['name'])).specificity())
    
    def testSpecificity4(self):
        self.assertEquals('0001 0000 0000', Selector(SelectorElement(['#id'])).specificity())
    
    def testSpecificity4(self):
        self.assertEquals('0001 0000 0001', Selector(SelectorElement(['#id'], [SelectorAttributeTest('a', '>', 'b')])).specificity())
    
    def testSpecificity4(self):
        self.assertEquals('0001 0000 0002', Selector(SelectorElement(['#id'], [SelectorAttributeTest('a', '>', 'b'), SelectorAttributeTest('a', '<', 'b')])).specificity())

if __name__ == '__main__':
    unittest.main()