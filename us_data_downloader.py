import os
import random
import string
from random import randrange
from datetime import datetime, timedelta

import yfinance as yf
from elasticsearch import Elasticsearch
from elasticsearch import helpers

from logger import MyLogger

LOGGER = MyLogger(log_file="", name=__file__)
STOCKS_LIST = str(os.getenv("STOCKS", "AAPL,TSLA,MSFT")).split(",")
INDEX_1_MIN = os.getenv("INDEX_1_MIN", "us_tickers_1m")
INDEX_1_DAY = os.getenv("INDEX_1_DAY", "us_tickers_1d")
ES_HOST = os.getenv("ES_HOST", "localhost")
ES_PORT = os.getenv("ES_PORT", "9200")
ES_USERNAME = os.getenv("ES_USERNAME", "elastic")
ES_PASSWORD = os.getenv("ES_PASSWORD", "SOME_RANDOM_PASS")


def random_id_generator():
    id_size = randrange(5, 10)
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=id_size))


def doc_generator(df, ticker_name, date_time_field, es_index):
    df_iter = df.iterrows()
    for df_idx, document in df_iter:
        doc_dict = document.to_dict()
        doc_dict["ticker"] = ticker_name
        doc_id = str(document[date_time_field].value) + "-" + str(random_id_generator())
        final_doc = {
            "_index": es_index,
            "_type": "_doc",
            "_id": f"{doc_id}",
            "_source": doc_dict,
        }

        yield final_doc


def download_1d_data(ticker, s_date, e_data):
    """
    Download 1 day\'s worth of data from start to end data
    :param ticker: Ticker name , e.g: "AAPL"
    :param s_date: Start date, e.g: "2021-05-07"
    :param e_data: End date, e.g: "2021-05-07"
    :return:
    """
    data_interval = "1d"
    data_1_day = yf.download(
        tickers=ticker, start=s_date, end=e_data, interval=data_interval
    )
    data_1_day.reset_index(level=0, inplace=True)
    return data_1_day


def download_min_data(ticker, s_date, e_date):
    data_interval = "1m"
    LOGGER.info(
        f"Downloading {ticker} from Yahoo finance - s_data={s_date}, e_date={e_date}"
    )
    data_1_min = yf.download(
        tickers=ticker,
        start=s_date,
        end=e_date,
        interval=data_interval,
        auto_adjust=True,
        threads=True
    )
    data_1_min.reset_index(level=0, inplace=True)
    return data_1_min


def get_es_client():
    es_client = Elasticsearch(
        [{"host": ES_HOST, "port": ES_PORT}],
        http_auth=("elastic", "5qq17MySsmBhN4DFvsJW"),
        http_compress=True
    )
    # es_client = Elasticsearch(['localhost'], port=9200, http_compress=True)
    return es_client


def day_downloader_main():
    today_date = datetime.today().strftime("%Y-%m-%d")
    LOGGER.info(f"Downloading day's worth of data for date - [{today_date}]")
    es_client = get_es_client()

    for item in STOCKS_LIST:
        res_data = download_1d_data(item, today_date, today_date)
        helpers.bulk(
            es_client, doc_generator(res_data, item, "Date", INDEX_1_DAY)
        )
    LOGGER.info(f"Done downloading data for - [{today_date}]")


def min_downloader_main():
    start_date = datetime.today().strftime("%Y-%m-%d")
    end_date = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    es_client = get_es_client()

    LOGGER.info(f"Downloading day's worth of data for date - [{start_date}]")
    for item in STOCKS_LIST:
        res_data = download_min_data(item, start_date, end_date)
        LOGGER.info(res_data)
        if res_data.shape[0] > 0:
            helpers.bulk(
                es_client, doc_generator(res_data, item, "Datetime", INDEX_1_MIN)
            )
    LOGGER.info(f"Done downloading data for - [{start_date}]")


if __name__ == "__main__":
    LOGGER.info("Inside main function")
    LOGGER.info(
        f"Global variables are:: {STOCKS_LIST}, {ES_HOST}, {ES_PORT}, {ES_USERNAME}, {ES_PASSWORD}"
    )

    min_downloader_main()
    day_downloader_main()
