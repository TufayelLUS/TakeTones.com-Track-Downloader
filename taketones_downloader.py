import tkinter as tk
import requests
import re
import tkinter.messagebox as messagebox


def handle_click(event):
    clipboard_text = window.clipboard_get()
    
    # Set the input field's text
    input_field.delete(0, tk.END)
    input_field.insert(0, clipboard_text)


def download_file():
    # Placeholder function for file download logic
    # print("File download initiated.")
    link = window.clipboard_get().strip()
    if not link.startswith("https://taketones.com/track/") and not link.startswith("https://www.taketones.com/track/"):
        messagebox.showerror("Invalid link", "Please paste a valid Taketones link")
        return
    messagebox.showinfo("Download started!", "Download started and will appear in the folder soon")
    download_button.configure(state=tk.DISABLED)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
    }
    try:
        resp = requests.get(link, headers=headers).text
    except:
        print("Failed to open {}".format(link))
        return
    
    track_id = re.findall(r'track_id":(.*?),', resp)[0]
    audio_id = re.findall(r'audio_id":(.*?),', resp)[0]
    api_link = f"https://api.taketones.com/v1/public/tracks/{track_id}/single/{audio_id}"
    file_name = resp.split('headerBrowseBlock__title--track">')[1].split('</h1>')[0]
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
    }
    try:
        response = requests.get(api_link, headers=headers, stream=True)
    except:
        print("Failed to open {}".format(link))
        return
    
    # Get the file size from the response headers
    file_size = int(response.headers.get("Content-Length", 0))
    
    bytes_downloaded = 0
    
    # Download the file in chunks and update the progress bar
    with open(file_name + ".mp3", "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
                bytes_downloaded += len(chunk)
                progress_mb = bytes_downloaded / 1024 / 1024
                total_mb = file_size / 1024 / 1024
                download_status.config(text=f"Download Progress: {progress_mb:.2f}/{total_mb:.2f} MB")
                window.update()
    

    messagebox.showinfo("Download finished!", "Download finished, check the folder for mp3 file now!")
    window.destroy()
    window.quit()


# Create the main window
window = tk.Tk()
window.title("File Downloader")


label = tk.Label(window, text="Copy a track link and click on the input field to paste")
label.pack(pady=10, padx=10)

# Create the input field
input_field = tk.Entry(window)
input_field.pack(pady=10, padx=10)
input_field.bind("<Button-1>", handle_click)


# Create the download button
download_button = tk.Button(window, text="Download", command=download_file)
download_button.pack(pady=10)

download_status = tk.Label(window, text="")
download_status.pack(pady=10)

# Run the application
window.mainloop()
