import json
import re
from typing import Dict, List

class QuestionDetector:
    def __init__(self):
        # English question patterns
        self.en_patterns = [
            r'^(Who|What|Where|When|Why|How|Which|Whose|Whom)\b',  # WH questions
            r'^(Do|Does|Did|Is|Are|Was|Were|Have|Has|Had|Can|Could|Should|Would|Will)\b',  # Yes/No questions
            r'\?$'  # Question mark at end
        ]
        
        # Marathi question patterns
        self.mr_patterns = [
            r'^(कोण|काय|कुठे|केव्हा|का|कसे|कोणता|कोणाचे|कोणाला)\b',  # WH questions
            r'\?$',  # Question mark
            r'(का|काय)$'  # Question particles at end
        ]
        
        # Arabic question patterns
        self.ar_patterns = [
            r'^(من|ما|ماذا|أين|متى|لماذا|كيف|أي|لمن|هل)\b',  # WH questions and هل
            r'\?$',  # Question mark
            r'؟$'    # Arabic question mark
        ]
        
        # Indonesian question patterns
        self.id_patterns = [
            r'^(Siapa|Apa|Dimana|Kapan|Mengapa|Bagaimana|Yang mana|Kepada siapa)\b',  # WH questions
            r'^Apakah\b',  # Yes/No questions
            r'\?$'  # Question mark
        ]
        
        # Afrikaans question patterns
        self.af_patterns = [
            r'^(Wie|Wat|Waar|Wanneer|Hoekom|Hoe|Watter|Aan wie)\b',  # WH questions
            r'^(Is|Het|Sal|Kan|Moet|Wil|Mag)\b',  # Verb-initial questions
            r'\?$'  # Question mark
        ]
        
        # Map language codes to their patterns
        self.lang_patterns = {
            'en': self.en_patterns,
            'mr': self.mr_patterns,
            'ar': self.ar_patterns,
            'id': self.id_patterns,
            'af': self.af_patterns
        }

    def is_question(self, text: str, language: str) -> bool:
        """Check if a text is a question in the specified language."""
        if not text or language not in self.lang_patterns:
            return False
            
        patterns = self.lang_patterns[language]
        
        # Check each pattern for the language
        for pattern in patterns:
            if re.search(pattern, text):
                # Additional validation: must end with question mark for most cases
                if language != 'mr':  # Marathi can have questions without question marks
                    return text.rstrip().endswith('?') or text.rstrip().endswith('؟')
                return True
                
        return False

def extract_question_pairs(source_file: str, target_file: str, language: str, limit: int = 1000) -> Dict:
    """
    Extracts question-translation pairs from source and target language files.

    Args:
        source_file: Path to the source language file.
        target_file: Path to the target language file (English).
        language: The language code of the source file.
        limit: The maximum number of lines to read from each file.

    Returns:
        A dictionary where keys are indices of questions in the source file, 
        and values are dictionaries containing the source question and its English translation.
    """

    detector = QuestionDetector()
    question_pairs = {}

    try:
        with open(source_file, 'r', encoding='utf-8') as sf, open(target_file, 'r', encoding='utf-8') as tf:
            source_lines = [line.strip() for line in sf.readlines()[:limit]]
            target_lines = [line.strip() for line in tf.readlines()[:limit]]  # Read target lines

            for i, source_text in enumerate(source_lines):
                if detector.is_question(source_text, language):
                    question_pairs[i] = {"source": source_text, "target": target_lines[i]} # Add translation

    except FileNotFoundError:
        print(f"Error: {source_file} or {target_file} not found.")
        return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

    return question_pairs



def main():
    """
    Main function to process language files and extract question pairs.
    """
    language_pairs = {
        'af': 'NLLB.af-en',
        'ar': 'NLLB.ar-en',
        'id': 'NLLB.en-id',
        'mr': 'NLLB.en-mr'
    }

    all_question_pairs = {}


    for lang, file_base in language_pairs.items():
        source_file = f"data/{file_base}.{lang}"
        target_file = f"data/{file_base}.en"  # English target
        output_file = f"results/question_pairs_{lang}.json"

        print(f"Processing {lang.upper()}...")
        try:
            question_pairs = extract_question_pairs(source_file, target_file, lang)
            all_question_pairs[lang] = question_pairs
            with open(output_file, 'w', encoding='utf-8') as outfile:
                json.dump(question_pairs, outfile, ensure_ascii=False, indent=2)

            print(f"Saved {len(question_pairs)} question-translation pairs to {output_file}")

        except Exception as e:
            print(f"Error processing {lang}: {str(e)}")


    combined_output_file = "results/all_question_pairs.json"
    with open(combined_output_file, 'w', encoding='utf-8') as outfile:
        json.dump(all_question_pairs, outfile, ensure_ascii=False, indent=2)

    print(f"\nSaved all question-translation pairs to {combined_output_file}")




if __name__ == "__main__":
    main()