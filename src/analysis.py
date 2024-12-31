import pandas as pd

def analyze_question_pairs(csv_file):
    """
    Analyzes question pairs from a CSV file.

    Args:
        csv_file: Path to the CSV file.

    Returns:
        A dictionary containing the analysis results.  Returns None if there's an error.
    """
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: CSV file is empty.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return None

    # Crucial fix:  Convert to proper lists.  Handles empty lists correctly!
    df['feature1'] = df['feature1'].astype(str).apply(lambda x: eval(x) if x != 'nan' and x !='[]' else [])
    df['feature2'] = df['feature2'].astype(str).apply(lambda x: eval(x) if x != 'nan' and x != '[]' else [])


    results = {}
    languages = df['language'].unique()

    for lang in languages:
        lang_df = df[df['language'] == lang]
        results[lang] = {
            'pairs_count': len(lang_df),
            'fully_annotated': len(lang_df[(lang_df['feature1'].apply(len) > 0) & (lang_df['feature2'].apply(len) > 0)])
        }
        
    overall = {
        'pairs_count': len(df),
        'fully_annotated': len(df[(df['feature1'].apply(len) > 0) & (df['feature2'].apply(len) > 0)])
    }
    
    feature_counts = {}
    for col in ['feature1', 'feature2']:
        for _, row in df.iterrows():
            for feature in row[col]:
                if feature not in feature_counts:
                    feature_counts[feature] = {'total': 0, 'per_language': {}}
                if col == 'feature1':
                    feature_counts[feature]['per_language'][row['language']] = feature_counts[feature].get('per_language', {}).get(row['language'], 0) + 1
                    feature_counts[feature]['total'] += 1
                elif col == 'feature2':
                    feature_counts[feature]['per_language'][row['language']] = feature_counts[feature].get('per_language', {}).get(row['language'], 0) + 1
                    feature_counts[feature]['total'] += 1
    
    results['overall'] = overall
    results['feature_counts'] = feature_counts
    return results




analysis_results = analyze_question_pairs('results/filtered_questions.csv')
if analysis_results:
    print(analysis_results)