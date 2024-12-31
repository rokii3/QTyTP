import requests
import gzip
import json
from typing import Dict
import time

def download_and_index_lines(url: str, language: str, num_lines: int = 100, chunk_size: int = 8192) -> Dict[str, str]:
    """
    Downloads and indexes lines from a gzipped text file efficiently, preserving original corpus indices.
    
    Args:
        url: The URL of the gzipped text file
        language: Language identifier (e.g., 'en' or 'mr')
        num_lines: Number of lines to read (maximum)
        chunk_size: Size of chunks to download at a time
    """
    try:
        print(f"\nDownloading {language} text...")
        
        # Stream the download
        response = requests.get(url, stream=True)
        if not response.ok:
            print(f"Error downloading file: {response.status_code}")
            return {}

        # Create decompressor
        decompressor = gzip.GzipFile(fileobj=response.raw)
        
        # Variables for tracking
        indexed_lines = {}
        lines_processed = 0
        start_time = time.time()
        
        # Read the file in binary mode line by line
        while lines_processed < num_lines:
            try:
                line = decompressor.readline()
                if not line:  # End of file
                    break
                    
                # Decode and store the line with its original index
                line_text = line.decode('utf-8').strip()
                if line_text:  # Only store non-empty lines
                    indexed_lines[str(lines_processed)] = line_text
                
                lines_processed += 1
                
                # Progress update every 1000 lines
                if lines_processed % 1000 == 0:
                    elapsed = time.time() - start_time
                    speed = lines_processed / elapsed
                    print(f"Processed {lines_processed} lines... ({speed:.1f} lines/second)")
                    print(f"Currently at index {lines_processed-1}")
                    
            except EOFError:
                break
                
        elapsed = time.time() - start_time
        print(f"Completed {language} in {elapsed:.1f} seconds")
        print(f"Processed {lines_processed} lines ({lines_processed/elapsed:.1f} lines/second)")
        print(f"Stored {len(indexed_lines)} non-empty lines")
        
        # Print some sample indices and content
        sample_indices = sorted(list(indexed_lines.keys()))[:5]
        print("\nSample content:")
        for idx in sample_indices:
            print(f"Index {idx}: {indexed_lines[idx][:50]}...")
        
        return indexed_lines
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {}

def save_indexed_lines(indexed_lines: Dict[str, str], language: str):
    """Saves indexed lines to a JSON file."""
    output_file = f"indexed_lines_{language}.json"
    try:
        print(f"Saving to {output_file}...")
        # Save without pretty printing for better performance
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(indexed_lines, f, ensure_ascii=False)
        print(f"Saved {len(indexed_lines)} lines")
        
        # Print index range
        indices = list(map(int, indexed_lines.keys()))
        print(f"Index range: {min(indices)} to {max(indices)}")
    except Exception as e:
        print(f"Error saving file: {str(e)}")

def read_line_by_index(language: str, index: str) -> str:
    """Reads a specific line by its index."""
    file_path = f"indexed_lines_{language}.json"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get(str(index))
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return None

def read_parallel_lines(index: str, languages: list) -> dict:
    """
    Reads parallel lines from all specified language files.
    
    Args:
        index: The index to retrieve
        languages: List of language codes to retrieve
    
    Returns:
        Dictionary of language codes and their corresponding lines
    """
    return {lang: read_line_by_index(lang, index) for lang in languages}

if __name__ == "__main__":
    # URLs for all language files
    urls = {
        'en': "https://object.pouta.csc.fi/OPUS-NLLB/v1/mono/en.txt.gz",
        'mr': "https://object.pouta.csc.fi/OPUS-NLLB/v1/mono/mr.txt.gz",
        'af': "https://object.pouta.csc.fi/OPUS-NLLB/v1/mono/af.txt.gz",
        'ar': "https://object.pouta.csc.fi/OPUS-NLLB/v1/mono/ar.txt.gz",
        'id': "https://object.pouta.csc.fi/OPUS-NLLB/v1/mono/id.txt.gz"
    }
    
    # List of language codes
    languages = list(urls.keys())
    
    start_total = time.time()
    
    # Download and save all language files
    for lang, url in urls.items():
        indexed_lines = download_and_index_lines(url, lang)
        save_indexed_lines(indexed_lines, lang)
    
    total_time = time.time() - start_total
    print(f"\nTotal processing time: {total_time:.1f} seconds")
    
    # Example: Read parallel lines
    print("\nExample - Reading specific indices:")
    test_indices = ['0', '100', '1000']  # test a few specific indices
    for idx in test_indices:
        lines = read_parallel_lines(idx, languages)
        print(f"\nIndex {idx}:")
        for lang, text in lines.items():
            if text:
                print(f"{lang.upper()}: {text}")