__author__ = 'tahsin'
import os

"""
    This is the application starter. It can be used to run the application instead of running each step manually.
"""

if __name__ == '__main__':

    if (os.path.exists('testdata.json')):
        print('testdata.json removed!')
        os.remove('testdata.json')

    # run the scrapy spider
    # os.system('scrapy crawl katcr -o testdata.json > out.txt')
    os.system('scrapy crawl yobit -o testdata.json > out.txt')
    # print(sys.path)
    # sort data
    # os.system('python main.py')

    # start server
    # os.system('python -m SimpleHTTPServer')

    print("DONE!")


