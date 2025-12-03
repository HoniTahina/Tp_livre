from db.query import query



def main():
    rows = query("SELECT sysdate FROM dual")
    print(rows)


if __name__ == "__main__":
    main()
