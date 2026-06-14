import pandas as pd
from sqlalchemy import inspect

from database.connection import get_engine


def load_dashboard_datasets() -> dict[str, pd.DataFrame]:
    engine = get_engine()
    places = pd.read_sql(
        """SELECT d.Place_Id,d.Place_Name,d.Description,c.Category,k.City,d.Price,d.Rating,
        d.Time_Minutes,d.Coordinate,d.Lat,d.`Long` FROM dim_destination d
        JOIN dim_city k ON d.City_Id=k.City_Id JOIN dim_category c ON d.Category_Id=c.Category_Id
        ORDER BY d.Place_Id""", engine)
    users = pd.read_sql("SELECT User_Id,Location,Age,Age_Group FROM dim_user ORDER BY User_Id", engine)
    fact_columns = {column["name"] for column in inspect(engine).get_columns("fact_rating")}
    observation_select = (
        "f.Rating_Observations"
        if "Rating_Observations" in fact_columns
        else "1 AS Rating_Observations"
    )
    ratings = pd.read_sql(
        f"""SELECT f.User_Id,f.Place_Id,f.Place_Ratings,{observation_select},u.Location,u.Age,u.Age_Group,
        d.Place_Name,k.City,c.Category,d.Price,d.Rating FROM fact_rating f
        JOIN dim_user u ON f.User_Id=u.User_Id JOIN dim_destination d ON f.Place_Id=d.Place_Id
        JOIN dim_city k ON d.City_Id=k.City_Id JOIN dim_category c ON d.Category_Id=c.Category_Id
        ORDER BY f.Rating_Id""", engine)
    long = pd.read_sql(
        """SELECT p.Package_Id Package,k.City,b.Sequence_No,d.Place_Name FROM dim_package p
        JOIN dim_city k ON p.City_Id=k.City_Id JOIN bridge_package_destination b ON p.Package_Id=b.Package_Id
        JOIN dim_destination d ON b.Place_Id=d.Place_Id ORDER BY p.Package_Id,b.Sequence_No""", engine)
    packages = long.pivot(index=["Package", "City"], columns="Sequence_No", values="Place_Name").reset_index()
    packages.columns = [f"Place_Tourism{x}" if isinstance(x, int) else x for x in packages.columns]
    for number in range(1, 6):
        if f"Place_Tourism{number}" not in packages:
            packages[f"Place_Tourism{number}"] = pd.NA
    return {"places": places, "ratings": ratings, "users": users, "packages": packages}
