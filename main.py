import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PDFCompressorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Compressor with Edge")
        self.file_paths = []

        # Upload Button
        self.upload_button = tk.Button(root, text="Upload PDFs", command=self.upload_files)
        self.upload_button.pack(pady=10)

        # Compress Button
        self.compress_button = tk.Button(root, text="Compress PDFs", command=self.compress_pdfs)
        self.compress_button.pack(pady=10)

    def upload_files(self):
        """Open file dialog to select multiple PDF files."""
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        self.file_paths = list(files)
        messagebox.showinfo("Uploaded Files", f"Selected {len(self.file_paths)} files.")

    def compress_pdfs(self):
        """Compress the uploaded PDFs using Smallpdf."""
        if not self.file_paths:
            messagebox.showwarning("No Files", "Please upload PDF files first.")
            return

        # Set up Edge WebDriver
        driver_path = r'C:\Users\tanay\Desktop\Python\namescraperbbdcollegepapers\msedgedriver.exe'  # Update with your actual path
        service = Service(driver_path)
        driver = webdriver.Edge(service=service)

        for file_path in self.file_paths:
            try:
                # Open the Smallpdf Compress PDF page
                driver.get("https://smallpdf.com/compress-pdf#r=compress")

                # Wait for the file input to be present and upload the PDF
                WebDriverWait(driver, 100).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
                ).send_keys(os.path.abspath(file_path))

                # Wait for the "Compress" button to be clickable using the updated XPath
                compress_button = WebDriverWait(driver, 120).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@aria-hidden="false" and contains(@class, "r5zwp6-1")]/span[text()="Compress"]'))
                )
                compress_button.click()

                # Wait for the compression to finish and the download button to appear using the new XPath
                download_button = WebDriverWait(driver, 123).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@aria-hidden="false" and contains(@class, "r5zwp6-1")]/span[text()="Download"]'))
                )
                download_button.click()

                # Optional: Wait for a moment to ensure the download completes
                time.sleep(7)

                # Click the specified button to prepare for the next upload
                next_upload_button = WebDriverWait(driver, 90).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "sc-1jsxb9n-1") and @tabindex="-1"]'))
                )
                next_upload_button.click()

                # Optional: Wait a bit before the next upload
                time.sleep(7)

            except Exception as e:
                messagebox.showerror("Error", f"Error processing file {file_path}: {str(e)}")

        driver.quit()
        messagebox.showinfo("Done", "All PDFs have been processed.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFCompressorApp(root)
    root.mainloop()
