import unittest
from cascade import ParseException, parse_stylesheet
from cascade import Selector, SelectorElement, SelectorAttributeTest
from cascade import postprocess_property, postprocess_value, Property

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

    def testRulesets5(self):
        self.assertEqual(1, len(parse_stylesheet('Map { }')))

class SelectorTests(unittest.TestCase):
    
    def testSpecificity1(self):
        self.assertEquals((0, 1, 0), Selector(SelectorElement(['Layer'])).specificity())
    
    def testSpecificity2(self):
        self.assertEquals((0, 2, 0), Selector(SelectorElement(['Layer']), SelectorElement(['name'])).specificity())
    
    def testSpecificity3(self):
        self.assertEquals((0, 2, 0), Selector(SelectorElement(['Layer', '.class'])).specificity())
    
    def testSpecificity4(self):
        self.assertEquals((0, 3, 0), Selector(SelectorElement(['Layer', '.class']), SelectorElement(['name'])).specificity())
    
    def testSpecificity5(self):
        self.assertEquals((1, 2, 0), Selector(SelectorElement(['Layer', '#id']), SelectorElement(['name'])).specificity())
    
    def testSpecificity6(self):
        self.assertEquals((1, 0, 0), Selector(SelectorElement(['#id'])).specificity())
    
    def testSpecificity7(self):
        self.assertEquals((1, 0, 1), Selector(SelectorElement(['#id'], [SelectorAttributeTest('a', '>', 'b')])).specificity())
    
    def testSpecificity8(self):
        self.assertEquals((1, 0, 2), Selector(SelectorElement(['#id'], [SelectorAttributeTest('a', '>', 'b'), SelectorAttributeTest('a', '<', 'b')])).specificity())

    def testSpecificity9(self):
        self.assertEquals((1, 0, 2), Selector(SelectorElement(['#id'], [SelectorAttributeTest('a', '>', 100), SelectorAttributeTest('a', '<', 'b')])).specificity())

    def testMatch1(self):
        self.assertEqual(True, Selector(SelectorElement(['Layer'])).matches('Layer', 'foo', []))

    def testMatch2(self):
        self.assertEqual(True, Selector(SelectorElement(['#foo'])).matches('Layer', 'foo', []))

    def testMatch3(self):
        self.assertEqual(False, Selector(SelectorElement(['#foo'])).matches('Layer', 'bar', []))

    def testMatch4(self):
        self.assertEqual(True, Selector(SelectorElement(['.bar'])).matches('Layer', None, ['bar']))

    def testMatch5(self):
        self.assertEqual(True, Selector(SelectorElement(['.bar'])).matches('Layer', None, ['bar', 'baz']))

    def testMatch6(self):
        self.assertEqual(True, Selector(SelectorElement(['.bar', '.baz'])).matches('Layer', None, ['bar', 'baz']))

    def testMatch7(self):
        self.assertEqual(False, Selector(SelectorElement(['.bar', '.baz'])).matches('Layer', None, ['bar']))

    def testMatch8(self):
        self.assertEqual(False, Selector(SelectorElement(['Layer'])).matches('Map', None, []))

    def testMatch9(self):
        self.assertEqual(False, Selector(SelectorElement(['Map'])).matches('Layer', None, []))

    def testMatch10(self):
        self.assertEqual(True, Selector(SelectorElement(['*'])).matches('Layer', None, []))

    def testMatch10(self):
        self.assertEqual(True, Selector(SelectorElement(['*'])).matches('Map', None, []))

    def testRange1(self):
        selector = Selector(SelectorElement(['*'], [SelectorAttributeTest('scale-denominator', '>', 100)]))
        self.assertEqual(True, selector.isRanged())
        self.assertEqual(False, selector.inRange(99))
        self.assertEqual(False, selector.inRange(100))
        self.assertEqual(True, selector.inRange(1000))

    def testRange2(self):
        selector = Selector(SelectorElement(['*'], [SelectorAttributeTest('scale-denominator', '>=', 100)]))
        self.assertEqual(True, selector.isRanged())
        self.assertEqual(False, selector.inRange(99))
        self.assertEqual(True, selector.inRange(100))
        self.assertEqual(True, selector.inRange(1000))

    def testRange3(self):
        selector = Selector(SelectorElement(['*'], [SelectorAttributeTest('scale-denominator', '<', 100)]))
        self.assertEqual(True, selector.isRanged())
        self.assertEqual(True, selector.inRange(99))
        self.assertEqual(False, selector.inRange(100))
        self.assertEqual(False, selector.inRange(1000))

    def testRange4(self):
        selector = Selector(SelectorElement(['*'], [SelectorAttributeTest('scale-denominator', '<=', 100)]))
        self.assertEqual(True, selector.isRanged())
        self.assertEqual(True, selector.inRange(99))
        self.assertEqual(True, selector.inRange(100))
        self.assertEqual(False, selector.inRange(1000))

    def testRange5(self):
        selector = Selector(SelectorElement(['*'], [SelectorAttributeTest('nonsense', '<=', 100)]))
        self.assertEqual(False, selector.isRanged())
        self.assertEqual(True, selector.inRange(99))
        self.assertEqual(True, selector.inRange(100))
        self.assertEqual(True, selector.inRange(1000))

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

class ValueTests(unittest.TestCase):

    def testBadValue1(self):
        self.assertRaises(ParseException, postprocess_value, [], Property('polygon-opacity'))

    def testBadValue2(self):
        self.assertRaises(ParseException, postprocess_value, [('IDENT', 'too'), ('IDENT', 'many')], Property('polygon-opacity'))

    def testBadValue3(self):
        self.assertRaises(ParseException, postprocess_value, [('IDENT', 'non-number')], Property('polygon-opacity'))

    def testBadValue4(self):
        self.assertRaises(ParseException, postprocess_value, [('IDENT', 'non-string')], Property('text-face-name'))

    def testBadValue5(self):
        self.assertRaises(ParseException, postprocess_value, [('IDENT', 'non-hash')], Property('polygon-fill'))

    def testBadValue6(self):
        self.assertRaises(ParseException, postprocess_value, [('HASH', '#badcolor')], Property('polygon-fill'))

    def testBadValue7(self):
        self.assertRaises(ParseException, postprocess_value, [('IDENT', 'non-URI')], Property('point-file'))

    def testBadValue8(self):
        self.assertRaises(ParseException, postprocess_value, [('IDENT', 'bad-boolean')], Property('text-avoid-edges'))

    def testBadValue9(self):
        self.assertRaises(ParseException, postprocess_value, [('STRING', 'not an IDENT')], Property('line-join'))

    def testBadValue10(self):
        self.assertRaises(ParseException, postprocess_value, [('IDENT', 'not-in-tuple')], Property('line-join'))

    def testValue1(self):
        self.assertEqual(1.0, postprocess_value([('NUMBER', 1.0)], Property('polygon-opacity')).value)

    def testValue2(self):
        self.assertEqual(10, postprocess_value([('NUMBER', 10)], Property('line-width')).value)

    def testValue3(self):
        self.assertEqual('DejaVu', str(postprocess_value([('STRING', '"DejaVu"')], Property('text-face-name'))))

    def testValue4(self):
        self.assertEqual('#ff9900', str(postprocess_value([('HASH', '#ff9900')], Property('map-bgcolor'))))

    def testValue5(self):
        self.assertEqual('#ff9900', str(postprocess_value([('HASH', '#f90')], Property('map-bgcolor'))))

    def testValue6(self):
        self.assertEqual('http://example.com', str(postprocess_value([('URI', 'url("http://example.com")')], Property('point-file'))))

    def testValue7(self):
        self.assertEqual('true', str(postprocess_value([('IDENT', 'true')], Property('text-avoid-edges'))))

    def testValue8(self):
        self.assertEqual('false', str(postprocess_value([('IDENT', 'false')], Property('text-avoid-edges'))))

    def testValue9(self):
        self.assertEqual('bevel', str(postprocess_value([('IDENT', 'bevel')], Property('line-join'))))

if __name__ == '__main__':
    unittest.main()