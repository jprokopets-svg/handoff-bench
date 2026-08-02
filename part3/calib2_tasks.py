#!/usr/bin/env python3
"""part3/calib2_tasks.py — Handoff Part III Round-2 calibration candidates.

10 tasks in the harder class per Fable's ruling 1 (Buzz event 3a021bab):
multi-stage / multi-file / strict-contract implementations, benchmarked
against V2's harder half (pooled success <=60%: n_queens 7%, word_break 43%,
regex_parser 53%, serialize_tree 53%, max_path_sum 60%).

Disjoint from: the V2 task set (regex_parser, n_queens, median_stream,
word_break, median_two_sorted, serialize_tree, max_path_sum, merge_k_lists),
the 5 Stage 0 tasks (two_sum, valid_palindrome, fibonacci, count_bits,
climbing_stairs), and the 12 Round-1 candidates (atoi_clone,
longest_substring_no_repeat, max_area_container, interval_merge, rotate_image,
valid_bst, lru_cache, trie_impl, decode_string, course_schedule,
min_window_substring, find_duplicate_number).

Each task's test file was validated against a reference implementation before
any API budget was spent (see CALIBRATION2_REPORT.md).
"""

CALIB2_TASKS = [
    {
        "name": "mini_brainfuck",
        "prompt": ("Implement a Brainfuck interpreter. brainfuck(code, input_str) runs the program and "
                   "returns all output characters concatenated. Tape: 30,000 cells, initially 0; cell "
                   "values are integers with NO wraparound. Data pointer starts at cell 0. Commands: "
                   "> move pointer right; < move left; + increment current cell; - decrement; . output "
                   "chr(current cell); , read the next char of input_str (ord value; if input exhausted, "
                   "set the cell to 0). [ jumps forward past the matching ] if the current cell is 0; "
                   "] jumps back to just after the matching [ if the current cell is not 0. Any other "
                   "character is ignored. Raise ValueError if brackets are unbalanced."),
        "func_sig": "def brainfuck(code: str, input_str: str = \"\") -> str:",
        "tests": [
            "def _raises(fn):\n    try:\n        fn()\n        return False\n    except ValueError:\n        return True",
            "assert brainfuck('') == ''",
            "assert brainfuck('+++.') == chr(3)",
            "assert brainfuck('++[>+<-]>.') == chr(2)",
            "assert brainfuck('+++[>+.<-]') == chr(1) + chr(2) + chr(3)",
            "assert brainfuck('+++[->++<]>.' ) == chr(6)",
            "assert brainfuck('++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.') == 'Hello World!\\n'",
            "assert brainfuck(',.', 'Z') == 'Z'",
            "assert brainfuck(',+++.', 'B') == 'E'",
            "assert brainfuck('+++.junk-+-', '') == chr(3)",
            "assert _raises(lambda: brainfuck('['))",
            "assert _raises(lambda: brainfuck(']'))",
            "assert _raises(lambda: brainfuck('++[>++'))",
        ],
    },
    {
        "name": "json_parser",
        "prompt": ("Implement a STRICT JSON parser. parse_json(text) parses a single JSON value and returns "
                   "the Python equivalent (dict/list/str/int/float/bool/None). Must accept: null, true, "
                   "false; integers and floats with optional minus sign, fraction and exponent (e.g. -0.5, "
                   "1e10, 1.5E-3); strings with escapes \\\" \\\\ \\/ \\b \\f \\n \\r \\t \\uXXXX (exactly 4 hex "
                   "digits); nested objects and arrays; surrounding whitespace. MUST REJECT: any trailing "
                   "content after the value; unclosed braces/brackets/strings; invalid escapes; single "
                   "quotes; trailing commas; numbers with leading zeros (e.g. 01); numbers like .5 or 1. "
                   "or +1; raw control characters inside strings; empty input; multiple top-level values. "
                   "Raise ValueError on any invalid input."),
        "func_sig": "def parse_json(text: str) -> object:",
        "tests": [
            "def _raises(fn):\n    try:\n        fn()\n        return False\n    except ValueError:\n        return True",
            "assert parse_json('123') == 123",
            "assert parse_json('-0.5') == -0.5",
            "assert parse_json('123.456') == 123.456",
            "assert parse_json('[-0.5, 1e10, 1.5E-3, 0, -7]') == [-0.5, 1e10, 1.5E-3, 0, -7]",
            "assert parse_json('{\"a\": 1, \"b\": [true, null, \"x\"]}') == {'a': 1, 'b': [True, None, 'x']}",
            "assert parse_json('{\"a\":{\"b\":[1,[2,3],{\"c\":null}]}}') == {'a': {'b': [1, [2, 3], {'c': None}]}}",
            "assert parse_json('\"\\\\u0041\\\\n\\\\t\\\\\\\"\"') == 'A\\n\\t\\\"'",
            "assert _raises(lambda: parse_json(''))",
            "assert _raises(lambda: parse_json('{\"a\": 1} extra'))",
            "assert _raises(lambda: parse_json('01'))",
            "assert _raises(lambda: parse_json('[1,]'))",
            "assert _raises(lambda: parse_json('{\"a\":1,}'))",
            "assert _raises(lambda: parse_json(\"'x'\"))",
            "assert _raises(lambda: parse_json('1.'))",
            "assert _raises(lambda: parse_json('.5'))",
            "assert _raises(lambda: parse_json('+1'))",
            "assert _raises(lambda: parse_json('\"unclosed'))",
        ],
    },
    {
        "name": "regex_matcher",
        "prompt": ("Implement a regular expression engine. full_match(pattern, text) returns True iff the "
                   "ENTIRE text matches the pattern. Supported syntax: literal characters; '.' matches any "
                   "single character; character classes [abc], ranges [a-z], negation [^...], and escaped "
                   "metacharacters inside classes like [\\]]; quantifiers on the preceding atom: * (zero or "
                   "more), + (one or more), ? (zero or one); groups (...) with alternation | (e.g. (ab|cd) "
                   "matches ab or cd); anchors ^ (start of text) and $ (end of text); backslash escapes "
                   "\\., \\*, \\\\, \\^, \\$ etc. for literal metacharacters. Matching is greedy but must "
                   "backtrack to allow the whole pattern to match (e.g. 'a*ab' must match 'aaab'). No "
                   "backreferences, no lookahead, no {m,n}. Raise ValueError on malformed patterns: "
                   "unclosed group, unclosed class, or a quantifier with no preceding atom."),
        "func_sig": "def full_match(pattern: str, text: str) -> bool:",
        "tests": [
            "def _raises(fn):\n    try:\n        fn()\n        return False\n    except ValueError:\n        return True",
            "assert full_match('abc', 'abc') == True",
            "assert full_match('abc', 'abd') == False",
            "assert full_match('a.c', 'abc') == True",
            "assert full_match('a.c', 'ac') == False",
            "assert full_match('ab*c', 'ac') == True",
            "assert full_match('ab*c', 'abbbc') == True",
            "assert full_match('ab*c', 'abbd') == False",
            "assert full_match('ab+c', 'abc') == True",
            "assert full_match('ab+c', 'ac') == False",
            "assert full_match('colou?r', 'color') == True",
            "assert full_match('colou?r', 'colour') == True",
            "assert full_match('[a-c]x', 'bx') == True",
            "assert full_match('[a-c]x', 'dx') == False",
            "assert full_match('[^0-9]', 'a') == True",
            "assert full_match('[^0-9]', '5') == False",
            "assert full_match('(ab|cd)e', 'abe') == True",
            "assert full_match('(ab|cd)e', 'cde') == True",
            "assert full_match('(ab|cd)e', 'ade') == False",
            "assert full_match('(a(b|c))', 'ab') == True",
            "assert full_match('^abc$', 'abc') == True",
            "assert full_match('^abc$', 'abcd') == False",
            "assert full_match('^a', 'a') == True",
            "assert full_match('a$', 'ba') == False",
            "assert full_match('a\\\\.b', 'a.b') == True",
            "assert full_match('a\\\\.b', 'axb') == False",
            "assert full_match('\\\\*', '*') == True",
            "assert full_match('(ab)*', 'abab') == True",
            "assert full_match('(ab)*', 'aba') == False",
            "assert full_match('a*ab', 'aaab') == True",
            "assert _raises(lambda: full_match('(ab', 'x'))",
            "assert _raises(lambda: full_match('*a', 'x'))",
            "assert _raises(lambda: full_match('[ab', 'x'))",
        ],
    },
    {
        "name": "graph_serializer",
        "prompt": ("Implement a serializer that converts a Python object graph to a string and back, "
                   "PRESERVING shared references and cycles. Supported types: int, float, bool, None, str, "
                   "list, and dict with string keys. encode(obj) returns a string such that "
                   "decode(encode(x)) equals x; if the same object appears multiple times in the input "
                   "(shared reference), decode must return the SAME object instance (identity preserved, "
                   "use 'is' to check); cycles (e.g. a list containing itself, or a dict whose value is "
                   "itself) must round-trip with the cycle preserved. The exact wire format is your "
                   "choice but encode and decode must agree. Raise ValueError on malformed input in "
                   "decode, or if encode is given an unsupported type."),
        "func_sig": "def encode(obj: object) -> str:\ndef decode(s: str) -> object:",
        "tests": [
            "assert decode(encode([1, 2.5, True, None, 'x', {'a': [1]}])) == [1, 2.5, True, None, 'x', {'a': [1]}]",
            "assert decode(encode([])) == []",
            "assert decode(encode({})) == {}",
            "assert decode(encode('')) == ''",
            "assert decode(encode('h\\u00e9llo\\u2192\\u4e16\\u754c')) == 'h\\u00e9llo\\u2192\\u4e16\\u754c'",
            "inner = [1, 2]; obj = [inner, inner]; out = decode(encode(obj)); assert out[0] is out[1]",
            "lst = [1]; lst.append(lst); out = decode(encode(lst)); assert out[0] == 1 and out[1] is out",
            "d = {}; d['self'] = d; out = decode(encode(d)); assert out['self'] is out",
            "v = [1]; d = {'a': v, 'b': v}; out = decode(encode(d)); assert out['a'] is out['b']",
        ],
    },
    {
        "name": "avl_tree",
        "prompt": ("Implement an AVL (self-balancing) binary search tree. AVLTree has insert(key: int), "
                   "delete(key: int), contains(key: int) -> bool, and a public attribute 'root' (the root "
                   "node or None). After every insert/delete the tree must be height-balanced: for every "
                   "node the heights of its left and right subtrees differ by at most 1, maintained by "
                   "single and double rotations. Each node has attributes val, left, right. Duplicates: "
                   "inserting an existing key is a no-op (no duplicate nodes). Deleting a missing key is "
                   "a no-op. insert and delete return None."),
        "func_sig": "class AVLTree:\n    def __init__(self): ...\n    def insert(self, key: int) -> None: ...\n    def delete(self, key: int) -> None: ...\n    def contains(self, key: int) -> bool: ...",
        "tests": [
            "def _h(n):\n    return 0 if n is None else 1 + max(_h(n.left), _h(n.right))",
            "def _bal(t):\n    def walk(n):\n        if n is None:\n            return True\n        if abs(_h(n.left) - _h(n.right)) > 1:\n            return False\n        return walk(n.left) and walk(n.right)\n    return walk(t.root)",
            "def _sorted_keys(t):\n    out = []\n    def walk(n):\n        if n is None:\n            return\n        walk(n.left); out.append(n.val); walk(n.right)\n    walk(t.root); return out",
            "t = AVLTree();\nfor k in range(1, 101):\n    t.insert(k)\n    assert _bal(t)\nassert _sorted_keys(t) == list(range(1, 101))",
            "t = AVLTree();\nfor k in range(100, 0, -1):\n    t.insert(k)\n    assert _bal(t)\nassert t.contains(1) and t.contains(100) and not t.contains(101)",
            "t = AVLTree();\nfor k in [7, 3, 11, 1, 5, 9, 13, 0, 2, 4, 6, 8, 10, 12, 14]:\n    t.insert(k)\nassert _bal(t)\nassert _sorted_keys(t) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]",
            "t = AVLTree();\nfor k in range(1, 21):\n    t.insert(k)\nfor k in [10, 5, 1, 20, 15, 7, 13]:\n    t.delete(k)\n    assert _bal(t)\nassert _sorted_keys(t) == [2, 3, 4, 6, 8, 9, 11, 12, 14, 16, 17, 18, 19]",
            "t = AVLTree(); t.insert(5); t.insert(5); assert _sorted_keys(t) == [5]; t.delete(5); assert t.root is None and not t.contains(5)",
            "t = AVLTree(); t.delete(9); assert t.root is None",
        ],
    },
    {
        "name": "edit_distance_ops",
        "prompt": ("Return a MINIMAL sequence of edit operations transforming string a into string b, using "
                   "only: ('delete', i) removes the character at index i; ('insert', i, c) inserts "
                   "character c at index i; ('sub', i, c) replaces the character at index i with c. "
                   "Operations apply sequentially to the CURRENT string (indices refer to the state after "
                   "all prior operations). The number of operations must equal the Levenshtein distance "
                   "(uniform cost 1 for delete/insert/substitute). If a == b, return []."),
        "func_sig": "def min_edit_ops(a: str, b: str) -> list[tuple]:",
        "tests": [
            "def _lev(a, b):\n    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]\n    for i in range(len(a) + 1):\n        dp[i][0] = i\n    for j in range(len(b) + 1):\n        dp[0][j] = j\n    for i in range(1, len(a) + 1):\n        for j in range(1, len(b) + 1):\n            dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + (0 if a[i-1] == b[j-1] else 1))\n    return dp[len(a)][len(b)]",
            "def _replay(a, ops):\n    s = list(a)\n    for op in ops:\n        if op[0] == 'delete':\n            del s[op[1]]\n        elif op[0] == 'insert':\n            s.insert(op[1], op[2])\n        else:\n            s[op[1]] = op[2]\n    return ''.join(s)",
            "ops = min_edit_ops('kitten', 'sitting'); assert len(ops) == _lev('kitten', 'sitting') and _replay('kitten', ops) == 'sitting'",
            "ops = min_edit_ops('', 'abc'); assert len(ops) == 3 and _replay('', ops) == 'abc'",
            "ops = min_edit_ops('abc', ''); assert len(ops) == 3 and _replay('abc', ops) == ''",
            "ops = min_edit_ops('abc', 'abc'); assert ops == [] and _replay('abc', ops) == 'abc'",
            "ops = min_edit_ops('sunday', 'saturday'); assert len(ops) == _lev('sunday', 'saturday') and _replay('sunday', ops) == 'saturday'",
            "ops = min_edit_ops('intention', 'execution'); assert len(ops) == _lev('intention', 'execution') and _replay('intention', ops) == 'execution'",
            "ops = min_edit_ops('cat', 'cut'); assert len(ops) == 1 and _replay('cat', ops) == 'cut'",
        ],
    },
    {
        "name": "calculator_parser",
        "prompt": ("Evaluate an infix arithmetic expression and return the numeric result as a float. "
                   "Operators, highest to lowest precedence: ** (right-associative, highest); unary minus "
                   "and unary plus; then * / % (left-associative); then + - (left-associative, lowest). "
                   "Parentheses group. Numbers may be integers or decimals (a digit must precede the "
                   "decimal point: 3.5, 0.5). Whitespace is allowed anywhere. Division is float division. "
                   "Division or modulo by zero raises ValueError. Unbalanced parentheses, an empty "
                   "expression, two adjacent operands without an operator, a trailing operator, or an "
                   "invalid token raise ValueError. Unary minus binds tighter than * / but looser than **: "
                   "-2**2 == -(2**2) == -4.0, and 2**-1 == 0.5."),
        "func_sig": "def evaluate(expr: str) -> float:",
        "tests": [
            "def _raises(fn):\n    try:\n        fn()\n        return False\n    except ValueError:\n        return True",
            "assert evaluate('2 + 3 * 4') == 14.0",
            "assert evaluate('(2 + 3) * 4') == 20.0",
            "assert evaluate('2 ** 3 ** 2') == 512.0",
            "assert evaluate('-2 ** 2') == -4.0",
            "assert evaluate('2 ** -1') == 0.5",
            "assert evaluate('10 % 3') == 1.0",
            "assert evaluate('-7 % 3') == 2.0",
            "assert evaluate('3.5 * 2') == 7.0",
            "assert evaluate('7 / 2') == 3.5",
            "assert evaluate('  - 5 + 2 ') == -3.0",
            "assert evaluate('2 * -3') == -6.0",
            "assert evaluate('(1 + 2) ** (3 - 1)') == 9.0",
            "assert evaluate('+3') == 3.0",
            "assert _raises(lambda: evaluate('1 / 0'))",
            "assert _raises(lambda: evaluate('1 % 0'))",
            "assert _raises(lambda: evaluate('((1+2)'))",
            "assert _raises(lambda: evaluate(''))",
            "assert _raises(lambda: evaluate('1 2'))",
            "assert _raises(lambda: evaluate('1+'))",
            "assert _raises(lambda: evaluate('2**'))",
            "assert _raises(lambda: evaluate('a'))",
        ],
    },
    {
        "name": "critical_path",
        "prompt": ("Given task durations (mapping task id -> duration) and dependency pairs (a, b) meaning "
                   "task a must complete before task b can start, return (project_duration, critical_path). "
                   "project_duration is the minimum time to finish ALL tasks assuming unlimited parallel "
                   "execution and no idle time. critical_path is a list of task ids on ONE longest path "
                   "from any source (task with no prerequisites) to any sink (task with no dependents); the "
                   "sum of durations along the path must equal project_duration. Tasks with no "
                   "prerequisites may start at time 0. If the dependency graph contains a cycle, raise "
                   "ValueError. If durations is empty, return (0.0, [])."),
        "func_sig": "def critical_path(durations: dict, deps: list) -> tuple:",
        "tests": [
            "def _valid(durations, deps, dur, path):\n    if abs(dur - sum(durations[t] for t in path)) > 1e-9:\n        return False\n    pos = {t: i for i, t in enumerate(path)}\n    for a, b in deps:\n        if a in pos and b in pos and pos[a] > pos[b]:\n            return False\n    return True",
            "d, durs = critical_path({}, []); assert d == 0.0 and durs == []",
            "d, p = critical_path({7: 3.5}, []); assert d == 3.5 and p == [7]",
            "d, p = critical_path({1: 3, 2: 2, 3: 4}, []); assert d == 4.0 and _valid({1: 3, 2: 2, 3: 4}, [], d, p)",
            "dur = {1: 2, 2: 4, 3: 3, 4: 6, 5: 2, 6: 1}\ndeps = [(1, 2), (1, 3), (2, 4), (3, 4), (4, 5), (3, 6), (5, 6)]\nd, p = critical_path(dur, deps); assert d == 15.0 and _valid(dur, deps, d, p)",
            "dur = {1: 5, 2: 7}; d, p = critical_path(dur, []); assert d == 7.0 and _valid(dur, [], d, p)",
            "dur = {1: 1, 2: 1}\ndef _cyc():\n    return critical_path(dur, [(1, 2), (2, 1)])\ntry:\n    _cyc(); assert False\nexcept ValueError:\n    pass",
            "dur = {1: 1, 2: 1, 3: 1}\nd, p = critical_path(dur, [(1, 2), (2, 3)]); assert d == 3.0 and _valid(dur, [(1, 2), (2, 3)], d, p)",
            "dur = {1: 2, 2: 5, 3: 1, 4: 2}\nd, p = critical_path(dur, [(1, 3), (2, 3), (3, 4)]); assert d == 8.0 and _valid(dur, [(1, 3), (2, 3), (3, 4)], d, p)",
        ],
    },
    {
        "name": "text_justification",
        "prompt": ("Format a list of words into fully-justified lines of exactly max_width characters. "
                   "Greedy packing: add words to the current line while they fit, where words on a line "
                   "are separated by at least one space. Each NON-last line is fully justified: spaces are "
                   "distributed between the gaps, with the extra spaces going one per gap from left to "
                   "right (the leftmost gaps get the extra spaces first). The LAST line is left-justified: "
                   "single spaces between words, padded with trailing spaces to max_width. A line "
                   "containing a single word is left-justified with trailing padding. Every word is "
                   "guaranteed shorter than max_width. Return the list of justified lines."),
        "func_sig": "def full_justify(words: list[str], max_width: int) -> list[str]:",
        "tests": [
            "assert full_justify(['This', 'is', 'an', 'example', 'of', 'text', 'justification.'], 16) == ['This    is    an', 'example  of text', 'justification.  ']",
            "assert full_justify(['This', 'is', 'an', 'example', 'of', 'text', 'justification.'], 15) == ['This    is   an', 'example of text', 'justification. ']",
            "assert full_justify(['hello'], 10) == ['hello     ']",
            "assert full_justify(['a', 'b', 'c'], 3) == ['a b', 'c  ']",
            "assert full_justify(['ab', 'cd'], 5) == ['ab cd']",
            "assert full_justify(['a', 'b', 'c', 'd'], 7) == ['a b c d']",
            "assert full_justify(['What', 'must', 'be', 'acknowledgment', 'shall', 'be'], 16) == ['What   must   be', 'acknowledgment  ', 'shall be        ']",
            "assert full_justify(['Science', 'is', 'what', 'we', 'understand', 'well', 'enough', 'to', 'explain', 'to', 'a', 'computer.', 'Art', 'is', 'everything', 'else', 'we', 'do'], 20) == ['Science  is  what we', 'understand      well', 'enough to explain to', 'a  computer.  Art is', 'everything  else  we', 'do                  ']",
        ],
    },
    {
        "name": "token_bucket_limiter",
        "prompt": ("Implement a token bucket rate limiter. TokenBucket(capacity, refill_rate): capacity is "
                   "the maximum number of tokens the bucket can hold; refill_rate is the number of tokens "
                   "added per unit time (continuous refill). allow(tokens=1.0, now=None) -> bool: if 'now' "
                   "is provided it is the current time (deterministic testing); otherwise use a monotonic "
                   "internal clock. The bucket refills continuously from the last time it was observed, up "
                   "to capacity (never above). If the bucket holds at least 'tokens', deduct them and "
                   "return True; otherwise return False and deduct NOTHING. tokens > capacity always "
                   "returns False. tokens <= 0 returns True and deducts nothing. A freshly constructed "
                   "bucket starts FULL (capacity tokens)."),
        "func_sig": "class TokenBucket:\n    def __init__(self, capacity: float, refill_rate: float): ...\n    def allow(self, tokens: float = 1.0, now: float | None = None) -> bool: ...",
        "tests": [
            "tb = TokenBucket(5, 1.0); assert tb.allow(1, now=0.0); assert tb.allow(4, now=0.0); assert not tb.allow(1, now=0.0)",
            "tb = TokenBucket(5, 1.0); assert tb.allow(5, now=0.0); assert tb.allow(5, now=5.0); assert tb.allow(5, now=100.0); assert not tb.allow(5, now=100.0)",
            "tb = TokenBucket(5, 1.0); assert tb.allow(5, now=0.0); assert not tb.allow(1, now=0.0); assert tb.allow(1, now=1.0)",
            "tb = TokenBucket(2, 1.0); assert not tb.allow(3, now=0.0); assert tb.allow(2, now=0.0); assert not tb.allow(1, now=0.0)",
            "tb = TokenBucket(1, 1.0); assert tb.allow(0, now=0.0); assert tb.allow(-1, now=0.0); assert tb.allow(1, now=0.0)",
            "tb = TokenBucket(5, 1.0); assert tb.allow(3, now=0.0); assert tb.allow(3, now=1.0); assert not tb.allow(1, now=1.5)",
            "tb = TokenBucket(5, 0.5); assert tb.allow(5, now=0.0); assert tb.allow(1, now=2.0); assert not tb.allow(1, now=2.0)",
            "tb = TokenBucket(3, 2.0); assert tb.allow(3, now=0.0); assert not tb.allow(2, now=0.5); assert tb.allow(2, now=1.0); assert not tb.allow(1, now=1.0)",
        ],
    },
]
