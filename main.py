import os
import threading
from data_driver.excel_driver import ExcelDriver


if __name__ == "__main__":
    ths = []

    for path, _, files in os.walk("./data"):
        if not path.endswith("/"):
            path = f"{path}/"

        for file in files:
            if file.endswith(".xlsx"):
                thread_id = len(ths)
                ths.append(threading.Thread(target=ExcelDriver().run, args=[f"{path}{file}", thread_id]))

        for th in ths:
            th.start()
