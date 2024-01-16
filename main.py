from crawl import WebCrawler
from application import crawl
from excel import read_excel


def main():
    crawler = WebCrawler()
    crawl(crawler)
    crawler.close()


if __name__ == "__main__":
    main()
