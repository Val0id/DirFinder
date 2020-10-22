#/usr/bin/env python3

import click
import requests
import concurrent.futures

@click.command()
@click.argument('url')
@click.option('-w', '--wordlist', help='Directory Wordlist', default='common.txt')
@click.option('-t', '--threads', help='Threads', default=5)

def main(url, wordlist, threads):
    if not url.startswith('http'):
        url = 'http://%s' % url
    if url[-1] != '/':
        url = '%s/' % url

    try:
        requests.get(url)
    except:
        print("%s ^Error^ No Response [!]" % url)
        exit(0)

    try:
        wordl = open(wordlist, 'r')
    except:
        print("No Such File or Directory : %s" % wordlist)
        exit(0)

    tr = int(threads)
    
    def load_url(wl):
        wl = wl.strip()
        r = requests.get(url+wl)
        
        return r.status_code

    with concurrent.futures.ThreadPoolExecutor(max_workers=tr) as e:
        futures = {e.submit(load_url, wl): wl.strip() for wl in wordl}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            wlist = futures[future]

            print(wlist, result)

if __name__ == '__main__':
    main()
