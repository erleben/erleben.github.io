import os
import json
import requests


def exist_url(url):
    try:
        r = requests.head(url)
        if r.status_code == 200:
            return True
    except:
        return False


def get_safe_address(root, link: str):
    if exist_url(link):
        print("Found link =", link)
        return link
    else:
        filename = root + "/" + link
        if os.path.exists(filename):
            print("Found filename =", filename)
            return filename
    print("ERROR: Could not find link =", link)
    return None


def generate_html_paper(root, data):
    paper = ""
    paper += "<tr valign = \"top\">\n"
    paper += "  <td>\n"
    address = get_safe_address(root, data["icon"])
    paper += "    <img height=96 src = \"" + address + "\" alt = \"paper icon\">\n"
    paper += "  </td>\n"
    paper += "  <td>\n"
    paper += "    " + data["authors"] + ": " + data["title"] + "." + data["venue"] + " (" + data["year"] + ").<br>\n"
    links = []
    if "video-link" in data.keys():
        address = get_safe_address(root, data["video-link"])
        links.append("<a href=\"" + address + "\">video</a>")
    if "paper-link" in data.keys():
        address = get_safe_address(root, data["paper-link"])
        links.append("<a href=\"" + address + "\">paper</a>")
    if "code-link" in data.keys():
        address = get_safe_address(root, data["code-link"])
        links.append("<a href=\"" + address + "\">code</a>")
    if "data-link" in data.keys():
        address = get_safe_address(root, data["data-link"])
        links.append("<a href=\"" + address + "\">data</a>")
    if "web-link" in data.keys():
        address = get_safe_address(root, data["web-link"])
        links.append("<a href=\"" + address + "\">web</a>")
    N = len(links)
    if N > 0:
        paper += links[0]
        if N > 1:
            paper += ", \n"
        for i in range(1, N):
            paper += "    " + links[i]
            if i < N-1:
                paper += ", \n"
        paper += ".\n"
    paper += "  </td>\n"
    paper += "</tr>\n"
    return paper


def read_json(directory: str):
    content = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                absolute_path = os.path.join(root, file)
                json_file = open(absolute_path)
                data = json.load(json_file)
                year = data["year"]
                html_paper = generate_html_paper(root, data)
                if year not in content.keys():
                    content[year] = []
                content[year].append(html_paper)
                json_file.close()
    return content


if __name__ == '__main__':
    content = read_json("PUBLICATIONS")
    markdown_file = open("publications.md", 'w')

    library = content.items()
    library = sorted(library)

    for collection in library:
        markdown_file.write("\n")
        markdown_file.write("## " + collection[0] + "\n")
        markdown_file.write("<table border = \"0\" cellspacing = \"0\" cellpadding = \"0\">\n")
        for paper in collection[1]:
            markdown_file.write(paper)
        markdown_file.write("</table>\n")
    markdown_file.close()
