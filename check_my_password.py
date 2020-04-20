import requests
import hashlib
import sys

def req_api_response(hashed_query):
    url = 'https://api.pwnedpasswords.com/range/'+'CBFDA'
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f'Error occurred while invoking the API. Returned with a status code {response.status_code}')
    return response

def get_hacked_password_count(response,tail):
    list_of_hash_with_count = (line.split(':') for line in response.text.splitlines())
    for hash_password,count in list_of_hash_with_count:
        if tail == hash_password:
            return int(count)
    return 0

def pwned_api_check(password):
    hashed_password = hashlib.sha1(password.encode('UTF-8')).hexdigest().upper()
    first_5_hashed_chars, tail = hashed_password[:5],hashed_password[5:]
    response = req_api_response(first_5_hashed_chars)
    return(get_hacked_password_count(response,tail))

def main(passwords):
    for password in passwords:
        hack_count = pwned_api_check(password)
        if hack_count > 0:
            print(f'Password {password} was hacked {hack_count} times!')
        else:
            print(f'Password {password} is safe!')

if __name__ == '__main__':
    passwords = sys.argv[1:]
    sys.exit(main(passwords))