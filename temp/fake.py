from requests import Session, post, put, get

def main():
    s = Session()
    response =s.get('http://localhost:5000/api/orders/test/')
    if (response.status_code == 500):
        pass
if __name__ == '__main__':
    main()
