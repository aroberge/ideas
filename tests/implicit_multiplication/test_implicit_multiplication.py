from ideas.examples import implicit_multiplication

add_mul = implicit_multiplication.add_multiplication_symbol


def test_multiply_by_number():
    assert add_mul("2n") == "2 * n", "Multiply name by 2"
    assert add_mul("3 n") == "3 *  n", "Multiply name by 3"
    assert add_mul("4()") == "4 * ()", "Multiply ( by 4"
    assert add_mul("5 ()") == "5 *  ()", "Multiply ( by 5"
    assert add_mul("6 7") == "6 *  7", "Multiply 6 by 7"


def test_multiply_two_identifiers():
    assert add_mul("m n") == "m * n", "Multiply m by n"


if __name__ == '__main__':
    test_multiply_by_number()
    test_multiply_two_identifiers()
    print("Done.")
