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

def process_language_file(input_file: str, output_file: str, detector: QuestionDetector, language: str) -> int:
    """
    Process a single language file and extract questions.
    Returns the number of questions found.
    """
    try:
        # Read input file
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Filter questions
        questions = {}
        for idx, text in data.items():
            if detector.is_question(text, language):
                questions[idx] = text
        
        # Save questions
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)
            
        return len(questions)
        
    except Exception as e:
        print(f"Error processing {language}: {str(e)}")
        return 0

def main():
    # Initialize question detector
    detector = QuestionDetector()
    
    # List of languages to process
    languages = ['en', 'mr', 'ar', 'id', 'af']
    
    print("Starting question extraction...")
    total_questions = 0
    
    # Process each language
    for lang in languages:
        input_file = f'indexed_lines_{lang}.json'
        output_file = f'questions_{lang}.json'
        
        print(f"\nProcessing {lang.upper()}...")
        try:
            num_questions = process_language_file(input_file, output_file, detector, lang)
            total_questions += num_questions
            print(f"Found {num_questions} questions in {lang.upper()}")
            
            # Show first 3 questions as examples
            with open(output_file, 'r', encoding='utf-8') as f:
                questions = json.load(f)
                print(f"\nExample questions ({lang.upper()}):")
                for i, (idx, text) in enumerate(list(questions.items())[:3]):
                    print(f"{i+1}. [{idx}] {text}")
                    
        except FileNotFoundError:
            print(f"Warning: {input_file} not found. Skipping {lang}.")
        except Exception as e:
            print(f"Error processing {lang}: {str(e)}")
    
    print(f"\nTotal questions found across all languages: {total_questions}")

if __name__ == "__main__":
    main()