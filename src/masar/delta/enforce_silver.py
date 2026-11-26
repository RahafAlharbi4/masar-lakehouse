from masar.spark import get_spark


def add_constraints() -> None:
    spark = get_spark("enforce-silver")
    spark.sql("ALTER TABLE silver.trips ADD CONSTRAINT positive_fare CHECK (fare_sar > 0)")
    spark.sql("ALTER TABLE silver.trips ADD CONSTRAINT valid_duration CHECK (ended_at > started_at)")
    spark.sql("SHOW TBLPROPERTIES silver.trips").show(truncate=False)
    spark.sql(""" ALTER TABLE silver.trips
        ADD CONSTRAINT completed_trips_only
        CHECK (status IS NOT NULL AND status = 'completed')""")
    spark.sql("""ALTER TABLE silver.trips
        ADD CONSTRAINT valid_driver_rating
        CHECK (driver_rating IS NULL OR driver_rating BETWEEN 1 AND 5)""")
    
        
        
    


if __name__ == "__main__":
    add_constraints()

