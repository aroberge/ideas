# flake8: noqa
x = 3
y = 4

x--
assert x == 2
y = x--y  # valid python expression
assert x == 2, y == 4
y = x-- -y  # x-- will be converted here
assert x==1, y ==-3
++x
assert x == 2
--x
assert x == 1
z = (++x, 'y++')  # x converted after assignment
assert z == (2, 'y++')
z = (x++, 'name++')
assert z == (2, 'name++') # x converted before assignment
assert x == 3