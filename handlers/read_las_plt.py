import pandas as pd
from typing import Tuple, List


def sep_and_names(is_spartek: bool) -> Tuple[str, List[str]]:
    # choose the names of the header in case of metrolog or spartek
    if not is_spartek:
        sep = "[,\t]"
        names = ["date", "time", "pressure", "temperature"]
    else:
        sep = r"\s+"
        names = ["date", "time", "AMPM", "elpse", "pressure", "temperature"]
    return sep, names


def drop_and_make_datetime(df: pd.DataFrame, is_spartek: bool) -> pd.DataFrame:
    if is_spartek:
        df["date_time"] = df["date"] + " " + df["time"] + " " + df["AMPM"]
        date_formats = [
            "%d-%b-%y %I:%M:%S %p",
            "%m-%d-%Y %I:%M:%S %p",
            "%m/%d/%Y %I:%M:%S %p",
            "%d/%m/%Y %I:%M:%S %p",
            "%d-%m-%Y %I:%M:%S %p",
            "%d/%b/%y %I:%M:%S %p",
        ]

        for date_format in date_formats:
            try:
                df["date_time_corrected"] = pd.to_datetime(
                    df["date_time"],
                    format=date_format,
                )
                # If parsing succeeds, break out of the loop
                break
            except ValueError:
                # If parsing fails, try the next format
                continue

        df = df.drop(columns=["date", "time", "AMPM", "date_time"])
    else:
        df["date_time"] = df["date"] + " " + df["time"]

        date_formats = [
            "%d-%m-%y %H:%M:%S",
            "%d/%m/%y %H:%M:%S",
            "%m-%d-%y %H:%M:%S",
            "%m/%d/%y %H:%M:%S",
            "%d-%b-%y %H:%M:%S",
            "%b/%d/%y %H:%M:%S",
        ]

        for date_format in date_formats:
            try:
                df["date_time_corrected"] = pd.to_datetime(
                    df["date_time"],
                    format=date_format,
                )
                # If parsing succeeds, break out of the loop
                break
            except ValueError:
                # If parsing fails, try the next format
                continue

        df = df.drop(columns=["date", "time", "date_time"])
    return df


def read_csv_standard(source_file: str, row: int, is_spartek=False) -> pd.DataFrame:
    sep, names = sep_and_names(is_spartek)
    df = pd.read_csv(
        source_file,
        skiprows=row,
        header=None,
        sep=sep,
        names=names,
        engine="python",
    )
    df = drop_and_make_datetime(df, is_spartek)
    return df
