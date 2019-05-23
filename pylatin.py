#Alex Greenman
#873392313
#this python script contains two functions that convert strings to and from
#the made-up language PyLatin. It also contains a main function that contains
#test cases that ensure the conversion functions have the requisite properties

import string
import unittest

ascii_vowels_lowercase = 'aeiouy'
ascii_vowels_uppercase = 'AEIOUY'
ascii_vowels = ascii_vowels_lowercase + ascii_vowels_uppercase
#generator expression to create variable containing all lowercase consonants
ascii_consonants_lowercase = ''.join(let for let in string.ascii_lowercase
                             if let not in ascii_vowels_lowercase)
#generator expression to create variable containing all uppercase consonants
ascii_consonants_uppercase = ''.join(let for let in string.ascii_uppercase
                             if let not in ascii_vowels_uppercase)
#create variable that has all upper and lower consonants
ascii_consonants = ascii_consonants_lowercase+ascii_consonants_uppercase

def to_pylatin(s):
    '''Translates a single string argument, 's', into the fictional language
    of PyLatin. Raises appropriate error if non-string argument or a string
    containing characters other than letters is passed in as an argument'''
    if type(s) != str:
        raise TypeError("input must be a string")
    #iterate over elements in s to check for the presence of non-letters
    for elements in s:
        if elements not in string.ascii_letters:
            raise ValueError("string must only contain letter characters")
    if len(s) < 3:
        pass
    #if s begins with a constant, add 'py' to the end of the string, and then
    #move all leading consonants to the end of s
    elif s[0] in ascii_consonants:
        s = s+'py'
        while s[0] not in ascii_vowels:
            s = s[1:] + s[0]
    #if s begins with a vowel, add 'on' to the end of the string, and then
    #move all leading vowels to the end of s
    elif s[0] in ascii_vowels:
        s = s+'on'
        while s[0] not in ascii_consonants:
            s = s[1:] + s[0]

    return s

def from_pylatin(s):
    '''Translates a single string argument, 's', from PyLatin back into English.
    Raises appropriate error if non-string argument, a string containing
    characters other than letters, or a string that is non-translatable
    is passed in as an argument'''
    if type(s) != str:
        raise TypeError("input must be a string")
    #iterate over elements in s to check for the presence of non-letters
    for elements in s:
        if elements not in string.ascii_letters:
            raise ValueError("string must only contain letter characters")
    if len(s) < 3:
        pass
    #if s ends with 'py' followed by consonants, remove 'py', and move consonants
    #to the beginning of s
    elif s[-1] in ascii_consonants and 'py' in s:
        #because of the rules of Pylatin, if s is less or equal to four letters,
        #it's not translatable, raise ValueError to notify user
        if len(s) <= 4:
            raise ValueError("string is not translatable")
        while s[-1] not in ascii_vowels:
            s = s[-1]+s[:-1]
        s=s[:-2]
    #if s ends with 'on' followed by vowels, remove 'on', and move vowels
    #to the beginning of s
    elif s[-1] in ascii_vowels and 'on' in s:
        #because of the rules of Pylatin, if s is less or equal to four letters,
        #it's not translatable, raise ValueError to notify user
        if len(s) <= 4:
            raise ValueError("string is not translatable")
        while s[-1] not in ascii_consonants:
            s = s[-1]+s[:-1]
        s=s[:-2]
    #if s is not a Pylatin word, inform the user that words is not translatable
    else:
        raise ValueError("string is not translatable")

    return s

class TestMethods(unittest.TestCase):

    def test_to_pylatin_consonants(self):
        '''Tests whether or not a string beginning with a consonant
        is properly translated to Pylatin'''
        to_pylatin_consonant_pairs=[('hello', 'ellopyh'),('snakes', 'akespysn'),
        ('hamburger', 'amburgerpyh'),('python', 'ythonpyp'), ('pie', 'iepyp')]
        for word, translation in to_pylatin_consonant_pairs:
            with self.subTest(word=word, translation=translation):
                self.assertEqual(to_pylatin(word),translation)

    def test_to_pylatin_vowels(self):
        '''Tests whether or not a string beginning with a vowel
        is properly translated to Pylatin'''
        to_pylatin_vowel_pairs=[('apple', 'ppleona'), ('island', 'slandoni'),
        ('excellent', 'xcellentone'), ('onion', 'nionono'), ('use', 'seonu')]
        for word, translation in to_pylatin_vowel_pairs:
            with self.subTest(word=word, translation=translation):
                self.assertEqual(to_pylatin(word),translation)

    def test_from_pylatin_consonants(self):
        '''Tests whether or not a Pylatin string that begins with a consonant
        is properly translated back to plain English'''
        from_pylatin_consonant_pairs=[("ppleona", 'apple'),("slandoni", 'island'),
        ("xcellentone",'excellent'), ('nionono','onion')]
        for word, translation in from_pylatin_consonant_pairs:
            with self.subTest(word=word, translation=translation):
                self.assertEqual(from_pylatin(word),translation)

    def test_from_pylatin_vowels(self):
        '''Tests whether or not a Pylatin string that begins with a vowel
        is properly translated back to plain English'''
        from_pylatin_vowel_pairs=[('ellopyh', 'hello'),('akespysn', 'snakes'),
        ('amburgerpyh','hamburger'), ('ythonpyp','python')]
        for word, translation in from_pylatin_vowel_pairs:
            with self.subTest(word=word, translation=translation):
                self.assertEqual(from_pylatin(word),translation)

    def test_to_pylatin_less_than_three(self):
        '''Tests whether or not a string with less than 3 characters passed
        into 'to_python' returns that same, untranslated string'''
        to_pylatin_less_than_three=[('an', 'an'),('of', 'of'), ('by', 'by'),
        ('py', 'py'), ('on', 'on')]
        for word, translation in to_pylatin_less_than_three:
            with self.subTest(word=word, translation=translation):
                self.assertEqual(to_pylatin(word),translation)

    def test_from_pylatin_less_than_three(self):
        '''Tests whether or not a string with less than 3 characters passed
        into 'from_python' returns that same, untranslated string'''
        from_pylatin_less_than_three=[('as', 'as'),('be', 'be'),('it', 'it'),
        ('on', 'on'), ('py','py')]
        for word, translation in from_pylatin_less_than_three:
            with self.subTest(word=word, translation=translation):
                self.assertEqual(from_pylatin(word),translation)

    def test_non_string_to_pylatin(self):
        '''Test that passing a non-string into to_pylatin raises a TypeError'''
        bad_inputs=[6,['hello?'],(4,5,'car'),{},.5]
        for bad_input in bad_inputs:
            with self.subTest(bad_input=bad_input):
                with self.assertRaises(TypeError):
                    to_pylatin(bad_input)

    def test_non_string_from_pylatin(self):
        '''Test that passing a non-string into from_pylatin raises a TypeError'''
        bad_inputs=[6,['hello?'],(4,5,'car'),{},.5]
        for bad_input in bad_inputs:
            with self.subTest(bad_input=bad_input):
                with self.assertRaises(TypeError):
                    from_pylatin(bad_input)

    def test_non_letters_string_to_pylatin(self):
        '''Test that passing a string containing non-letters to_pylatin
        raises a ValueError'''
        bad_inputs=['hello!','hello?','#hello!', 'h-i>!']
        for bad_input in bad_inputs:
            with self.subTest(bad_input=bad_input):
                with self.assertRaises(ValueError):
                    to_pylatin(bad_input)

    def test_non_letters_string_from_pylatin(self):
        '''Test that passing a string containing non-letters from_pylatin
        raises a ValueError'''
        bad_inputs=['ellopyh!','ellopyh?','#ellopyh!', 'el-lo>pyh!']
        for bad_input in bad_inputs:
            with self.subTest(bad_input=bad_input):
                with self.assertRaises(ValueError):
                    from_pylatin(bad_input)

    def test_non_pylatin_pass_into_from_pylatin(self):
        '''Test that passing non-PyLatin strings to from_pylatin
        raises a ValueError'''
        bad_inputs=['newyork','cars', 'test', 'pyon', 'ypon', 'use', 'tie',
        'onpy','elloph']
        for bad_input in bad_inputs:
            with self.subTest(bad_input=bad_input):
                with self.assertRaises(ValueError):
                    from_pylatin(bad_input)

if __name__ == '__main__':
   unittest.main()
