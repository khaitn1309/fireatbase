
def verify_url(url):
    if url[-1] == "/":
        return url
    else:
        new_url = url + "/"
        return new_url
