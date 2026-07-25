import os
import time
import pandas as pd
from dotenv import load_dotenv
import comtradeapicall

# ==========================
# CONFIG
# ==========================

load_dotenv()

API_KEY = os.getenv("UN_API_KEY")

OUTPUT_DIR = r"C:\Users\HP\Desktop\projet2\data\raw"

os.makedirs(OUTPUT_DIR, exist_ok=True)

YEARS = range(2016, 2027)

FLOWS = {
    "M": "import",
    "X": "export"
}

# ==========================
# DOWNLOAD
# ==========================

for flow_code, flow_name in FLOWS.items():

    all_data = []

    print(f"\n========== {flow_name.upper()} ==========")

    for year in YEARS:

        for month in range(1, 13):

            period = f"{year}{month:02d}"

            print(f"Downloading {period}")

            try:

                df = comtradeapicall.getFinalData(

                    subscription_key=API_KEY,

                    typeCode="C",
                    freqCode="M",
                    clCode="HS",

                    period=period,

                    reporterCode=None,
                    partnerCode=None,

                    cmdCode="2510",

                    flowCode=flow_code,

                    partner2Code=None,
                    customsCode=None,
                    motCode=None,

                    maxRecords=250000,

                    format_output="JSON",

                    aggregateBy=None,
                    breakdownMode="classic",

                    countOnly=False,
                    includeDesc=True

                )

                if df is not None and len(df):

                    all_data.append(df)

                    print(f"Rows : {len(df)}")

                else:

                    print("No Data")

            except Exception as e:

                print(e)

            time.sleep(1)

    if len(all_data):

        final = pd.concat(all_data, ignore_index=True)

        output = os.path.join(
            OUTPUT_DIR,
            f"{flow_name}_2016_2026.csv"
        )

        final.to_csv(

            output,

            index=False,

            encoding="utf-8-sig"

        )

        print(f"\nSaved : {output}")
        print(final.shape)

    else:

        print("Nothing downloaded.")