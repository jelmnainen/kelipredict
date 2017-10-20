import os
import pandas as pd
from utils import ensure_dir_exists

def main():
    inputDir = './processedData'
    outputDir = './finalData'

    dirs = next(os.walk(inputDir))[1]
    df = pd.DataFrame()
    for dataDir in dirs:
        path, d, files = next(os.walk(inputDir + "/" + dataDir))
        for file in files:
            filepath = inputDir + "/" + dataDir + "/" + file
            df2 = pd.read_csv(filepath)
            df = df.append(df2)

    ensure_dir_exists(outputDir)
    df.to_csv(outputDir + '/data.csv')

main()
