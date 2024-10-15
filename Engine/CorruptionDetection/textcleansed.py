import re
import string

def clean_text(text):
    """
    Cleans the input text by removing unnecessary characters, whitespace, and applying other transformations.
    
    Args:
        text (str): The text to be cleaned.
        
    Returns:
        str: The cleaned text.
    """
 
    cleaned_text = text.strip()

    cleaned_text = cleaned_text.lower()

    cleaned_text = cleaned_text.translate(str.maketrans('', '', string.punctuation))

    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', cleaned_text)

    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)

    return cleaned_text

def remove_stopwords(text, stopwords):
    """
    Removes stopwords from the cleaned text.
    
    Args:
        text (str): The cleaned text.
        stopwords (set): A set of stopwords to remove.
        
    Returns:
        str: The text with stopwords removed.
    """
    words = text.split()
    filtered_text = ' '.join(word for word in words if word not in stopwords)
    return filtered_text

def process_text(text, stopwords):
    """
    Cleans and processes the input text by removing unnecessary characters and stopwords.
    
    Args:
        text (str): The text to be processed.
        stopwords (set): A set of stopwords to remove.
        
    Returns:
        str: The processed text.
    """
    cleaned_text = clean_text(text)
    processed_text = remove_stopwords(cleaned_text, stopwords)
    return processed_text

# Example usage
if __name__ == "__main__":
    sample_text = "  Hello, World! This is a test text.  @2024! Let's clean it up.  "
    # Define a simple set of stopwords
    stopwords = {"is", "a", "the", "it", "up", "let's", "this"}
    
    processed_sample = process_text(sample_text, stopwords)
    print("Original Text: ", sample_text)
    print("Processed Text: ", processed_sample)
