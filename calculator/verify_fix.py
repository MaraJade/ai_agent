from pkg.calculator import Calculator

c = Calculator()
print("3 + 7 * 2 =", c.evaluate("3 + 7 * 2"))
print("3 * 4 + 5 =", c.evaluate("3 * 4 + 5"))
print("2 * 3 - 8 / 2 + 5 =", c.evaluate("2 * 3 - 8 / 2 + 5"))
