"""This is my attempt at making a doc viewer/editor in dash

- want to upload/store a document with some text (pdf, doc, md, etc)
- want to view the document with various formats (or none)
- want to edit the (unformatted) text and track/see changes (formated)
  - want to commit changes
- want to 

"""
from devtools import debug
from dataclasses import dataclass, field
from typing import Optional
from typing_extensions import Self

class TextChangesTracker(object):
    _special_token = '`'# '<PBR>'
    # WARNING: we're assuming special token is single char and no entering string will keep it as non-special
    
    """
    A base class containing a piece of text that can be manipulated in sequence
    and we can get back the original text or latest, as well as some formatting 
    that resembles 'track changes'
    """
    def __init__(self, text: str):
        # this piece of text is the original one we'll return, but it won't remain stored here
        if self._special_token in text:
            print(f"WARNING: replacing instances of our reserved token {self._special_token} with '")
            text = text.replace("`", "'")        
        self._text: str = text
        
    @property
    def original_text(self) -> str:
        # view of original text
        raise NotImplementedError
    
    @property
    def current_text(self) -> str:
        # view of current text
        raise NotImplementedError
    
    def insert(self, chars: str, start: int) -> str:
        # insert chars at starting position (returns self for chaining of the method)
        raise NotImplementedError
    
    def remove(self, start: int, end: Optional[int]) -> str:
        # remove char(s) at starting position up to end if specified (returns self for chaining of the method)
        raise NotImplementedError
    
    def __repr__(self):
        return f'{self.__class__.__name__}(_text={self._text})'
        
        
class TextChangesTrackerSet(TextChangesTracker):

    def __init__(self, text: str):
        super().__init__(text)
        self._insertions = set() # points out which current indices are insertions
        self._deletions = set() # points out which current indices are deletions
        # self._special_token = '<PBR>' # page break token to insert
        # NOTE: all tokens are single characters except special_token

    @property
    def original_text(self) -> str:
        # view of original text
        pass
        
    @property
    def current_text(self) -> str:
        # view of current text
        pass

    def __repr__(self):
        return f'{super().__repr__()[:-1]}, _insertions={self._insertions}, _deletions={self._deletions})'
    
    def insert(self, token: str, start: int) -> Self:
        # insert chars at starting position (returns self for chaining of the method)
        # assert len(chars) == 1 unless == '<PBR>'?
        if len(token) > 1:
            for i, c in enumerate(token):
                # i is like offset of cursor, and after any insertion we move cursor ahead by 1
                self.insert(token=c, start=start+i)
        else:
            assert 0 <= start <= len(self._text)
            if start in self._deletions and self._text[start] == token:
                # cancel out previous deletion
                self._deletions.remove(start)
            else:
                # otherwise insert it, updating all things ahead of it
                self._text = self._text[:start] + token + self._text[start:]
                # TODO: not so efficient!
                self._deletions = {i if i < start else i + 1 for i in self._deletions}
                self._insertions = {i if i < start else i + 1 for i in self._insertions}
                self._insertions.add(start)
        return self
    
    def remove(self, start: int, end: Optional[int] = None) -> str:
        # remove char(s) at starting position up to end if specified (returns self for chaining of the method)
        if end is not None and start < end:
            i = 0
            for _ in range(start, end):
                # s moves up like a cursor
                n = len(self._text)
                self.remove(start=start+i, end=None)
                if len(self._text) == n - 1:
                    # we've deleted an inserted token, so keep cursor where it is
                    pass
                else:
                    # we have not changed the underlying _text sequence, so move cursor ahead
                    i += 1
        else:
            assert 0 <= start <= len(self._text)
            if start in self._deletions:
                # do nothing, as re-deleting is allowed
                pass
            elif start in self._insertions: # but not in deletions
                # cancel out previous insertion
                self._text = self._text[:start] + self._text[start+1:]
                # TODO: not so efficient!
                self._deletions = {i if i < start else i - 1 for i in self._deletions}
                self._insertions.remove(start)
                self._insertions = {i if i < start else i - 1 for i in self._insertions}
            else: # neither in insertions nor in deletions
                # add as new deletion
                # TODO: not so efficient!
                self._deletions.add(start)
        return self
    

if __name__ == "__main__":
    tc = TextChangesTrackerSet('I like you')
    debug(tc)
    debug(tc.remove(2, 2 + len('like')))
    debug(tc.insert('luv', 2))
    # debug(tc.remove(3)) #u
    # debug(tc.remove(3)) #v
    # equivalently:
    debug(tc.remove(3, 3 + len('uv')))
    debug(tc.insert('ove', 3))
    debug(tc.insert('!', 13))
