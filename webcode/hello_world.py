import re

pattern = re.compile('hello.+')
s = 'hello world'
print pattern.search(s).group(0)
