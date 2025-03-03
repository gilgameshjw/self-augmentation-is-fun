

import markdown
from weasyprint import HTML


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


def markdown_to_pdf(md_file_path, pdf_file_path):
    """
    Converts a Markdown file to a PDF.

    Args:
        md_file_path (str): Path to the input Markdown file.
        pdf_file_path (str): Path to save the output PDF file.
    """
    try:
        # Step 1: Read the Markdown file
        with open(md_file_path, "r", encoding="utf-8") as md_file:
            markdown_content = md_file.read()

        # Step 2: Convert Markdown to HTML
        html_content = markdown.markdown(markdown_content)

        # Step 3: Add basic HTML structure (optional)
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    margin: 20px;
                }}
                h1, h2, h3, h4, h5, h6 {{
                    color: #2c3e50;
                }}
                code {{
                    background-color: #f4f4f4;
                    padding: 2px 5px;
                    border-radius: 3px;
                }}
                pre {{
                    background-color: #f4f4f4;
                    padding: 10px;
                    border-radius: 5px;
                    overflow-x: auto;
                }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """

        # Step 4: Convert HTML to PDF using WeasyPrint
        HTML(string=full_html).write_pdf(pdf_file_path)

        print(f"PDF successfully created at: {pdf_file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

