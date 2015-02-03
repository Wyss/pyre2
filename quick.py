import re2
import re
import timeit

def bump_num(matchobj):
    int_value = int(matchobj.group_b(0))
    return str(int_value + 1).encode('utf-8')


print(re2.sub(b'\\d+', bump_num, b'08.2 -2 23x99y'))
print(b'9.3 -3 24x100y')

s = b'\\1\\1'
print(re2.escape(s) == s)
print(re2.sub(b'(.)', re2.escape(s), b'x'))
print(re2.sub(b'(.)', re2.escape(s), b'x') == s)

#begin unicode
def bump_num(matchobj):
    int_value = int(matchobj.group_b(0))
    return str(int_value + 1)

print(re2.sub('\\d+', bump_num, '08.2 -2 23x99y'))
print('9.3 -3 24x100y')

s = '\\1\\1'
print(re2.escape(s) == s)
print(re2.sub('(.)', re2.escape(s), 'x'))
print(re2.sub('(.)', re2.escape(s), 'x') == s)

import os.path as opath
path = opath.dirname(opath.abspath(__file__))
fn = opath.join(path, "tests", "genome.dat")
with open(fn, 'rb') as fd:
    genome = fd.read()


search = b"(?P<cupcake>c[cg]cg[ag]g)"

re2_regex = re2.compile(search)
re_regex = re.compile(search)
def testre2():
    return re2_regex.findall(genome)
def testre():
    return re_regex.findall(genome)

print(re2_regex.search(genome).groupdict())
search = b"c[cg]cg[ag]g"
re2_regex = re2.compile(search)
# print(re2_regex.findall(genome))
print("bytes re2:", timeit.timeit("testre2()", setup="from __main__ import testre2", number=10))
print("bytes re:", timeit.timeit("testre()", setup="from __main__ import testre", number=10))

with open(fn, 'r') as fd:
    genome_u = fd.read()

search = "(?P<cupcake>c[cg]cg[ag]g)"

re2_regex_u = re2.compile(search)
def testre3():
    return re2_regex_u.findall(genome_u)
print("unicode re2:", timeit.timeit("testre3()", setup="from __main__ import testre3", number=10))
# print(testre3()[:10])
print(re2_regex_u.search(genome_u).groupdict())