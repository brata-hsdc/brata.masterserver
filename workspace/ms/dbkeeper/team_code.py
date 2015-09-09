#!/usr/bin/python

from random import randint

#----------------------------------------------------------------------------
class TeamCode(object):
    """ Creates and manipulates a user-friendly Team identification code.
        Each code is made of 3 components:  2 letters and an integer.
        Each component is represented by a word.  The letters use the military
        radio letter code (Alpha, Bravo, Charlie, ...), and the integers map to
        ice cream flavors.  Other words can be substituted for the values if desired.
        The integer will be a check value for the letters.  The letters will be added
        together, and taken mod 16 to match the numeric check value.
    """
    CALL_LETTERS = """alpha bravo charlie delta echo foxtrot golf hotel
                      india juliet kilo lima mike november oscar papa
                      quebec romeo sierra tango uniform victor whiskey
                      xray yankee zulu""".split()
    CHAR_LETTERS = "abcdefghijklmnopqrstuvwxyz"
    
    LETTER_LIST = zip(CALL_LETTERS, list(CHAR_LETTERS))
                   
    LETTER = dict(LETTER_LIST)
#                 "alpha":    "a",
#                 "bravo":    "b",
#                 "charlie":  "c",
#                 "delta":    "d",
#                 "echo":     "e",
#                 "foxtrot":  "f",
#                 "golf":     "g",
#                 "hotel":    "h",
#                 "india":    "i",
#                 "juliet":   "j",
#                 "kilo":     "k",
#                 "lima":     "l",
#                 "mike":     "m",
#                 "november": "n",
#                 "oscar":    "o",
#                 "papa":     "p",
#                 "quebec":   "q",
#                 "romeo":    "r",
#                 "sierra":   "s",
#                 "tango":    "t",
#                 "uniform":  "u",
#                 "victor":   "v",
#                 "whiskey":  "w",
#                 "xray":     "x",
#                 "yankee":   "y",
#                 "zulu":     "z",

    NUMBER_WORDS = """bubble-gum vanilla chocolate strawberry coffee chocolate-chip
                      mint-chocolate-chip lemon raspberry cookie-dough cherry peach
                      praline mocha mocha-chip rocky-road""".split()

    NUMBER_LIST = zip(NUMBER_WORDS, range(0, 16))

    NUMBER = dict(NUMBER_LIST)
#                 "bubble-gum":           0,
#                 "vanilla":              1,
#                 "chocolate":            2,
#                 "strawberry":           3,
#                 "coffee":               4,
#                 "chocolate-chip":       5,
#                 "mint-chocolate-chip":  6,
#                 "lemon":                7,
#                 "raspberry":            8,
#                 "cookie-dough":         9,
#                 "cherry":              10,
#                 "peach":               11,
#                 "praline":             12,
#                 "mocha":               13,
#                 "mocha-chip":          14,
#                 "rocky-road":          15,

    
    CODE_LENGTH = 2  # Max # of codes = 26 * 26 = 626  
    CHECK_LENGTH = 2
    LENGTH = CODE_LENGTH + CHECK_LENGTH  # length in chars of the whole code
    
    MAX_TRIES = 5000  # Number of attempts at finding a unique code

    @staticmethod
    def maxUniqueCodes():
        return len(TeamCode.CHAR_LETTERS)**TeamCode.CODE_LENGTH
    
    @staticmethod
    def newCode(existingCodes=None):
        """ Create a random code.
            existingCodes is an optional list of codes to avoid.  If provided,
            newCode() will guarantee returning a code not in the list (if it can),
            or None (if it can't find one after MAX_TRIES).
            The maximum number of unique codes is len(CHAR_LETTERS)**CODE_LENGTH.
            existingCodes must be properly in lower case.
        """
        code = TeamCode._genCode()
        count = 1
        if existingCodes is not None:
            while code in existingCodes:
                code = TeamCode._genCode()
                count += 1
                if count >= TeamCode.MAX_TRIES:
                    return None
        return code
    
    @staticmethod
    def _genCode():
        code = ""
        n = 0
        for _ in range(TeamCode.CODE_LENGTH):
            c = randint(0, 25) + ord('a')
            n += c
            code += chr(c)
        n = n % 16
        return "{}{:02}".format(code, n)
    
    @staticmethod
    def isValid(code):
        """ Validate code.
            Return True if code is a legal code.
            Ignores leading and trailing whitespace.
        """
        code = code.strip().lower()
        return len(code) == (TeamCode.LENGTH) and \
               sum([ord(n) for n in code[0:TeamCode.CODE_LENGTH]]) % 16 == int(code[2:])
    
    @staticmethod
    def wordify(code):
        """ Convert code into words.
            If the code is badly formed or otherwise unconvertible,
            return an empty string.  The code does not need to be
            valid in order to wordify.  As long as the check number
            is in the valid range, words will be returned.
        """
        if len(code) != TeamCode.LENGTH:
            return ""
        words = ""
        try:
            code = code.strip().lower()
            for c in code[0:TeamCode.CODE_LENGTH]:
                words += TeamCode.CALL_LETTERS[ord(c) - ord('a')] + " "
            words += TeamCode.NUMBER_WORDS[int(code[TeamCode.CODE_LENGTH:])]
        except:
            return ""
        return words
    
    @staticmethod
    def unwordify(wordCode):
        """ Convert a wordified code back to an alphanumeric code.
            Return a valid code or None.
            This method is tolerant of upper/lower case and extra
            whitespace as long as it is not within a word.
        """
        words = wordCode.strip().lower().split()
        if len(words) != TeamCode.CODE_LENGTH + 1:
            return None
        code = ""
        try:
            for i in range(TeamCode.CODE_LENGTH):
                code += TeamCode.LETTER[words[i]]
            code += "{:02}".format(TeamCode.NUMBER[words[-1]])
        except KeyError:
                return None
        if TeamCode.isValid(code):
            return code
        return None

#----------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    import unittest
    from collections import defaultdict
    
    class TeamCodeTestCase(unittest.TestCase):
        def testIsValid(self):
            self.assertTrue(TeamCode.isValid("aa02"))
            self.assertTrue(TeamCode.isValid("ab03")) # note that check value does not prevent transposing of chars
            self.assertTrue(TeamCode.isValid("ba03"))
            self.assertTrue(TeamCode.isValid("sz13"))
            self.assertFalse(TeamCode.isValid("sz12"))
            self.assertFalse(TeamCode.isValid("sz14"))
            
            self.assertTrue(TeamCode.isValid("  sz13"))
            self.assertTrue(TeamCode.isValid("sz13 "))
            self.assertTrue(TeamCode.isValid(" sz13 "))
            
        def testNewCode(self):
            counts = defaultdict(int)
            codes = []
            while True:
                c = TeamCode.newCode(codes)
                if c is None:
                    break
                codes.append(c)
                counts[c] += 1
            
            # This checks that MAX_TRIES is sufficiently large to get
            # most of the codes before newCode() gives up
            self.assertTrue(len(codes) >= 0.9 * TeamCode.maxUniqueCodes())
            
            # Check that no duplicate codes were generated
            for v in counts.itervalues():
                self.assertTrue(v <= 1)
        
        def testWordifyUnwordify(self):
            for _ in xrange(1000):
                c = TeamCode.newCode()
                self.assertEqual(c, TeamCode.unwordify(TeamCode.wordify(c)))
    
    unittest.main()  # run the unit tests
    sys.exit(0)
