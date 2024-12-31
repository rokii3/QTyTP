import pandas as pd
import random

def filter_and_dedupe_annotations(input_file, output_file, target_fraction=0.5):
    """
    Filters a CSV file of question pairs, removing rows with partial or empty annotations,
    duplicate questions, and reduces Indonesian examples to a target fraction.

    Args:
        input_file: Path to the input CSV file
        output_file: Path to the output CSV file
        target_fraction: Target fraction of Indonesian examples to keep (default: 0.5)
    """
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return
    except pd.errors.EmptyDataError:
        print("Error: Input CSV file is empty.")
        return
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return

    # Convert string representations of lists to actual lists
    df['feature1'] = df['feature1'].astype(str).apply(lambda x: eval(x) if x != 'nan' and x != '[]' else [])
    df['feature2'] = df['feature2'].astype(str).apply(lambda x: eval(x) if x != 'nan' and x != '[]' else [])

    # Filter for rows with non-empty annotations and question marks
    df_filtered = df[
        (df['feature1'].apply(len) > 0) & 
        (df['feature2'].apply(len) > 0) & 
        (df['source'].str.contains('[?؟]', regex=True, na=False)) & 
        (df['target'].str.contains('[?؟]', regex=True, na=False))
    ].copy()

    # Create a combined question column
    df_filtered['combined_question'] = df_filtered['source'] + df_filtered['target']

    # Handle Indonesian sampling
    if 'language' not in df_filtered.columns:
        print("Error: Language column not found in the input file.")
        return

    # Split the dataframe into Indonesian and non-Indonesian examples
    indonesian_df = df_filtered[df_filtered['language'] == 'id'].copy()
    non_indonesian_df = df_filtered[df_filtered['language'] != 'id'].copy()

    # Calculate how many Indonesian examples to keep
    num_indonesian_to_keep = int(len(indonesian_df) * target_fraction)
    
    if num_indonesian_to_keep > 0:
        # Randomly sample Indonesian examples
        sampled_indonesian = indonesian_df.sample(n=num_indonesian_to_keep, random_state=42)
        
        # Combine sampled Indonesian with non-Indonesian examples
        df_balanced = pd.concat([sampled_indonesian, non_indonesian_df])
    else:
        df_balanced = df_filtered

    # Remove duplicates based on the combined question
    df_deduped = df_balanced.drop_duplicates(subset='combined_question', keep='first')

    # Drop the temporary combined question column
    df_final = df_deduped.drop(columns=['combined_question'])

    # Print statistics about the dataset
    print("\nDataset Statistics:")
    print("Original total examples:", len(df))
    print("After filtering:", len(df_filtered))
    print("Final examples after balancing and deduplication:", len(df_final))
    print("\nLanguage distribution in final dataset:")
    print(df_final['language'].value_counts())

    try:
        df_final.to_csv(output_file, index=False)
        print(f"\nFiltered and balanced data saved to {output_file}")
    except Exception as e:
        print(f"Error writing to output file: {e}")

# Example usage:
if __name__ == "__main__":
    input_csv = 'results/annotated_question_pairs.csv'
    output_csv = 'results/filtered_questions.csv'
    target_fraction = 0.5  # Reduce Indonesian examples to 50%
    filter_and_dedupe_annotations(input_csv, output_csv, target_fraction)