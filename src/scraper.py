from github import Github
from github import Auth
import os
import time
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("GITHUB_TOKEN") #Declare your token in .env file

auth = Auth.Token(token) #GitHub Authentication
g = Github(auth=auth)

def download_gcode_dataset(count_per_range=10):
    total_file_count = 0
    if not os.path.exists("data_raw"):
        os.makedirs("data_raw")
    for size in range(20000, 400000, 20000):
        query = f'G1 extension:gcode size:{size}..{size+19999}'
        print(f"Range: {size}-{size + 19999}")
        result = g.search_code(query)

        total_downloaded_bytes = 0
        file_count = 0

        print(f"Downloading {count_per_range} files")

        try:
            for file in result:
                if file_count >= count_per_range:
                    print(f"Downloaded {file_count} files. Ending...")
                    break
                try:
                    content = file.decoded_content
                    file_size = len(content)

                    file_name = f"data_raw/gcode_{total_file_count}.gcode"
                    with open(file_name, "wb") as f:
                        f.write(content)

                    total_downloaded_bytes += file_size
                    file_count += 1
                    total_file_count += 1

                    progress = (total_downloaded_bytes / count_per_range) * 100
                    print(f"[{progress:.2f}%] Downloaded: {file.name} ({file.size/1024} KB)")

                    if file_count % 10 == 0:
                        time.sleep(2)
                except Exception as e:
                    print(f"Error downloading gcode file {file.name}: {e}")
                    continue
        except Exception as e:
            if "rate limit" in str(e).lower():
                print(f"Rate limit exceeded. {e}")
            else:
                print(f"Error: {e}")
        print(f"Downloaded {file_count} gcode files. Total downloaded {total_downloaded_bytes/(1024*1024):.2f} MB.")
        time.sleep(5)

if __name__ == "__main__":
    download_gcode_dataset(100)
