import os
import json
import requests
import cv2


def exist_url(url):
    try:
        r = requests.head(url)
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
    """

    :param link:
    :return:
    """
    image = cv2.imread(link)
    height, width = image.shape[:2]
    if height == 128 and width == 128:
        return True
    else:
        print("ERROR: ", link, " was not 128x128")
        return False


def generate_html_paper(root, data):
    paper = ""
    paper += "<tr>\n"
    paper += "  <td>\n"
    link = create_safe_link(root, data["icon-link"])
    verify_image_size(link)
    paper += "    <img src=\"" + link + "\" alt=\"paper icon\" width=\"64\" height=\"64\">\n"
    paper += "  </td>\n"
    paper += "  <td>\n"
    paper += "    " + data["authors"] + ": " + data["title"] + "." + data["venue"] + " (" + data["year"] + ").<br>\n"
    links = []
    if "video-link" in data.keys():
        link = create_safe_link(root, data["video-link"])
        links.append("<a href=\"" + link + "\">video</a>")
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
                try:
                    data = json.load(json_file)
                    year = data["year"]
                    html_paper = generate_html_paper(root, data)
                    if year not in content.keys():
                        content[year] = []
                    content[year].append(html_paper)
                except:
                    print("ERROR: ", json_file, " was corrupt?")
                json_file.close()
    return content


if __name__ == '__main__':
    content = read_json("pubs")
    markdown_file = open("publications.html", 'w')
    markdown_file.write("---\n")
    markdown_file.write("\n")
    markdown_file.write("---\n")
    markdown_file.write("<!DOCTYPE html>\n")
    markdown_file.write("<html>\n")
    markdown_file.write("<head>\n")
    markdown_file.write("<meta charset=\"utf-8\">\n")
    markdown_file.write("<title>Publications</title>\n")
    markdown_file.write("</head>\n")
    markdown_file.write("<body>\n")
    markdown_file.write("<h1>Publications</h1>\n")
    library = content.items()
    library = sorted(library)
    for collection in library:
        markdown_file.write("\n")
        markdown_file.write("<h2>" + collection[0] + "</h2>\n")
        markdown_file.write("<table>\n")
        for paper in collection[1]:
            markdown_file.write(paper)
        markdown_file.write("</table>\n")
    markdown_file.write("</body>\n")
    markdown_file.write("</html>\n")
    markdown_file.close()