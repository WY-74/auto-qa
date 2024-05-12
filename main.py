import os
from data_driver.excel_driver import ExcelDriver


if __name__ == "__main__":
    ths = []

    for path, _, files in os.walk("./data"):
        if not path.endswith("/"):
            path = f"{path}/"

        for file in files:
            if file.endswith(".xlsx"):
                ExcelDriver().run(f"{path}{file}")
