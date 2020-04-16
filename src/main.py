from validators import url
from scrapper import get_and_write_sellers

if __name__ == '__main__':
    print('Enter product link')
    while True:
        input_url = input()
        is_valid_url = url(input_url)
        if is_valid_url:
            filename = get_and_write_sellers(input_url)
            print(f'Links were written to a file {filename}')
            break
        else:
            print('Invalid url, please enter valid address')

