import pandas as pd
import os
from utils import ensure_dir_exists

def main():
    inputDir = './data'
    outputDir = './processedData'
    ensure_dir_exists(outputDir)
    dirs = [x for x in os.walk(inputDir)][1:]
    for path, d, files in dirs:
        outputDirname = outputDir + "/" + path[len(inputDir) + 1:]
        for file in files:
            filepath = path + "/" + file
            print("Reading " + filepath)
            data = read_file(filepath)
            if(isinstance(data, pd.core.frame.DataFrame)):
                save_data(data, outputDirname, file)

def read_file(filename):
    data = pd.read_csv(filename)
    if 'Latitude' and 'Longitude' in data.columns:
        data = clean_data(data)
        dataNearKumpula = is_near_kumpula(data)
        if (dataNearKumpula.shape[0] > 0):
            return dataNearKumpula
    return None

def clean_data(df):
    df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
    df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
    df['Latitude'] = df['Latitude'].fillna(value=2000)
    df['Longitude'] = df['Longitude'].fillna(value=2000)
    return df


def is_near_kumpula(df):
    kumpulaLat = 60.205000
    kumpulaLon = 24.962000
    closeEnough = 0.025000

    return df.loc[
        (abs(df['Latitude'] - kumpulaLat) < closeEnough) &
        (abs(df['Longitude'] - kumpulaLon) < closeEnough)
    ]

def save_data(df, outputDir, outputFile):
    ensure_dir_exists(outputDir)
    filepath = outputDir + "/" + outputFile
    print("Saving data to " + filepath)
    df.to_csv(filepath)

main()
