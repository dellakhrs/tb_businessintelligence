from etl.extract import extract
from etl.transform import transform


def test_etl_star_schema_counts() -> None:
    tables = transform(extract())
    assert len(tables["dim_city"]) == 5
    assert len(tables["dim_category"]) == 6
    assert len(tables["dim_destination"]) == 437
    assert len(tables["dim_user"]) == 300
    assert len(tables["fact_rating"]) == 9_597
    assert not tables["fact_rating"].duplicated(["User_Id", "Place_Id"]).any()
    assert tables["fact_rating"]["Rating_Observations"].sum() == 9_921
    assert len(tables["dim_package"]) == 100
    assert len(tables["bridge_package_destination"]) == 405
