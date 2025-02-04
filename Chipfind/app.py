from flask import Flask, render_template, request, send_file
import pandas as pd
from fuzzywuzzy import fuzz
from waitress import serve
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle file upload
        file = request.files["file"]
        if file:
            df = pd.read_csv(file)

            # Data Cleaning
            df = clean_data(df)

            # Fuzzy Matching
            df = fuzzy_match(df)

            # Wildcard Matching
            df = wildcard_match(df)

            # Flag Non-Existent MPNs
            df = flag_non_existent_mpns(df)

            # Save cleaned file
            cleaned_file = "cleaned_data.csv"
            df.to_csv(cleaned_file, index=False)

            return render_template("index.html", message="File processed successfully!", download=True)

    return render_template("index.html", message=None, download=False)

@app.route("/download")
def download():
    path = "cleaned_data.csv"
    return send_file(path, as_attachment=True)

def clean_data(df):
    # Example: Remove special characters, standardize formats, etc.
    df = df.applymap(lambda x: str(x).replace("!", "").replace("@", ""))
    return df

def fuzzy_match(df):
    # Example: Implement fuzzy matching logic
    df["similarity_score"] = df["MPN"].apply(lambda x: fuzz.ratio(x, "example_mpn"))
    return df

def wildcard_match(df):
    # Example: Support wildcard searches
    df["wildcard_match"] = df["MPN"].str.contains("ABC*", regex=True)
    return df

def flag_non_existent_mpns(df):
    # Example: Flag non-existent MPNs
    valid_mpns = ["example_mpn1", "example_mpn2"]
    df["exists"] = df["MPN"].isin(valid_mpns)
    return df

if __name__ == "__main__":
    app.run()
    