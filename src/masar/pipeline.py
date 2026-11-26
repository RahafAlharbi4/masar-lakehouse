"""Capstone step 6: run the Masar pipeline with make pipeline."""

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BRONZE = ROOT / "lakehouse" / "bronze"


def run(*cmd, cwd=ROOT):
    env = os.environ.copy()
    env["MASAR_HOME"] = str(ROOT)
    env["PYTHONPATH"] = os.pathsep.join(
        part for part in (str(ROOT / "src"), env.get("PYTHONPATH")) if part
    )
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=cwd, env=env, check=True)


def main():
    loaded = [
        (BRONZE / name / "_delta_log").is_dir()
        for name in ("trips", "drivers", "gps_pings")
    ]

    if not any(loaded):
        run(sys.executable, "-m", "masar.ingest.land_bronze")
    elif not all(loaded):
        raise SystemExit("Bronze is partially loaded. Check the three tables.")
    else:
        print("Bronze already loaded", flush=True)

    run(sys.executable, "-m", "masar.register")
    run("dbt", "build", "--select", "+silver_trips", cwd=ROOT / "dbt" / "masar")

    run(sys.executable, "-c", """
from masar.quality.contract import load, validate

silver = load("silver")
results = validate(silver)
for name, result in results.items():
    print(name, result["passed"], "bad_rows:", result["bad_rows"])

failed = [name for name, result in results.items() if not result["passed"]]
if failed:
    raise SystemExit(f"Silver quality failed: {failed}")

spark = silver.sparkSession
properties = {
    row.key for row in spark.sql("SHOW TBLPROPERTIES silver.trips").collect()
}
for name, condition in (
    ("positive_fare", "fare_sar > 0"),
    ("valid_duration", "ended_at > started_at"),
):
    if f"delta.constraints.{name}" not in properties:
        spark.sql(f"ALTER TABLE silver.trips ADD CONSTRAINT {name} CHECK ({condition})")
""")

    run(sys.executable, "-c", """
from masar.transform.build_gold import build_zone_hourly_demand

build_zone_hourly_demand()
""")

    run(sys.executable, "-c", """
from masar.serve.bi_view import build_bi_safe_view

build_bi_safe_view()
""")

    run(sys.executable, "-c", """
from masar.config import GOLD, SILVER
from masar.spark import get_spark

spark = get_spark("capstone-counts")
for path in (
    "lakehouse/bronze/trips",
    "lakehouse/bronze/drivers",
    "lakehouse/bronze/gps_pings",
    str(SILVER),
    f"{GOLD}/zone_hourly_demand",
    f"{GOLD}/bi_trips_safe",
):
    count = spark.read.format("delta").load(path).count()
    print(f"{path}: {count:,}")
""")


if __name__ == "__main__":
    main()