#!/usr/bin/env python
# encoding: utf-8
#
# Copyright © 2013 deanishe@deanishe.net.
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2013-12-05
#

"""
"""



import sys
import os
import unittest
import unicodedata

import alfred

class AlfredTests(unittest.TestCase):

    _test_filename = 'üöäéøØÜÄÖÉàÀ.l11n'
    _unicode_test_filename = str(_test_filename, 'utf-8')

    def setUp(self):
        with open(self._test_filename, 'wb') as file:
            file.write('Testing!')

    def tearDown(self):
        if os.path.exists(self._test_filename):
            os.unlink(self._test_filename)

    def test_unicode_normalisation(self):
        """Ensure args are normalised in line with filesystem names"""
        self.assertTrue(os.path.exists(self._test_filename))
        filenames = [f for f in os.listdir('.') if f.endswith('.l11n')]
        self.assertTrue(len(filenames) == 1)
        print('{!r}'.format(filenames))
        fs_filename = filenames[0]
        self.assertTrue(fs_filename != self._test_filename)  # path has been NFD normalised by filesystem
        alfred_filename = alfred.decode(self._test_filename)
        self.assertTrue(alfred_filename == fs_filename)

    def test_unicode_value_xml(self):
        """Ensure we can handle converting Items with unicode values to xml"""
        item = alfred.Item({}, '\xb7', '\xb7')
        expected = '<items><item><title>\xc2\xb7</title><subtitle>\xc2\xb7</subtitle></item></items>'
        actual = alfred.xml([item])
        self.assertTrue(expected == actual, '{!r} != {!r}'.format(expected, actual))


if __name__ == '__main__':
    unittest.main()
