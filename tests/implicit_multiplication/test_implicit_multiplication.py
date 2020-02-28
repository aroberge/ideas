from ideas.examples import implicit_multiplication

add_mul = implicit_multiplication.add_multiplication_symbol
transform_source = implicit_multiplication.transform_source


def test_multiply_by_number():
    assert add_mul("2n") == "2 * n", "Multiply name by 2"
    assert add_mul("2 n") == "2 *  n", "Multiply name by 2"
    assert add_mul("2()") == "2 * ()", "Multiply ( by 2"
    assert add_mul("2 ()") == "2 *  ()", "Multiply ( by 2"


if __name__ == '__main__':
    test_multiply_by_number()
    print("Done.")
