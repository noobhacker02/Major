import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import os
from openai import OpenAI

def extract_text_from_pdf(pdf_path, output_text_file):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Initialize empty string to store extracted text
    extracted_text = ""

    # Loop through each page in the PDF
    for page_number in range(len(pdf_document)):
        # Get the page
        page = pdf_document.load_page(page_number)

        # Convert the page to a PIL Image
        image = page.get_pixmap()

        # Convert PIL Image to grayscale
        image = Image.frombytes("RGB", [image.width, image.height], image.samples)
        image = image.convert("L")

        # Use Tesseract OCR to extract text from the image
        page_text = pytesseract.image_to_string(image)

        # Append extracted text to the overall text
        extracted_text += page_text + "\n\n"

    # Close the PDF document
    pdf_document.close()

    # Write the extracted text to a text file
    with open(output_text_file, 'w', encoding='utf-8') as f:
        f.write(extracted_text)

    print(f'Extracted text saved to: {output_text_file}')
    return extracted_text

# Path to the input PDF file
pdf_path = 'aotq&a.pdf'

# Path to the output text file
output_text_file = 'extracted_text.txt'

# Call the function to extract text from the PDF
extracted_text = extract_text_from_pdf(pdf_path, output_text_file)

# Chat with an intelligent assistant in your terminal
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

history = [
    {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful and summerize any appened history.."},
    {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise and always start you conversation and summerize any appened history."},
]

# Append the extracted text to the history
history.append({"role": "user", "content": extracted_text})

while True:
    completion = client.chat.completions.create(
        model="TheBloke/Mistral-7B-Instruct-v0.2-GGUF/mistral-7b-instruct-v0.2.Q4_K_S.gguf",
        messages=history,
        temperature=0.7,
        stream=True,
    )

    new_message = {"role": "assistant", "content": ""}
   
    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            new_message["content"] += chunk.choices[0].delta.content

   
    history.append(new_message)
    
    # Uncomment to see chat history
    # import json
    # gray_color = "\033[90m"
    # reset_color = "\033[0m"
    # print(f"{gray_color}\n{'-'*20} History dump {'-'*20}\n")
    # print(json.dumps(history, indent=2))
    # print(f"\n{'-'*55}\n{reset_color}")

    print()
    history.append({"role": "user", "content": input("> ")})
