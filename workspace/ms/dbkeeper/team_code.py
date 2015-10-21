#!/usr/bin/python

from random import randint, getrandbits

#----------------------------------------------------------------------------
class TeamPassCode(object):
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

    
    CODE_LENGTH  = 3  # Max # of codes = 26 * 26 = 626  
    CHECK_LENGTH = 2
    LENGTH = CODE_LENGTH + CHECK_LENGTH  # length in chars of the whole code
    
    MAX_TRIES = 5000  # Number of attempts at finding a unique code

    @staticmethod
    def maxUniqueCodes():
        return len(TeamPassCode.CHAR_LETTERS)**TeamPassCode.CODE_LENGTH
    
    @staticmethod
    def newPassCode(existingCodes=None):
        """ Create a random code.
            existingCodes is an optional list of codes to avoid.  If provided,
            newCode() will guarantee returning a code not in the list (if it can),
            or None (if it can't find one after MAX_TRIES).
            The maximum number of unique codes is len(CHAR_LETTERS)**CODE_LENGTH.
            existingCodes must be properly in lower case.
        """
        code = TeamPassCode._genCode()
        count = 1
        if existingCodes is not None:
            while code in existingCodes:
                code = TeamPassCode._genCode()
                count += 1
                if count >= TeamPassCode.MAX_TRIES:
                    return None
        return code
    
    @staticmethod
    def _genCode():
        code = ""
        n = 0
        for _ in range(TeamPassCode.CODE_LENGTH):
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
        return len(code) == (TeamPassCode.LENGTH) and \
               sum([ord(n) for n in code[0:TeamPassCode.CODE_LENGTH]]) % 16 == int(code[2:])
    
    @staticmethod
    def wordify(code):
        """ Convert code into words.
            If the code is badly formed or otherwise unconvertible,
            return an empty string.  The code does not need to be
            valid in order to wordify.  As long as the check number
            is in the valid range, words will be returned.
        """
        if len(code) != TeamPassCode.LENGTH:
            return ""
        words = ""
        try:
            code = code.strip().lower()
            for c in code[0:TeamPassCode.CODE_LENGTH]:
                words += TeamPassCode.CALL_LETTERS[ord(c) - ord('a')] + " "
            words += TeamPassCode.NUMBER_WORDS[int(code[TeamPassCode.CODE_LENGTH:])]
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
        if len(words) != TeamPassCode.CODE_LENGTH + 1:
            return None
        code = ""
        try:
            for i in range(TeamPassCode.CODE_LENGTH):
                code += TeamPassCode.LETTER[words[i]]
            code += "{:02}".format(TeamPassCode.NUMBER[words[-1]])
        except KeyError:
                return None
        if TeamPassCode.isValid(code):
            return code
        return None

class TeamRegCode(object):
    """ Create a unique Team registration code for authentication.
        The BRATA will send the reg_code with each message, so the
        MS can determine the validity of the sender.
    """
    MAX_TRIES   = 10  # dups are a low-probability event with 64 random bits
    LENGTH      = 16          # characters
    CODE_BITS   = LENGTH * 4  # bits
    
    @staticmethod
    def newRegCode(existingCodes=None):
        """ Create a random code.
            existingCodes is an optional list of codes to avoid.  If provided,
            generateRegCode() will guarantee returning a code not in the list
            (if it can), or None (if it can't find one after MAX_TRIES).
            The maximum number of unique codes is 2**CODE_LENGTH.
            The RegCode is a sequence of bits represented as a hexadecimal string
            literal.
        """
        for _ in range(TeamRegCode.MAX_TRIES):
            formatStr = "{:0" + str(TeamRegCode.LENGTH) + "x}"
            code = formatStr.format(getrandbits(TeamRegCode.CODE_BITS))
            if code not in existingCodes:
                return code
        return None
        

#----------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    import unittest
    from collections import defaultdict
    
    class TeamPassCodeTestCase(unittest.TestCase):
        def testIsValid(self):
            # Check that check digits work properly
            # TODO: generate some codes with valid check digits to test
            self.assertTrue(TeamPassCode.isValid("aaa03"))
            self.assertTrue(TeamPassCode.isValid("ab03")) # note that check value does not prevent transposing of chars
            self.assertTrue(TeamPassCode.isValid("ba03"))
            self.assertTrue(TeamPassCode.isValid("sz13"))
            self.assertFalse(TeamPassCode.isValid("sz12"))
            self.assertFalse(TeamPassCode.isValid("sz14"))
            
            # Check for ignore leading/trailing whitespace
            self.assertTrue(TeamPassCode.isValid("  sz13"))
            self.assertTrue(TeamPassCode.isValid("sz13 "))
            self.assertTrue(TeamPassCode.isValid(" sz13 "))
            
        def testNewCode(self):
            counts = defaultdict(int)
            codes = []
            while True:
                c = TeamPassCode.newCode(codes)
                if c is None:
                    break
                codes.append(c)
                counts[c] += 1
            
            # This checks that MAX_TRIES is sufficiently large to get
            # most of the codes before newCode() gives up
            self.assertTrue(len(codes) >= 0.9 * TeamPassCode.maxUniqueCodes())
            
            # Check that no duplicate codes were generated
            for v in counts.itervalues():
                self.assertTrue(v <= 1)
        
        def testWordifyUnwordify(self):
            for _ in xrange(1000):
                c = TeamPassCode.newCode()
                self.assertEqual(c, TeamPassCode.unwordify(TeamPassCode.wordify(c)))
    
    unittest.main()  # run the unit tests
    sys.exit(0)
