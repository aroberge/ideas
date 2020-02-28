expected = "..pp.p.p.."
result = []
for i in range(11):
    switch i:
        case in (0, 1, 4, 6, 8, 9):
            result.append(".")
        case in (2, 3, 5, 7):
            result.append("p")

result = "".join(result)
assert expected == result
