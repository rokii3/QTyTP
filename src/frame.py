import json
import pandas as pd

def create_dataframe_from_json(json_filepaths, languages):
    """
    Creates a Pandas DataFrame from multiple JSON files containing question-translation pairs.
    Adds metadata columns for language, feature1, and feature2 (initialized as empty lists).

    Args:
        json_filepaths: A list of filepaths to the JSON files.
        languages: A list of language codes corresponding to the JSON files.

    Returns:
        A Pandas DataFrame containing the question-translation pairs and metadata.
    """
    data = []
    for filepath, lang in zip(json_filepaths, languages):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                question_pairs = json.load(f)
                for idx, pair in question_pairs.items():
                    data.append({
                        'index': idx,
                        'source': pair.get('source', ''),
                        'target': pair.get('target', ''),
                        'language': lang,
                        'feature1': [],  # Initialize feature1 as an empty list
                        'feature2': []  # Initialize feature2 as an empty list
                    })
        except FileNotFoundError:
            print(f"Error: File not found: {filepath}")
            return None
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in file: {filepath}")
            return None

    df = pd.DataFrame(data)
    return df


def add_features_to_dataframe(df):
    """
    Placeholder function to add features to the DataFrame.
    Modify this function to extract and add the specific features you need.
    """
    # Example (replace with your feature extraction logic)

    # df['feature1'] = df.apply(lambda row: extract_feature1(row), axis=1)

    # df['feature2'] = ...  # Add more features as needed

    return df



def main():

    filepaths = [
        "results/question_pairs_af.json", 
        "results/question_pairs_ar.json",
        "results/question_pairs_id.json",
        "results/question_pairs_mr.json",
    ]
    languages = ['af', 'ar', 'id', 'mr']



    df = create_dataframe_from_json(filepaths, languages)

    if df is not None:

        df = add_features_to_dataframe(df)  # Call the feature extraction function



        print(df.head())  # Print first few rows for inspection

        # Save to CSV
        df.to_csv("results/question_pairs_metadata.csv", index=False, encoding='utf-8')
        print("DataFrame saved to question_pairs_metadata.csv")


if __name__ == "__main__":
    main()