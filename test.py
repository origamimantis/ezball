x0 = 0
x1 = 1
a0 = 4
narg = 1


print(f"random number between {(x0:=(0 if nargs<2 else a0))} and {(x1:=(1 if nargs<1 else a0 if nargs<2 else a1))}: {random.randint(x0,x1)}")
print(eval(f"random number between {x0:=(0 if nargs<2 else a0)} and {x1:=(1 if nargs<1 else a0 if nargs<2 else a1)}: {random.randint(x0,x1)}"))
