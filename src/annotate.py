import pandas as pd
import re
import nltk
from nltk.stem import PorterStemmer


def annotate_features(df):
    """Annotates the DataFrame with information type and question type features."""

    # Information Type (feature1)
    def get_information_type(text):
        text = text.lower()  # Lowercase for case-insensitivity
        features = []

        # Modality
        if re.search(r"\b(can|could|should|would|will|may|might|must)\b", text):
            features.append("modality")

        # Quantification
        if re.search(r"\b(how much|how many|some|all|any|few|many|several|most|none)\b", text):
            features.append("quantification")

        # Comparison
        if re.search(r"\b(more|less|better|worse|bigger|smaller|than|as|equal|similar|different)\b", text):
            features.append("comparison")

        # Cleft
       
    # Improved regex for cleft sentences (focused on "that")
        cleft_pattern_that = r"^it(?:\'s|\sis|\swas|\swere)\s(?!not\b)(?:the\s)?(?!.*\bthat\b.*)(?:[a-zA-Z'-]+)(?:\s[a-zA-Z'-]+){0,4}?\sthat\b"
        if re.search(cleft_pattern_that, text, re.IGNORECASE):
            features.append("cleft_that")

    # Original (less accurate) regex for cleft sentences (with wh-words)
        cleft_pattern_wh = r"it'?s?\b.*\b(that|who|which|where|when|why|how)\b"  # Note the '?' after 'it' and 's'
        if re.search(cleft_pattern_wh, text, re.IGNORECASE):
            features.append("cleft_wh")



        # Negation
        if re.search(r"(\bnot|n't|\bno|\bnever|\bnobody|\bnothing|\bnowhere|\bneither|\bnor)\b", text):
            features.append("negation")

        return features

    # Question Type (feature2)
    def get_question_type(text):
        text = text.lower()  # Lowercase
        stemmer = PorterStemmer()
        text_stemmed = " ".join([stemmer.stem(word) for word in text.split()])
        
        if re.search(r"^(?:\bdo|doe|\bdid|\bis|are|wa|do|\bdoes|did|is|\bhas|were|have|ha|had|can|could|should|would|will|mai|might|must)\b", text_stemmed):
            return ["polar"]
        elif re.search(r"(\bwho|who|\bwhat|\bwhich|what|where|when|why|how|which|whose|whom)\b", text):
            return ["wh-question"]
        elif re.search(r"\bor\b", text):
            return ["alternative"]
        elif re.search(r"\bif\b", text):
            return ["conditional"]
        return []

    df['feature1'] = df['target'].apply(get_information_type)
    df['feature2'] = df['target'].apply(get_question_type)

    return df


def main():

    input_csv = "results/question_pairs_metadata.csv"
    output_csv = "results/annotated_question_pairs.csv"

    try:
        df = pd.read_csv(input_csv, converters={'feature1': eval, 'feature2': eval})  # Ensure correct loading from CSV
        df = annotate_features(df)
        print(df.head()) # Print the first few examples to check.
        df.to_csv(output_csv, index=False, encoding='utf-8')
        print(f"Annotated data saved to {output_csv}")

    except FileNotFoundError:
        print(f"Error: {input_csv} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Download required NLTK resources (only needed once)
    try:
        nltk.data.find('tokenizers/punkt') #checks if resource exists, otherwise download it
    except LookupError:
        nltk.download('punkt')

    try:
        nltk.data.find('corpora/stopwords') #checks if resource exists, otherwise download it
    except LookupError:
        nltk.download('stopwords')

    main()