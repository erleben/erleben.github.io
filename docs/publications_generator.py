import os
import json
import requests
import cv2


def exist_url(url):
    try:
        r = requests.head(url, allow_redirects=True)
        if r.status_code == 200:
            return True
    except:
        return False


def create_safe_link(root, link: str):
    if exist_url(link):
        return link
    else:
        filename = root + "/" + link
        if os.path.exists(filename):
            return filename
    print("ERROR: Could not find link =", link)
    return None


def verify_image_size(link):
    image = cv2.imread(link)
    height, width = image.shape[:2]
    if height == 128 and width == 128:
        return True
    else:
        print("ERROR: ", link, " was not 128x128")
        return False


def generate_authors_text(data):
    if not isinstance(data, list):
        print("ERROR: ", data, " was not a list of author names")
        return ""
    return ""


def generate_html_links(base_name, root, data, links):
    """
    Generate a list of html link texts.

    :param base_name: The base name of the link that will appear in the html page
    :param root:      The path to the root of where local resources are stored.
    :param data:      The data imported from json file. This is a list of URLS or a single URL.
    :param links:     This is a list of html anchor tags.
    """
    if isinstance(data, list):
        for idx, link in enumerate(data):
            href = create_safe_link(root, link)
            link_name = base_name + str(idx + 1)
            links.append("<a href=\"" + href + "\">" + link_name + "</a>")
    else:
        href = create_safe_link(root, data)
        links.append("<a href=\"" + href + "\">" + base_name + "</a>")


def generate_html_paper(root, data):
    paper = ""
    paper += "<tr>\n"
    paper += "  <td>\n"
    link = create_safe_link(root, data["icon-link"])
    verify_image_size(link)
    paper += "    <img src=\"" + link + "\" alt=\"paper icon\" width=\"64\" height=\"64\">\n"
    paper += "  </td>\n"
    paper += "  <td>\n"
    paper += "    " + generate_authors_text(data["authors"]) + ": " + data["title"] + "." + data["venue"] + " (" + data[
        "year"] + ").<br>\n"
    links = []
    if "video-link" in data.keys():
        generate_html_links("video", root, data["video-link"], links)
    if "paper-link" in data.keys():
        link = create_safe_link(root, data["paper-link"])
        links.append("<a href=\"" + link + "\">paper</a>")
    if "code-link" in data.keys():
        link = create_safe_link(root, data["code-link"])
        links.append("<a href=\"" + link + "\">code</a>")
    if "data-link" in data.keys():
        link = create_safe_link(root, data["data-link"])
        links.append("<a href=\"" + link + "\">data</a>")
    if "web-link" in data.keys():
        link = create_safe_link(root, data["web-link"])
        links.append("<a href=\"" + link + "\">web</a>")
    N = len(links)
    if N > 0:
        paper += links[0]
        if N > 1:
            paper += ", \n"
        for i in range(1, N):
            paper += "    " + links[i]
            if i < N - 1:
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
                try:
                    data = json.load(json_file)
                    year = data["year"]
                    html_paper = generate_html_paper(root, data)
                    if year not in content.keys():
                        content[year] = []
                    content[year].append(html_paper)
                except ValueError as e:
                    print("ERROR: ", absolute_path, " was corrupt?")
                    print(e)
                json_file.close()
    return content


if __name__ == '__main__':
    content = read_json("pubs")
    markdown_file = open("publications.html", 'w')
    markdown_file.write("---\n")
    markdown_file.write("layout : default\n")
    markdown_file.write("---\n")
    markdown_file.write("<h1>Publications</h1>\n")
    library = content.items()
    library = sorted(library, reverse=True)
    for collection in library:
        markdown_file.write("\n")
        markdown_file.write("<h2>" + collection[0] + "</h2>\n")
        markdown_file.write("<table>\n")
        for paper in collection[1]:
            markdown_file.write(paper)
        markdown_file.write("</table>\n")
    markdown_file.close()
