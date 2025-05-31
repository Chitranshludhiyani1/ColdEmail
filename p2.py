import google.generativeai as genai
import smtplib
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import csv
from PIL import Image, ImageTk

API_KEY = "enter your api"
genai.configure(api_key=API_KEY)

def generate_email():
    """LLM se email content generate karna"""
    prompt = (f"Write a {tone_var.get()} cold email for {recipient_entry.get()} "
              f"with the subject: {subject_entry.get()}. Keep it {tone_var.get()} and engaging. "
              f"Company Requirements: {requirements_entry.get()}")
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        body_text.delete("1.0", tk.END)
        body_text.insert("1.0", response.text)
    except Exception as e:
        messagebox.showerror("Error", f"LLM Error: {str(e)}")

def send_email():
    """SMTP se email bhejna"""
    sender_email = sender_entry.get()
    sender_password = password_entry.get()
    subject = subject_entry.get()
    body = body_text.get("1.0", tk.END)
    recipients = recipient_entry.get().split(',')
    
    if not sender_email or not sender_password or not subject or not body.strip():
        messagebox.showerror("Error", "All fields are required!")
        return
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        for recipient in recipients:
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(sender_email, recipient.strip(), message)
        
        server.quit()
        messagebox.showinfo("Success", "Emails sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send emails: {str(e)}")

def load_csv():
    """CSV se emails load karna"""
    file_path = filedialog.askopenfilename(filetypes=[["CSV Files", "*.csv"]])
    if not file_path:
        return
    
    try:
        with open(file_path, newline='') as file:
            reader = csv.reader(file)
            emails = [row[0] for row in reader if row]
            recipient_entry.delete(0, tk.END)
            recipient_entry.insert(0, ', '.join(emails))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load CSV: {str(e)}")

def toggle_password():
    if password_entry.cget('show') == '*':
        password_entry.config(show='')
        toggle_btn.config(text='Hide')
    else:
        password_entry.config(show='*')
        toggle_btn.config(text='Show')

def exit_program():
    root.destroy()

# Modern GUI
root = tk.Tk()
root.title("Cold Email Generator")
root.geometry("900x600")
root.configure(bg="#E3F2FD")

# Styling
style = ttk.Style()
style.configure("TFrame", background="#E3F2FD")
style.configure("TLabel", font=("Arial", 12, "bold"), background="#E3F2FD", foreground="#0D47A1")
style.configure("TButton", font=("Arial", 10, "bold"), background="#1565C0", foreground="black")
style.configure("TEntry", font=("Arial", 10))
style.configure("TNotebook.Tab", font=("Arial", 11, "bold"), padding=[10, 5])

# Tabs/notebook
notebook = ttk.Notebook(root)
main_frame = ttk.Frame(notebook)
settings_frame = ttk.Frame(notebook)
about_frame = ttk.Frame(notebook)
notebook.add(main_frame, text="Email Generator")
notebook.add(settings_frame, text="Settings")
notebook.add(about_frame, text="About Us")
notebook.pack(expand=True, fill='both')

# Main Frame Layout
sender_label = ttk.Label(main_frame, text="Sender Email")
sender_label.grid(row=0, column=0, sticky='w', pady=5)
sender_entry = ttk.Entry(main_frame, width=50)
sender_entry.grid(row=0, column=1, pady=5)

password_label = ttk.Label(main_frame, text="Password")
password_label.grid(row=1, column=0, sticky='w', pady=5)
password_entry = ttk.Entry(main_frame, width=50, show="*")
password_entry.grid(row=1, column=1, pady=5)

toggle_btn = ttk.Button(main_frame, text="Show", command=toggle_password)
toggle_btn.grid(row=1, column=2, padx=5)

recipient_label = ttk.Label(main_frame, text="Recipient Email(s)")
recipient_label.grid(row=2, column=0, sticky='w', pady=5)
recipient_entry = ttk.Entry(main_frame, width=50)
recipient_entry.grid(row=2, column=1, pady=5)

load_csv_btn = ttk.Button(main_frame, text="Load from CSV", command=load_csv)
load_csv_btn.grid(row=2, column=2, padx=5)

subject_label = ttk.Label(main_frame, text="Subject")
subject_label.grid(row=3, column=0, sticky='w', pady=5)
subject_entry = ttk.Entry(main_frame, width=50)
subject_entry.grid(row=3, column=1, pady=5)

requirements_label = ttk.Label(main_frame, text="Company Requirements")
requirements_label.grid(row=4, column=0, sticky='w', pady=5)
requirements_entry = ttk.Entry(main_frame, width=50)
requirements_entry.grid(row=4, column=1, pady=5)

tone_var = tk.StringVar(value="formal")
tone_menu = ttk.Combobox(main_frame, textvariable=tone_var, values=["formal", "friendly", "persuasive"])
tone_menu.grid(row=5, column=1, pady=5)

generate_btn = ttk.Button(main_frame, text="Generate Email", command=generate_email)
generate_btn.grid(row=6, column=1, pady=5)

body_text = scrolledtext.ScrolledText(main_frame, width=50, height=10, wrap=tk.WORD)
body_text.grid(row=7, column=1, pady=5)

send_btn = ttk.Button(main_frame, text="Send Email", command=send_email)
send_btn.grid(row=8, column=1, pady=10)

exit_btn = ttk.Button(root, text="Exit", command=exit_program)
exit_btn.pack(pady=10)

# About Us Page
ttk.Label(about_frame, text="Cold Email Generator v1.0", font=("Arial", 14, "bold")).pack(pady=10)
ttk.Label(about_frame, text="Developed by Chirag Solanli, Charinee Pandaw, Ayushi Tailor", font=("Arial", 12)).pack()
ttk.Label(about_frame, text="An efficient way to send bulk cold emails effortlessly.", font=("Arial", 10)).pack()

root.mainloop()
