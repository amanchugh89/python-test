# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 16:12:20 2015

@author: aman


Programming task
================

The following is an implementation of a simple Named Entity Recognition (NER).
NER is concerned with identifying place names, people names or other special
identifiers in text.

Here we make a very simple definition of a named entity: A sequence of
at least two consecutive capitalized words. E.g. "Los Angeles" is a named
entity, "our hotel" is not.

While the implementation passes the Unit test, it suffers from bad structure and
readability. It is your task to rework *both* the implementation and the Unit
test. You are expected to come up with a better interface than the one presented
here.

Your code will be evaluated on:
- Readability: Is naming intuitive? Are there comments where necessary?
- Structure: Is functionality grouped into functions or classes in a way that
enables reusability?
- Testability: Is it easy to test individual components of your algorithm? This
is a good indicator of good interface design.
- Bonus: Functional programming. Demonstrate how you have applied principles of
functional programming to improve this code.

If you want, explain reasons for changes you've made in comments.

Note that you don't have to improve the actual Named Entity Recognition
algorithm itself - the focus is on code quality.
"""

import re
import unittest

###############################################################################
## BEGIN of NamedEntityRecognizer Class
###############################################################################

class NamedEntityRecognizer:
    """
    The following is an implementation of a simple Named Entity Recognition (NER).
    NER is concerned with identifying place names, people names or other special
    identifiers in text.
    """

# Buffer to store current named entity. Will store two consecutive tokens
    # for Named Entity recognition.
    # Its cleared off if :
    #  - A named entity is found: So as to refresh for next named Entity
    #  - If one token is not followed by another token consecutively.
    word_buffer = []

    # Regular expression for matching a token at the beginning of a sentence
    token_re = re.compile(r"([a-z]+)\s*(.*)$", re.I)

    # Regular expression to recognize an token (Uppercase word)
    uppercase_re = re.compile(r"[A-Z][a-z]*$")

    def __init__(self, text):
        """
        Initializer to take in the input text and perform 
        NamedEntity-Recognition on it.
        """
        self.text = text

    def get_matched_named_entities(self):
        """
        Here we linearly scan the text and pick up tokens one by one and check
        if we have found a named entity.
        It works in two phases:
          - Popping token [pop_token()] : 
              This picks up the next token at the begenning of
              the text and checks if its a Valid token. A valid token is added
              to the word_buffer. An invalid token is ignored and the 
              word_buffer is refreshed.
          - Check if we have a Named Entity [pop_token()]:
              Here we keep track of the word_buffer. If we have obtained a 
              bigram we return it as a Named Entity and refresh the word_buffer
              for next Named Entity Recognition.
              
        @return: set([namedentity strings]). Empty set in case no entities are found.
        """
        entities = set()
        while True:
            token, self.text = self.pop_token()
            if not token:
                entity = self.has_named_entity()
                if entity:
                    entities.add(entity)
                break
            entity = self.has_named_entity()
            if entity:
                entities.add(entity)

        return entities

    def pop_token(self):
        """
        Take the first token off the beginning of text. If its first letter is
        capitalized, remember it in word buffer - we may have a named entity on our
        hands!!
    
        @return: Tuple (token, remaining_text). Token is None in case text is empty
        """
        token_match = NamedEntityRecognizer.token_re.match(self.text)
        if token_match:
            token = token_match.group(1)

            if NamedEntityRecognizer.uppercase_re.match(token):
                self.word_buffer.append(token)
            else:
                NamedEntityRecognizer.word_buffer = []
            return token, token_match.group(2)

        return None, self.text

    def has_named_entity(self):
        """
        Return a named entity, if we have assembled one in the current buffer.
        Returns None if we have to keep searching.
        """
        if len(NamedEntityRecognizer.word_buffer) >= 2:
            named_entity = " ".join(NamedEntityRecognizer.word_buffer)
            NamedEntityRecognizer.word_buffer = []
            return named_entity


###############################################################################
## END of NamedEntityRecognizer Class
###############################################################################

class NamedEntityTestCase(unittest.TestCase):
    """
    Adding couple of test scenario and corner cases just to be sure
    everyting is working as expected.
    """

    def test_ner_extraction(self):
        text = "When we went to Los Angeles last year we visited the Hollywood Sign"
        entities = NamedEntityRecognizer(text).get_matched_named_entities()
        self.assertEqual(set(["Los Angeles", "Hollywood Sign"]), entities)

    def test_negetive_case(self):
        text = "no named entities here"
        entities = NamedEntityRecognizer(text).get_matched_named_entities()
        self.assertEqual(set([]), entities)

    def test_overlapping_case(self):
        text = "All Named Entities Here"
        entities = NamedEntityRecognizer(text).get_matched_named_entities()
        self.assertEqual(set(['All Named', 'Entities Here']), entities)

###############################################################################
## END of Test Cases
###############################################################################


if __name__ == "__main__":
    unittest.main()


###############################################################################
## END of Code
###############################################################################

