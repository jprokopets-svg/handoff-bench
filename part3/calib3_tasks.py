#!/usr/bin/env python3
"""part3/calib3_tasks.py — Handoff Part III Round-3 calibration candidates.

Per Fable's Round-3 rulings (Buzz event 1885cf44):

Ruling 2 — KEEP the 4 in-band Round-2 survivors (regex_matcher,
calculator_parser, edit_distance_ops, graph_serializer), imported from
calib2_tasks.py; ADD 7 new candidates in the B-fresh-solve-fails class
(multi-file / stateful / strict-contract: interpreter with multi-statement
state, protocol state machine, concurrent structure with locking, strict
codecs, assembler+simulator, parser with strict rejection, ETL pipeline).

Disjoint from: the V2 task set, the 5 Stage 0 tasks, the 12 Round-1
candidates, and the 10 Round-2 candidates (all names verified unique in
CALIB3_UNIQUENESS check below).

Each new task's test file was validated against a reference implementation
(and against deliberately broken implementations) before any API budget was
spent — see .scratch/validate_calib3.py and CALIBRATION3_REPORT.md.

Seeds for Round 3: 313 and 515 (declared in CALIBRATION3_PREREG.md; burned,
excluded from confirmation). Round-3 runs use the confirmatory-family
representatives: gemini = google/gemini-2.5-pro (ruling 4), others unchanged.
"""

from calib2_tasks import CALIB2_TASKS  # noqa: E402

SURVIVORS = ("regex_matcher", "calculator_parser", "edit_distance_ops", "graph_serializer")

_NEW_TASKS = [
    {
        "name": "mini_interpreter",
        "prompt": ("Implement a tiny imperative programming language interpreter. "
                   "run_program(src, inputs=None) executes the program and returns the concatenated "
                   "output of all print statements (each printed value followed by a newline). "
                   "LANGUAGE: the program is a sequence of statements, one per line. Each statement is "
                   "one of: (1) assignment 'NAME = expr'; (2) 'print(expr)' — evaluates expr and appends "
                   "str(value) + newline to the output; (3) 'NAME = input()' — reads the next integer "
                   "from the inputs list (raise ValueError if exhausted); (4) 'if COND {' opens a block, "
                   "terminated by a line containing only '}'; the block executes iff COND is truthy "
                   "(nonzero); an optional 'else {' block may follow (either '}' then 'else {' on its own line, or the single line '} else {'); the else block executes iff COND is falsy (zero); "
                   "(5) 'while COND {' ... '}' — repeats while COND is truthy. Blocks nest arbitrarily "
                   "deep. EXPRESSIONS: integers; variable names; parentheses; binary operators with this "
                   "precedence (highest to lowest): '*', '/', '%' ; then '+', '-'; then comparisons "
                   "'==', '!=', '<', '<=', '>', '>=' (comparisons yield int 0 or 1). All operators are "
                   "left-associative. Division '/' and modulo '%' are integer operations; division by "
                   "zero raises ValueError. CONDITIONS are ints (0 = false, nonzero = true). ERRORS "
                   "(ValueError): undefined variable; division/modulo by zero; unbalanced parentheses or "
                   "braces; a stray '}' with no open block; a syntax error (unexpected token, missing "
                   "operator, trailing operator); input() with no inputs left. Program lines may have "
                   "leading/trailing whitespace; blank lines are skipped."),
        "func_sig": "def run_program(src: str, inputs: list | None = None) -> str:",
        "tests": [
            "def _raises(fn):\n    try:\n        fn()\n        return False\n    except ValueError:\n        return True",
            "assert run_program('x = 5\\nprint(x)') == '5\\n'",
            "assert run_program('print(2 + 3 * 4)') == '14\\n'",
            "assert run_program('print((2 + 3) * 4)') == '20\\n'",
            "assert run_program('print(10 % 3)') == '1\\n'",
            "assert run_program('print(20 / 4)') == '5\\n'",
            "assert run_program('x = 10\\ny = x - 3\\nprint(y)') == '7\\n'",
            "assert run_program('print(2 * 3 == 6)') == '1\\n'",
            "assert run_program('print(2 * 3 == 7)') == '0\\n'",
            "assert run_program('if 3 > 2 {\\nprint(1)\\n}') == '1\\n'",
            "assert run_program('if 0 {\\nprint(1)\\n} else {\\nprint(2)\\n}') == '2\\n'",
            "assert run_program('x = 0\\nwhile x < 3 {\\nx = x + 1\\nprint(x)\\n}') == '1\\n2\\n3\\n'",
            "assert run_program('x = 1\\nwhile x <= 10 {\\nprint(x)\\nx = x * 2\\n}') == '1\\n2\\n4\\n8\\n'",
            "assert run_program('x = input()\\nprint(x + 1)', [41]) == '42\\n'",
            "assert run_program('a = 1\\nb = 2\\nif a < b {\\nprint(a + b)\\n} else {\\nprint(0)\\n}') == '3\\n'",
            "assert run_program('x = 5\\nx = x * 2\\nprint(x)') == '10\\n'",
            "assert run_program('i = 0\\ns = 0\\nwhile i < 5 {\\ns = s + i\\ni = i + 1\\n}\\nprint(s)') == '10\\n'",
            "assert _raises(lambda: run_program('print(x)'))",
            "assert _raises(lambda: run_program('print(1 / 0)'))",
            "assert _raises(lambda: run_program('print(1 % 0)'))",
            "assert _raises(lambda: run_program('x = 1\\nif x {'))",
            "assert _raises(lambda: run_program('}'))",
            "assert _raises(lambda: run_program('print(1 2)'))",
            "assert _raises(lambda: run_program('print(1 +)'))",
            "assert _raises(lambda: run_program('print(x)', [1]))",
            "assert _raises(lambda: run_program('print((1)'))",
            "assert _raises(lambda: run_program('x = = 1'))",
        ],
    },
    {
        "name": "tcp_state_machine",
        "prompt": ("Implement a TCP connection state machine. TCPStateMachine() starts in state "
                   "'CLOSED'. handle(event) returns the new state string after the transition, and "
                   "raises ValueError if the (current state, event) pair is NOT in the table below. "
                   "VALID TRANSITIONS (state, event -> new state), exactly: "
                   "(CLOSED, OPEN)->LISTEN; (CLOSED, SYN)->SYN_SENT; (LISTEN, SYN)->SYN_RCVD; "
                   "(LISTEN, RESET)->LISTEN; (SYN_SENT, SYN_ACK)->ESTABLISHED; (SYN_SENT, SYN)->SYN_RCVD; "
                   "(SYN_SENT, RESET)->CLOSED; (SYN_RCVD, ACK)->ESTABLISHED; (SYN_RCVD, CLOSE)->FIN_WAIT_1; "
                   "(ESTABLISHED, FIN)->CLOSE_WAIT; (ESTABLISHED, CLOSE)->FIN_WAIT_1; "
                   "(ESTABLISHED, RESET)->CLOSED; (FIN_WAIT_1, ACK)->FIN_WAIT_2; (FIN_WAIT_1, FIN)->CLOSING; "
                   "(FIN_WAIT_1, FIN_ACK)->TIME_WAIT; (FIN_WAIT_2, FIN)->TIME_WAIT; (CLOSING, ACK)->TIME_WAIT; "
                   "(CLOSE_WAIT, CLOSE)->LAST_ACK; (LAST_ACK, ACK)->CLOSED; (TIME_WAIT, TIMEOUT)->CLOSED; "
                   "(TIME_WAIT, RESET)->CLOSED. Any other (state, event) pair raises ValueError and "
                   "leaves the state unchanged. The machine exposes a public attribute 'state'."),
        "func_sig": "class TCPStateMachine:\n    def __init__(self): ...\n    def handle(self, event: str) -> str: ...",
        "tests": [
            "def _raises(fn):\n    try:\n        fn()\n        return False\n    except ValueError:\n        return True",
            "m = TCPStateMachine(); assert m.state == 'CLOSED'",
            "m = TCPStateMachine(); assert m.handle('SYN') == 'SYN_SENT'",
            "m = TCPStateMachine(); assert m.handle('OPEN') == 'LISTEN'",
            "m = TCPStateMachine(); m.handle('OPEN'); assert m.handle('SYN') == 'SYN_RCVD'",
            "m = TCPStateMachine(); m.handle('OPEN'); m.handle('SYN'); assert m.handle('ACK') == 'ESTABLISHED'",
            "m = TCPStateMachine(); m.handle('SYN'); m.handle('SYN_ACK'); assert m.state == 'ESTABLISHED'",
            "m = TCPStateMachine(); m.handle('OPEN'); m.handle('SYN'); m.handle('ACK'); assert m.handle('FIN') == 'CLOSE_WAIT'",
            "m = TCPStateMachine(); m.handle('OPEN'); m.handle('SYN'); m.handle('ACK'); m.handle('FIN'); assert m.handle('CLOSE') == 'LAST_ACK'",
            "m = TCPStateMachine(); m.handle('OPEN'); m.handle('SYN'); m.handle('ACK'); m.handle('FIN'); m.handle('CLOSE'); assert m.handle('ACK') == 'CLOSED'",
            "m = TCPStateMachine(); m.handle('SYN'); m.handle('SYN_ACK'); m.handle('CLOSE'); assert m.state == 'FIN_WAIT_1'",
            "m = TCPStateMachine(); m.handle('SYN'); m.handle('SYN_ACK'); m.handle('CLOSE'); m.handle('ACK'); assert m.handle('FIN') == 'TIME_WAIT'",
            "m = TCPStateMachine(); m.handle('SYN'); m.handle('SYN_ACK'); m.handle('CLOSE'); m.handle('ACK'); m.handle('FIN'); assert m.handle('TIMEOUT') == 'CLOSED'",
            "m = TCPStateMachine(); m.handle('SYN'); m.handle('SYN_ACK'); m.handle('CLOSE'); assert m.handle('FIN') == 'CLOSING'",
            "m = TCPStateMachine(); m.handle('SYN'); m.handle('SYN_ACK'); m.handle('CLOSE'); m.handle('FIN'); assert m.handle('ACK') == 'TIME_WAIT'",
            "m = TCPStateMachine(); m.handle('SYN'); m.handle('SYN_ACK'); m.handle('CLOSE'); m.handle('FIN_ACK'); assert m.state == 'TIME_WAIT'",
            "m = TCPStateMachine(); m.handle('SYN'); m.handle('SYN_ACK'); m.handle('CLOSE'); m.handle('FIN'); m.handle('ACK'); m.handle('TIMEOUT'); assert m.state == 'CLOSED'",
            "m = TCPStateMachine(); m.handle('OPEN'); m.handle('SYN'); m.handle('ACK'); assert _raises(lambda: m.handle('SYN'))",
            "m = TCPStateMachine(); m.handle('SYN'); assert _raises(lambda: m.handle('ACK'))",
            "m = TCPStateMachine(); assert _raises(lambda: m.handle('FIN'))",
            "m = TCPStateMachine(); m.handle('OPEN'); m.handle('SYN'); m.handle('ACK'); m.handle('FIN'); assert _raises(lambda: m.handle('ACK'))",
        ],
    },
    {
        "name": "concurrent_bank",
        "prompt": ("Implement a thread-safe bank ledger. Bank() manages float balances keyed by string "
                   "account ids. Methods: create_account(acc_id) — ValueError if the account already "
                   "exists; deposit(acc_id, amount) — ValueError if amount <= 0 or account missing; "
                   "withdraw(acc_id, amount) — ValueError if amount <= 0, account missing, or the "
                   "balance is less than amount (no negative balances ever); transfer(from_id, to_id, "
                   "amount) — atomically moves amount from one account to the other; ValueError if "
                   "amount <= 0, either account missing, or insufficient funds (in which case NOTHING "
                   "changes); balance(acc_id) -> float — ValueError if account missing. All operations "
                   "must be atomic and thread-safe: concurrent transfers between the same accounts must "
                   "never lose money, double-spend, or produce negative balances. The total sum of all "
                   "balances must be conserved under any interleaving. Use locks (a single lock is "
                   "acceptable)."),
        "func_sig": "class Bank:\n    def __init__(self): ...\n    def create_account(self, acc_id: str) -> None: ...\n    def deposit(self, acc_id: str, amount: float) -> None: ...\n    def withdraw(self, acc_id: str, amount: float) -> None: ...\n    def transfer(self, from_id: str, to_id: str, amount: float) -> None: ...\n    def balance(self, acc_id: str) -> float: ...",
        "tests": [
            "def _raises(fn):\n    try:\n        fn()\n        return False\n    except ValueError:\n        return True",
            "b = Bank(); b.create_account('a'); b.create_account('b'); b.deposit('a', 100.0); b.deposit('b', 50.0); assert b.balance('a') == 100.0 and b.balance('b') == 50.0",
            "b = Bank(); b.create_account('a'); b.create_account('b'); b.deposit('a', 100.0); b.transfer('a', 'b', 30.0); assert b.balance('a') == 70.0 and b.balance('b') == 30.0",
            "b = Bank(); b.create_account('a'); b.deposit('a', 10.0); assert _raises(lambda: b.withdraw('a', 20.0)); assert b.balance('a') == 10.0",
            "b = Bank(); b.create_account('a'); assert _raises(lambda: b.deposit('a', 0.0))",
            "b = Bank(); b.create_account('a'); assert _raises(lambda: b.deposit('a', -5.0))",
            "b = Bank(); assert _raises(lambda: b.deposit('nope', 5.0))",
            "b = Bank(); assert _raises(lambda: b.balance('nope'))",
            "b = Bank(); b.create_account('a'); assert _raises(lambda: b.create_account('a'))",
            "b = Bank(); b.create_account('a'); b.create_account('b'); b.deposit('a', 10.0); assert _raises(lambda: b.transfer('a', 'b', 11.0)); assert b.balance('a') == 10.0 and b.balance('b') == 0.0",
            "b = Bank(); b.create_account('a'); b.create_account('b'); b.deposit('a', 10.0); assert _raises(lambda: b.transfer('a', 'zz', 1.0))",
            "import threading",
            "import sys; sys.setswitchinterval(1e-7)",
            "b = Bank()\nb.create_account('a0'); b.deposit('a0', 100000.0)\nb.create_account('a1'); b.deposit('a1', 100000.0)\nstart = threading.Barrier(16)\nerrors = []\ndef worker(i):\n    try:\n        start.wait()\n        f, t = ('a0', 'a1') if i % 2 == 0 else ('a1', 'a0')\n        for _ in range(3000):\n            b.transfer(f, t, 1.0)\n    except Exception as e:\n        errors.append(e)\nthreads = [threading.Thread(target=worker, args=(i,)) for i in range(16)]\nfor t in threads: t.start()\nfor t in threads: t.join()\nassert not errors\nassert b.balance('a0') == 100000.0 and b.balance('a1') == 100000.0\nassert b.balance('a0') >= 0.0 and b.balance('a1') >= 0.0",
        ],
    },
    {
        "name": "bencode_codec",
        "prompt": ("Implement bencode (BitTorrent) encoding and decoding. bencode(obj) -> bytes, "
                   "bdecode(data: bytes) -> object. ENCODE: int -> 'i<decimal>e' (e.g. i42e, i-7e, i0e); "
                   "bytes -> '<decimal length>:<bytes>'; str -> encoded as UTF-8 bytes with the same "
                   "length-prefix rule; list -> 'l' + concat(encoded items) + 'e'; dict -> 'd' + "
                   "key-value pairs + 'e', with keys REQUIRED to be str (converted to UTF-8 bytes), "
                   "sorted lexicographically by their raw encoded bytes (standard bencode key order). "
                   "Reject any other type (float, bool, None, tuple) with ValueError. DECODE: parse the "
                   "full byte string; return int / bytes / list / dict (dict keys are bytes, as in "
                   "bencode). MUST REJECT with ValueError: empty input; any trailing data after the "
                   "value; unterminated int/list/dict/string; integer with leading zeros (i01e) or "
                   "'-0' (i-0e) or bare '-'; length prefixes with leading zeros ('03:abc') or no ':' ; "
                   "a length prefix longer than the remaining data; non-bytes dict keys (e.g. "
                   "d1:ai1e is fine but di1e1:e is not); unexpected bytes (e.g. 'x', 'i1ei2e' as "
                   "trailing). Round-trip must hold: bdecode(bencode(x)) == x for int/bytes/str/list/"
                   "dict inputs."),
        "func_sig": "def bencode(obj: object) -> bytes:\ndef bdecode(data: bytes) -> object:",
        "tests": [
            "def _raises(fn):\n    try:\n        fn()\n        return False\n    except ValueError:\n        return True",
            "assert bencode(42) == b'i42e'",
            "assert bencode(-7) == b'i-7e'",
            "assert bencode(0) == b'i0e'",
            "assert bencode(b'') == b'0:'",
            "assert bencode(b'spam') == b'4:spam'",
            "assert bencode('hello') == b'5:hello'",
            "assert bencode([1, 2]) == b'li1ei2ee'",
            "assert bencode([]) == b'le'",
            "assert bencode({}) == b'de'",
            "assert bencode({'b': 2, 'a': 1}) == b'd1:ai1e1:bi2ee'",
            "assert bencode([1, b'a', [b'x']]) == b'li1e1:al1:xee'",
            "assert bdecode(b'i42e') == 42",
            "assert bdecode(b'i-7e') == -7",
            "assert bdecode(b'4:spam') == b'spam'",
            "assert bdecode(b'0:') == b''",
            "assert bdecode(b'le') == []",
            "assert bdecode(b'd1:ai1e1:bi2ee') == {b'a': 1, b'b': 2}",
            "assert bdecode(bencode([1, 3, b'x', {'k': 'v'}])) == [1, 3, b'x', {b'k': b'v'}]",
            "assert bdecode(bencode({'x': [1, b'y', {'z': 3}]})) == {b'x': [1, b'y', {b'z': 3}]}",
            "assert bdecode(bencode('héllo wörld')) == b'h\\xc3\\xa9llo w\\xc3\\xb6rld'",
            "assert bdecode(bencode(42)) == 42 and bdecode(bencode(b'bytes')) == b'bytes'",
            "assert _raises(lambda: bdecode(b''))",
            "assert _raises(lambda: bdecode(b'i1'))",
            "assert _raises(lambda: bdecode(b'i01e'))",
            "assert _raises(lambda: bdecode(b'i-0e'))",
            "assert _raises(lambda: bdecode(b'i-'))",
            "assert _raises(lambda: bdecode(b'3:ab'))",
            "assert _raises(lambda: bdecode(b'03:abc'))",
            "assert _raises(lambda: bdecode(b'4:ab'))",
            "assert _raises(lambda: bdecode(b'l1:ai1e'))",
            "assert _raises(lambda: bdecode(b'd1:a'))",
            "assert _raises(lambda: bdecode(b'di1e1:e'))",
            "assert _raises(lambda: bdecode(b'x'))",
            "assert _raises(lambda: bdecode(b'i1ei2e'))",
            "assert _raises(lambda: bencode(1.5))",
            "assert _raises(lambda: bencode(True))",
            "assert _raises(lambda: bencode(None))",
            "assert _raises(lambda: bencode({1: 'x'}))",
        ],
    },
    {
        "name": "rpn_assembler",
        "prompt": ("Implement an assembler + simulator for a tiny stack-machine language. run_asm(src) "
                   "assembles the program, executes it, and returns the concatenation of all PRINTED "
                   "values, each followed by a newline (empty output for programs that print nothing). "
                   "SOURCE: one instruction per line (leading/trailing whitespace allowed, blank lines "
                   "skipped, '#' starts a comment to end of line). A line ending with ':' defines a "
                   "label (name = alphanumeric + underscore; must be unique). INSTRUCTIONS: 'PUSH <int>' "
                   "push an integer; 'POP' discard top; 'DUP' duplicate top; 'SWAP' exchange top two; "
                   "'ADD'/'SUB'/'MUL'/'DIV' pop two operands and push the result (SUB pushes (second "
                   "pop) - (first pop); DIV pushes (second pop) // (first pop), integer division; DIV "
                   "by zero raises ValueError); 'NEG' negate top; 'PRINT' pop and append str(value) + "
                   "'\\n' to the output; 'HALT' stop execution immediately (later instructions ignored); "
                   "'JMP <label>' unconditional jump; 'JZ <label>' pops the top and jumps iff it equals "
                   "0; 'JNZ <label>' pops the top and jumps iff it differs from 0. ASSEMBLY ERRORS "
                   "(ValueError): unknown mnemonic; wrong operand count; non-integer PUSH; undefined "
                   "label; duplicate label. RUNTIME ERRORS (ValueError): stack underflow (any "
                   "operation with too few values); division by zero. Execution starts at the first "
                   "instruction and proceeds in order unless a jump redirects it; jumping to the end of "
                   "the program halts it."),
        "func_sig": "def run_asm(src: str) -> str:",
        "tests": [
            "def _raises(fn):\n    try:\n        fn()\n        return False\n    except ValueError:\n        return True",
            "assert run_asm('PUSH 5\\nPRINT') == '5\\n'",
            "assert run_asm('PUSH 3\\nPUSH 4\\nADD\\nPRINT') == '7\\n'",
            "assert run_asm('PUSH 10\\nPUSH 3\\nSUB\\nPRINT') == '7\\n'",
            "assert run_asm('PUSH 6\\nPUSH 7\\nMUL\\nPRINT') == '42\\n'",
            "assert run_asm('PUSH 20\\nPUSH 4\\nDIV\\nPRINT') == '5\\n'",
            "assert run_asm('PUSH 2\\nNEG\\nPRINT') == '-2\\n'",
            "assert run_asm('PUSH 1\\nPUSH 2\\nSWAP\\nPRINT\\nPRINT') == '1\\n2\\n'",
            "assert run_asm('PUSH 3\\nloop:\\nDUP\\nDUP\\nJZ done\\nPRINT\\nPUSH 1\\nSUB\\nJMP loop\\ndone:\\nPRINT\\nHALT') == '3\\n2\\n1\\n0\\n'",
            "assert run_asm('PUSH 0\\nPUSH 3\\nloop:\\nDUP\\nJZ done\\nSWAP\\nPUSH 1\\nADD\\nSWAP\\nPUSH 1\\nSUB\\nJMP loop\\ndone:\\nPOP\\nPRINT') == '3\\n'",
            "assert run_asm('# comment\\nPUSH 9\\nPRINT') == '9\\n'",
            "assert run_asm('PUSH 1\\nHALT\\nPUSH 2\\nPRINT') == ''",
            "assert run_asm('PUSH 2\\nPUSH 3\\nJMP skip\\nADD\\nPRINT\\nskip:\\nMUL\\nPRINT') == '6\\n'",
            "assert _raises(lambda: run_asm('PUSH 1\\nADD'))",
            "assert _raises(lambda: run_asm('PUSH 1\\nPUSH 0\\nDIV'))",
            "assert _raises(lambda: run_asm('JMP nowhere'))",
            "assert _raises(lambda: run_asm('FOO'))",
            "assert _raises(lambda: run_asm('loop:\\nloop:'))",
            "assert _raises(lambda: run_asm('PUSH'))",
            "assert _raises(lambda: run_asm('PUSH x'))",
            "assert _raises(lambda: run_asm('PUSH 1\\nPOP\\nPOP'))",
            "assert _raises(lambda: run_asm('PRINT'))",
            "assert _raises(lambda: run_asm('DUP'))",
        ],
    },
    {
        "name": "markdown_table",
        "prompt": ("Parse a GitHub-flavored markdown table and render it as strict HTML. "
                   "md_table_to_html(text) returns a string of the form: '<table>\\n<thead><tr>...rows..."
                   "</tr></thead>\\n<tbody>...rows...</tbody>\\n</table>'. PARSE: split the text into "
                   "lines, ignoring blank lines. The FIRST non-blank line is the header row; the SECOND "
                   "is the separator row; all remaining lines are body rows. A row may have an optional "
                   "leading '|' and optional trailing '|' (trailing pipe removed unless it is escaped). "
                   "Cells are separated by unescaped '|' characters; '\\|' inside a cell is a literal "
                   "pipe. Cell text is stripped of surrounding whitespace. SEPARATOR: each cell must "
                   "match ':?-{3,}:?' (three or more dashes, optional leading colon = left-align, "
                   "optional trailing colon = right-align, both = center, neither = default). The "
                   "separator must have the same number of cells as the header, and every body row must "
                   "match the header's cell count. ERRORS (ValueError): fewer than two non-blank lines; "
                   "a separator cell that does not match the pattern; a column-count mismatch in the "
                   "separator or any body row. HTML: header cells become '<th>' and body cells '<td>'; "
                   "when the separator declares alignment, add ' align=\"left|right|center\"' to the tag "
                   "(no align attribute for default). Escaping: in every cell, replace '&' with '&amp;', "
                   "'<' with '&lt;', '>' with '&gt;'. Rows are '<tr>' + cells + '</tr>' with no "
                   "whitespace between cells."),
        "func_sig": "def md_table_to_html(text: str) -> str:",
        "tests": [
            "def _raises(fn):\n    try:\n        fn()\n        return False\n    except ValueError:\n        return True",
            "assert md_table_to_html('| name | age |\\n| :--- | ---: |\\n| alice | 30 |') == '<table>\\n<thead><tr><th align=\"left\">name</th><th align=\"right\">age</th></tr></thead>\\n<tbody><tr><td align=\"left\">alice</td><td align=\"right\">30</td></tr></tbody>\\n</table>'",
            "assert md_table_to_html('| a | b |\\n| :---: | --- |\\n| x | y |') == '<table>\\n<thead><tr><th align=\"center\">a</th><th>b</th></tr></thead>\\n<tbody><tr><td align=\"center\">x</td><td>y</td></tr></tbody>\\n</table>'",
            "assert md_table_to_html('a | b\\n--- | ---\\nx | y') == '<table>\\n<thead><tr><th>a</th><th>b</th></tr></thead>\\n<tbody><tr><td>x</td><td>y</td></tr></tbody>\\n</table>'",
            "assert md_table_to_html('| a\\\\|b | c |\\n| --- | --- |\\n| 1 | 2 |') == '<table>\\n<thead><tr><th>a|b</th><th>c</th></tr></thead>\\n<tbody><tr><td>1</td><td>2</td></tr></tbody>\\n</table>'",
            "assert md_table_to_html('| <b> & x |\\n| --- |\\n| 1 |') == '<table>\\n<thead><tr><th>&lt;b&gt; &amp; x</th></tr></thead>\\n<tbody><tr><td>1</td></tr></tbody>\\n</table>'",
            "assert md_table_to_html('\\n\\n| a |\\n| --- |\\n| x |\\n\\n') == '<table>\\n<thead><tr><th>a</th></tr></thead>\\n<tbody><tr><td>x</td></tr></tbody>\\n</table>'",
            "assert md_table_to_html('| a | b |\\n| --- | --- |\\n| x | y |\\n| z | w |') == '<table>\\n<thead><tr><th>a</th><th>b</th></tr></thead>\\n<tbody><tr><td>x</td><td>y</td></tr><tr><td>z</td><td>w</td></tr></tbody>\\n</table>'",
            "assert md_table_to_html('| a |\\n| --- |\\n| |') == '<table>\\n<thead><tr><th>a</th></tr></thead>\\n<tbody><tr><td></td></tr></tbody>\\n</table>'",
            "assert _raises(lambda: md_table_to_html('| a |'))",
            "assert _raises(lambda: md_table_to_html('| a |\\n| -- |\\n| x |'))",
            "assert _raises(lambda: md_table_to_html('| a | b |\\n| --- |\\n| x | y |'))",
            "assert _raises(lambda: md_table_to_html('| a | b |\\n| --- | --- |\\n| x |'))",
            "assert _raises(lambda: md_table_to_html(''))",
        ],
    },
    {
        "name": "csv_pipeline",
        "prompt": ("Implement a strict CSV parse-transform-format pipeline. process_csv(text) parses "
                   "RFC-4180-style CSV, applies a fixed transform, and returns the re-serialized CSV "
                   "with a trailing newline. PARSE: the first row is the header; fields are separated by "
                   "commas; a field may be double-quoted (required when it contains a comma, quote, or "
                   "newline); inside quotes, '\"\"' is an escaped quote; fields may span newlines. "
                   "Raise ValueError on: an unterminated quoted field; empty input; a row whose column "
                   "count differs from the header. TRANSFORM: (1) drop every data row whose value in "
                   "the column named 'status' equals 'skip' exactly (if there is no 'status' column, "
                   "nothing is dropped); (2) if there is a column named 'sort', sort the remaining rows "
                   "STABLY by that column: rows whose value parses as a float sort numerically (ascending) "
                   "before rows whose value does not; within each group ascending (numeric, then "
                   "lexicographic). FORMAT: re-serialize as CSV with the same quoting rules (quote only "
                   "fields that need it, escape quotes by doubling), one row per line, and a trailing "
                   "newline at the very end. A header with no data rows is valid and returns the header "
                   "row plus newline."),
        "func_sig": "def process_csv(text: str) -> str:",
        "tests": [
            "def _raises(fn):\n    try:\n        fn()\n        return False\n    except ValueError:\n        return True",
            "assert process_csv('a,b\\n1,2\\n3,4') == 'a,b\\n1,2\\n3,4\\n'",
            "assert process_csv('a,b\\n\"x,y\",2') == 'a,b\\n\"x,y\",2\\n'",
            "assert process_csv('a\\n\"say \"\"hi\"\"\"') == 'a\\n\"say \"\"hi\"\"\"\\n'",
            "assert process_csv('a\\n\"line1\\nline2\"') == 'a\\n\"line1\\nline2\"\\n'",
            "assert process_csv('name,status\\nx,skip\\ny,ok\\nz,skip') == 'name,status\\ny,ok\\n'",
            "assert process_csv('id,sort\\n1,10\\n2,2\\n3,5') == 'id,sort\\n2,2\\n3,5\\n1,10\\n'",
            "assert process_csv('id,sort\\na,z\\nb,x\\nc,y') == 'id,sort\\nb,x\\nc,y\\na,z\\n'",
            "assert process_csv('id,sort\\n1,10\\n2,b\\n3,5') == 'id,sort\\n3,5\\n1,10\\n2,b\\n'",
            "assert process_csv('id,sort\\n1,10\\n2,2\\n3,5\\n4,skip2') == 'id,sort\\n2,2\\n3,5\\n1,10\\n4,skip2\\n'",
            "assert process_csv('a,b\\n1,2\\n3,4\\n5,skip') == 'a,b\\n1,2\\n3,4\\n5,skip\\n'",
            "assert process_csv('a,b') == 'a,b\\n'",
            "assert process_csv('a\\n1\\n2') == 'a\\n1\\n2\\n'",
            "assert _raises(lambda: process_csv(''))",
            "assert _raises(lambda: process_csv('a\\n\"x'))",
            "assert _raises(lambda: process_csv('a,b\\n1'))",
            "assert _raises(lambda: process_csv('a,b\\n1,2,3'))",
        ],
    },
]

CALIB3_TASKS = [t for t in CALIB2_TASKS if t["name"] in SURVIVORS] + _NEW_TASKS

if __name__ == "__main__":
    names = [t["name"] for t in CALIB3_TASKS]
    assert len(names) == len(set(names)), "duplicate task names"
    print(f"{len(CALIB3_TASKS)} tasks: {', '.join(names)}")
