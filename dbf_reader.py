__all__ = ['queries']

from dbfread import dbf

table = dbf.DBF("data/Kommun_RT90_region.dbf")


def pull_names(row):
    return f"{row['KnNamn']} kommun"


queries = list(map(pull_names, table))
