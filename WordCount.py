import string

# Function to count word occurrences in a text file
def count_word_occurrences(file_path, case_sensitive=True, stopwords=None, exclude_words=None):
    word_count = {}  # Dictionary to store word frequencies

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Use a more robust tokenization method
                words = line.strip().split()  # Split by whitespace and remove leading/trailing spaces
                for word in words:
                    if not case_sensitive:
                        word = word.lower()  # Convert word to lowercase if case-insensitive
                    if word not in string.punctuation:  # Exclude pure punctuation
                        if not stopwords or word.lower() not in stopwords:
                            if not exclude_words or word.lower() not in exclude_words:
                                if word in word_count:
                                    word_count[word] += 1
                                else:
                                    word_count[word] = 1

        return word_count

    except FileNotFoundError:
        return None

# Function to display word occurrences sorted by count
def display_word_occurrences(word_count):
    if not word_count:
        print("File not found.")
    else:
        sorted_word_count = dict(sorted(word_count.items(), key=lambda item: item[1], reverse=True))
        print("Unique words and their occurrences (sorted by count):")
        for word, count in sorted_word_count.items():
            print(f"{word}: {count}")

# Function to save word occurrences to a file
def save_word_occurrences_to_file(word_count, output_file):
    if not word_count:
        print("File not found.")
    else:
        try:
            with open(output_file, 'w', encoding='utf-8') as file:
                sorted_word_count = dict(sorted(word_count.items(), key=lambda item: item[1], reverse=True))
                file.write("Unique words and their occurrences (sorted by count):\n")
                for word, count in sorted_word_count.items():
                    file.write(f"{word}: {count}\n")
            print(f"Word occurrences saved to {output_file}")
        except Exception as e:
            print(f"Error saving to {output_file}: {str(e)}")

if __name__ == "__main__":
    file_path = input("Enter the path to the text file: ")  # Prompt user for file path

    # Add an option to specify case sensitivity, stopwords, and exclusion list
    case_sensitive = input("Case sensitivity (yes/no, default is yes): ").strip().lower() != "no"
    stopwords = input("Stopwords (comma-separated, leave empty for none): ").strip().split(",")
    exclude_words = input("Exclude words (comma-separated, leave empty for none): ").strip().split(",")

    result = count_word_occurrences(file_path, case_sensitive, stopwords, exclude_words)

    display_word_occurrences(result)

    save_option = input("Do you want to save word occurrences to a file? (yes/no): ").lower()
    if save_option == 'yes':
        output_file = input("Enter the output file name: ")
        save_word_occurrences_to_file(result, output_file)
