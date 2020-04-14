def test():
    i = 12

    def fn():
        print(i + 1)

    return fn


if __name__ == "__main__":
    test()()
