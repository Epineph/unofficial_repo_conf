import requests
from bs4 import BeautifulSoup

def fetch_repos():
    url = "https://wiki.archlinux.org/title/unofficial_user_repositories"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    repos = []

    # Find all repository sections
    for section in soup.find_all('h3'):
        repo_name = section.get_text(strip=True)
        next_elem = section.find_next_sibling()

        if next_elem and next_elem.name == 'dl':
            key_id = None
            server_url = None
            for dt, dd in zip(next_elem.find_all('dt'), next_elem.find_all('dd')):
                if dt.get_text(strip=True) == 'Server:':
                    server_url = dd.get_text(strip=True)
                if dt.get_text(strip=True) == 'Key-ID:':
                    key_id = dd.get_text(strip=True)

            if repo_name and server_url and key_id:
                repos.append({
                    'name': repo_name,
                    'server': server_url,
                    'key': key_id
                })

    return repos

def main():
    repos = fetch_repos()
    for repo in repos:
        print(f"{repo['name']},{repo['server']},{repo['key']}")

if __name__ == "__main__":
    main()
