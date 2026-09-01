# coding: lambda_encoding

square = λ x: x**2

assert square(3) == 9

print("Using lambda-encoding: λ")  # λ is not converted inside strings
print("The square of 5 is", square(5))
