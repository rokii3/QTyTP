import json

def find_question_in_alignment_file(question: str, alignment_file_path: str) -> list[str]:
    """
    Finds the given question in the specified local alignment file and returns a list of matching indices.
    """
    try:
        print(f"Searching for question in {alignment_file_path}...")
        matching_indices = []

        with open(alignment_file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                line_text = line.strip()
                if question in line_text:  # Check if the question is present in the line
                    matching_indices.append(str(i))

        return matching_indices

    except Exception as e:
        print(f"An error occurred while searching alignment file: {str(e)}")
        return []

def process_questions(question_file: str, alignment_file_path: str, output_file: str):
    """
    Processes the questions from the question file and finds their indices in the local alignment file.
    """
    try:
        with open(question_file, 'r', encoding='utf-8') as f:
            questions = json.load(f)

        question_indices = {}

        for idx, question in questions.items():  # Directly iterate through questions
            indices = find_question_in_alignment_file(question, alignment_file_path)
            if indices:
                question_indices[idx] = {
                    "question": question,  # Store the question itself
                    "indices": indices
                }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(question_indices, f, ensure_ascii=False, indent=2)

    except Exception as e:
        print(f"An error occurred while processing questions: {str(e)}")

if __name__ == "__main__":
    # Alignment file paths (local)
    alignment_files = {
        'af': "NLLB.af-en.af",
        'ar': "NLLB.ar-en.ar",
        'id': "NLLB.en-id.id",
        'mr': "NLLB.en-mr.mr"
    }

    for lang, lang_alignment_path in alignment_files.items():
        question_file = f'questions_{lang}.json'
        output_file = f'question_id_{lang}.json'

        print(f"\nProcessing {lang.upper()}...")
        process_questions(question_file, lang_alignment_path, output_file)  # No need for language_code