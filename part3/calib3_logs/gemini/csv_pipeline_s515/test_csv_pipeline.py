from csv_pipeline import *


def _raises(fn):
    try:
        fn()
        return False
    except ValueError:
        return True

assert process_csv('a,b\n1,2\n3,4') == 'a,b\n1,2\n3,4\n'

assert process_csv('a,b\n"x,y",2') == 'a,b\n"x,y",2\n'

assert process_csv('a\n"say ""hi"""') == 'a\n"say ""hi"""\n'

assert process_csv('a\n"line1\nline2"') == 'a\n"line1\nline2"\n'

assert process_csv('name,status\nx,skip\ny,ok\nz,skip') == 'name,status\ny,ok\n'

assert process_csv('id,sort\n1,10\n2,2\n3,5') == 'id,sort\n2,2\n3,5\n1,10\n'

assert process_csv('id,sort\na,z\nb,x\nc,y') == 'id,sort\nb,x\nc,y\na,z\n'

assert process_csv('id,sort\n1,10\n2,b\n3,5') == 'id,sort\n3,5\n1,10\n2,b\n'

assert process_csv('id,sort\n1,10\n2,2\n3,5\n4,skip2') == 'id,sort\n2,2\n3,5\n1,10\n4,skip2\n'

assert process_csv('a,b\n1,2\n3,4\n5,skip') == 'a,b\n1,2\n3,4\n5,skip\n'

assert process_csv('a,b') == 'a,b\n'

assert process_csv('a\n1\n2') == 'a\n1\n2\n'

assert _raises(lambda: process_csv(''))

assert _raises(lambda: process_csv('a\n"x'))

assert _raises(lambda: process_csv('a,b\n1'))

assert _raises(lambda: process_csv('a,b\n1,2,3'))