import re
import string


class TextPreprocessor:
    def clean_text(self, text):
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

    def process_text(self, text):
        """
        Cleans the input text by removing unnecessary characters.

        Args:
            text (str): The text to be processed.

        Returns:
            str: The processed text.
        """
        return self.clean_text(text)


# Example usage
if __name__ == "__main__":
    sample_text = "  Hello, World! This is a test text.  @2024! Let's clean it up.  "
    text_preprocessor = TextPreprocessor()
    processed_sample = text_preprocessor.process_text(sample_text)
    print("Original Text: ", sample_text)
    print("Processed Text: ", processed_sample)
