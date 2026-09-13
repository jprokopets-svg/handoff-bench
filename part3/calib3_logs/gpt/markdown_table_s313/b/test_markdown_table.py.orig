from markdown_table import *


def _raises(fn):
    try:
        fn()
        return False
    except ValueError:
        return True

assert md_table_to_html('| name | age |\n| :--- | ---: |\n| alice | 30 |') == '<table>\n<thead><tr><th align="left">name</th><th align="right">age</th></tr></thead>\n<tbody><tr><td align="left">alice</td><td align="right">30</td></tr></tbody>\n</table>'

assert md_table_to_html('| a | b |\n| :---: | --- |\n| x | y |') == '<table>\n<thead><tr><th align="center">a</th><th>b</th></tr></thead>\n<tbody><tr><td align="center">x</td><td>y</td></tr></tbody>\n</table>'

assert md_table_to_html('a | b\n--- | ---\nx | y') == '<table>\n<thead><tr><th>a</th><th>b</th></tr></thead>\n<tbody><tr><td>x</td><td>y</td></tr></tbody>\n</table>'

assert md_table_to_html('| a\\|b | c |\n| --- | --- |\n| 1 | 2 |') == '<table>\n<thead><tr><th>a|b</th><th>c</th></tr></thead>\n<tbody><tr><td>1</td><td>2</td></tr></tbody>\n</table>'

assert md_table_to_html('| <b> & x |\n| --- |\n| 1 |') == '<table>\n<thead><tr><th>&lt;b&gt; &amp; x</th></tr></thead>\n<tbody><tr><td>1</td></tr></tbody>\n</table>'

assert md_table_to_html('\n\n| a |\n| --- |\n| x |\n\n') == '<table>\n<thead><tr><th>a</th></tr></thead>\n<tbody><tr><td>x</td></tr></tbody>\n</table>'

assert md_table_to_html('| a | b |\n| --- | --- |\n| x | y |\n| z | w |') == '<table>\n<thead><tr><th>a</th><th>b</th></tr></thead>\n<tbody><tr><td>x</td><td>y</td></tr><tr><td>z</td><td>w</td></tr></tbody>\n</table>'

assert md_table_to_html('| a |\n| --- |\n| |') == '<table>\n<thead><tr><th>a</th></tr></thead>\n<tbody><tr><td></td></tr></tbody>\n</table>'

assert _raises(lambda: md_table_to_html('| a |'))

assert _raises(lambda: md_table_to_html('| a |\n| -- |\n| x |'))

assert _raises(lambda: md_table_to_html('| a | b |\n| --- |\n| x | y |'))

assert _raises(lambda: md_table_to_html('| a | b |\n| --- | --- |\n| x |'))

assert _raises(lambda: md_table_to_html(''))