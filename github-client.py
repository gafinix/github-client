import requests
from tqdm import tqdm
import os

def search_repos(query):
    url = f'https://api.github.com/search/repositories?q={query}'
    response = requests.get(url)
    if response.status_code == 200:
        repos = response.json().get('items', [])
        return repos[:5]  # Top 5 results
    return []

def download_repo(repo_url, repo_name):
    zip_url = f"{repo_url}/archive/main.zip"  # Assuming 'main' branch
    response = requests.get(zip_url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    with open(f"{repo_name}.zip", 'wb') as file, tqdm(
        total=total_size, unit='B', unit_scale=True
    ) as bar:
        for chunk in response.iter_content(chunk_size=1024):
            bar.update(len(chunk))
            file.write(chunk)

# Example Barista-style bot flow
def barista_bot():
    print("☕ Welcome to Repo Café! What can I fetch for you today?")
    query = input("Type in a repository keyword or name: ")
    repos = search_repos(query)

    if not repos:
        print("😔 Sorry, I couldn't find anything. Try another keyword!")
        return

    print("Here are some popular picks:")
    for i, repo in enumerate(repos, 1):
        print(f"{i}. {repo['name']} - {repo['html_url']}")

    choice = int(input("Pick a number to download (1-5): "))
    selected_repo = repos[choice - 1]
    download_repo(selected_repo['html_url'], selected_repo['name'])
    print(f"🎉 {selected_repo['name']} is ready for you in your folder!")

if __name__ == "__main__":
    barista_bot()
