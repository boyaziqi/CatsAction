from test import add


if __name__ == '__main__':
    print('start task')
    result = add.delay(2, 18)
    print('end task')
    print(result)
