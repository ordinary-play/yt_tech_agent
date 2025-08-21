import tkinter as tk
from tkinter import scrolledtext, messagebox
from agent import run_agent
from fetch_trends import fetch_all_trends

def generate_from_topic():
    topic = entry.get().strip()
    if not topic:
        messagebox.showwarning("Input Required", "Please enter a topic or use Fetch Trending.")
        return
    result = run_agent(topic)
    show_result(result)

def generate_from_trend():
    topics = fetch_all_trends()
    if not topics:
        messagebox.showerror("Error", "No trending topics found.")
        return
    topic = topics[0]
    result = run_agent(topic)
    show_result(result)

def show_result(result):
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, f"Topic: {result['topic']}\n\n{result['script']}")
    messagebox.showinfo("Saved", f"Script saved!\nFile: {result['file']}\nDB ID: {result['id']}")

# --- UI Setup ---
root = tk.Tk()
root.title("YouTube Script Agent")
root.geometry("900x600")

frame = tk.Frame(root)
frame.pack(pady=10)

entry = tk.Entry(frame, width=60, font=("Arial", 12))
entry.pack(side=tk.LEFT, padx=5)

btn_custom = tk.Button(frame, text="Generate from Topic", command=generate_from_topic)
btn_custom.pack(side=tk.LEFT, padx=5)

btn_trend = tk.Button(frame, text="Fetch Trending", command=generate_from_trend)
btn_trend.pack(side=tk.LEFT, padx=5)

output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=25, font=("Consolas", 11))
output_box.pack(pady=10)

root.mainloop()
