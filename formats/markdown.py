
def text_to_markdown(text, filename):
    """
    Transforms a given text into a Markdown file.

    Parameters:
        text (str): The text content to be written into the Markdown file.
        filename (str): The name of the output Markdown file (e.g., "output.md").

    Returns:
        None
    """
    # Ensure the filename ends with .md
    if not filename.endswith(".md"):
        filename += ".md"

    # Write the text to the Markdown file
    with open(filename, "w", encoding="utf-8") as md_file:
        md_file.write(text)

    print(f"Markdown file '{filename}' has been created successfully!")


"""
# Example usage:
if __name__ == "__main__":
    sample_text = " " "
# Heading 1
This is a paragraph under the first heading.

## Heading 2
Here is a list:
- Item 1
- Item 2
- Item 3

### Subheading
You can also include **bold text**, *italic text*, and [links](https://example.com).
" " "
text_to_markdown(sample_text, "example_output")
"""