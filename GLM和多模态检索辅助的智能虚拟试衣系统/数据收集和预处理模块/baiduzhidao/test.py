import re

str = "http://img10.360buyimg.com/n7/jfs/t1/162296/15/12596/161359/604cdc00E1dc62402/f9024e185b409632.jpg"
print(re.sub("n7*", "n0", str))
