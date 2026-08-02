from trie_impl import *


t = Trie(); t.insert('apple'); assert t.search('apple')==True; assert t.search('app')==False; assert t.starts_with('app')==True; t.insert('app'); assert t.search('app')==True

t = Trie(); t.insert('a'); assert t.starts_with('a')==True; assert t.starts_with('ab')==False; t.insert('ab'); assert t.search('ab')==True

t = Trie(); t.insert('hello'); t.insert('hell'); assert t.search('hell')==True; assert t.search('hello')==True; assert t.starts_with('he')==True