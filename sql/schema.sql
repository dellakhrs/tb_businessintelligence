CREATE TABLE IF NOT EXISTS dim_city (City_Id INT PRIMARY KEY, City VARCHAR(100) NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS dim_category (Category_Id INT PRIMARY KEY, Category VARCHAR(100) NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS dim_destination (
 Place_Id INT PRIMARY KEY, Place_Name VARCHAR(255) NOT NULL, Description TEXT,
 City_Id INT NOT NULL, Category_Id INT NOT NULL, Price INT NOT NULL, Rating DECIMAL(3,2) NOT NULL,
 Time_Minutes DECIMAL(10,2), Coordinate VARCHAR(255), Lat DECIMAL(12,8), `Long` DECIMAL(12,8),
 FOREIGN KEY (City_Id) REFERENCES dim_city(City_Id), FOREIGN KEY (Category_Id) REFERENCES dim_category(Category_Id)
);
CREATE TABLE IF NOT EXISTS dim_user (
 User_Id INT PRIMARY KEY, Location VARCHAR(255) NOT NULL, Age INT NOT NULL, Age_Group VARCHAR(20) NOT NULL
);
CREATE TABLE IF NOT EXISTS fact_rating (
 Rating_Id BIGINT AUTO_INCREMENT PRIMARY KEY, User_Id INT NOT NULL, Place_Id INT NOT NULL,
 Place_Ratings DECIMAL(4,2) NOT NULL, Rating_Observations SMALLINT NOT NULL DEFAULT 1,
 FOREIGN KEY (User_Id) REFERENCES dim_user(User_Id), FOREIGN KEY (Place_Id) REFERENCES dim_destination(Place_Id)
);
ALTER TABLE fact_rating MODIFY COLUMN Place_Ratings DECIMAL(4,2) NOT NULL;
ALTER TABLE fact_rating ADD COLUMN IF NOT EXISTS Rating_Observations SMALLINT NOT NULL DEFAULT 1;
CREATE TABLE IF NOT EXISTS dim_package (
 Package_Id INT PRIMARY KEY, City_Id INT NOT NULL, FOREIGN KEY (City_Id) REFERENCES dim_city(City_Id)
);
CREATE TABLE IF NOT EXISTS bridge_package_destination (
 Package_Id INT NOT NULL, Place_Id INT NOT NULL, Sequence_No TINYINT NOT NULL,
 PRIMARY KEY (Package_Id, Place_Id, Sequence_No),
 FOREIGN KEY (Package_Id) REFERENCES dim_package(Package_Id), FOREIGN KEY (Place_Id) REFERENCES dim_destination(Place_Id)
);
