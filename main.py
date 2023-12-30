from crawl import WebCrawler
from application import get_access_token
from excel import read_excel


def main():
    crawler = WebCrawler()

    file_path = "../Fitbit_device_외주용.xlsx"
    df = read_excel(file_path)

    try:
        df[["CLIENT_ID", "CLIENT_SECRET", "ACCESS_TOKEN"]] = df.apply(
            lambda row: get_access_token(crawler, row["Google_id"], row["Google_pw"]),
            axis=1,
            result_type="expand",
        )
        df.to_excel(file_path, index=False)
    except Exception as e:
        print(e)

    df.to_excel(file_path, index=False)
    crawler.close()


if __name__ == "__main__":
    main()
