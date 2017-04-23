import sheets


class Example(sheets.Row):
    title = sheets.Column()
    description = sheets.Column()


def main():
    print(Example._dialect)
    print(Example.title)


if __name__ == '__main__':
    main()
