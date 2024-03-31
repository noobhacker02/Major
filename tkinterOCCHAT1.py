import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import os
from openai import OpenAI
import tkinter as tk
from tkinter import scrolledtext, filedialog

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

def select_pdf():
    global pdf_path
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if pdf_path:
        extracted_text = extract_text_from_pdf(pdf_path, output_text_file)
        history.append({"role": "user", "content": extracted_text})
        chat_history.insert(tk.END, f'PDF loaded successfully: {pdf_path}\n')

def send_message():
    user_input = user_entry.get()
    history.append({"role": "user", "content": user_input})
    assistant_response = get_assistant_response(history)
    chat_history.insert(tk.END, f'You: {user_input}\n')
    chat_history.insert(tk.END, f'AI: {assistant_response}\n\n')
    chat_history.see(tk.END)
    user_entry.delete(0, tk.END)

def get_assistant_response(history):
    completion = client.chat.completions.create(
        model="TheBloke/Mistral-7B-Instruct-v0.2-GGUF/mistral-7b-instruct-v0.2.Q4_K_S.gguf",
        messages=history,
        temperature=0.7,
        stream=True,
    )
    assistant_response = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            assistant_response += chunk.choices[0].delta.content
    history.append({"role": "assistant", "content": assistant_response})
    return assistant_response

# Create the Tkinter window
window = tk.Tk()
window.title("Rizvite Study Assistant")
window.geometry("600x400")

# Chat history display
chat_history = scrolledtext.ScrolledText(window, width=60, height=20)
chat_history.pack(pady=10)

# Load PDF button
load_pdf_button = tk.Button(window, text="Load PDF", command=select_pdf)
load_pdf_button.pack()

# User input field
user_entry = tk.Entry(window, width=50)
user_entry.pack(pady=10)

# Send button
send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack()

# Initialize OpenAI client
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# Initial history
history = [
    {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
    {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise and always start your conversation and summarize any appended history."},
]

# Path to the output text file
output_text_file = 'extracted_text.txt'

# Start the Tkinter event loop
window.mainloop()
