import os
import json
import requests
import cv2


def exist_url(url):
    try:
        r = requests.head(url, allow_redirects=True, timeout=10)
        if r.status_code == 200:
            return True
        elif r.status_code == 503:
            print("WARNING: " + url + " resulted in status code " + str(r.status_code))
            return True
        else:
            print("ERROR: " + url + " resulted in status code " + str(r.status_code))
            return False
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
    if link is None:
        print("ERROR:  verify_image_size was called with None")
        return False
    image = cv2.imread(link)
    height, width = image.shape[:2]
    if height == 128 and width == 128:
        return True
    else:
        print("ERROR: ", link, " was not 128x128")
        return False


def style_name(name):
    if "Kenny" in name:
        return "<strong>" + name + "</strong>"
    return name


def generate_authors_text(data):
    """

    :param data:
    :return:
    """
    if isinstance(data, list):
        if len(data) == 1:
            return style_name(data[0])
        else:
            authors = ""
            for idx, name in enumerate(data):
                if idx == len(data)-1:
                    authors += " and "
                elif idx > 0:
                    authors += ", "
                authors += style_name(name)
            return authors
    else:
        return style_name(data)


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


def genereate_icon_tag(root, data):
    link = create_safe_link(root, data["icon-link"])
    verify_image_size(link)
    tag = ""
    tag += "<img src=\"" + link + "\" alt=\"paper icon\""
    tag += " class =\"icon\""
    tag += ">"
    return tag


def trim(text):
    if text.endswith("."):
        return text[:-1]
    return text


def generate_html_paper(root, data):
    paper = ""
    paper += "<tr>\n"
    paper += "  <td class=\"pic\">\n"
    paper += "    " + genereate_icon_tag(root, data) + "\n"
    paper += "  </td>\n"
    paper += "  <td  class=\"text\">\n"
    paper += "    " + generate_authors_text(data["authors"]) + ": "
    paper += trim(data["title"]) + ". "
    paper += trim(data["venue"]) + " "
    paper += "(" + data["year"] + ").<br>\n"

    links = []
    if "paper-link" in data.keys():
        generate_html_links("paper", root, data["paper-link"], links)
    if "video-link" in data.keys():
        generate_html_links("video", root, data["video-link"], links)
    if "code-link" in data.keys():
        generate_html_links("code", root, data["code-link"], links)
    if "data-link" in data.keys():
        generate_html_links("data", root, data["data-link"], links)
    if "web-link" in data.keys():
        generate_html_links("web", root, data["web-link"], links)
    if "doi-link" in data.keys():
        generate_html_links("doi", root, data["doi-link"], links)
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

    markdown_file.write("<style>\n")
    markdown_file.write("img.icon\n")
    markdown_file.write("{\n")
    markdown_file.write("    aspect - ratio: 1;\n")
    markdown_file.write("    width: 64px;\n")
    markdown_file.write("    height: 64px;\n")
    markdown_file.write("    background-color: white;\n")
    markdown_file.write("    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);\n")
    markdown_file.write("    border: 1px solid #ddd;\n")
    markdown_file.write("    border-radius: 4px;\n")
    markdown_file.write("    padding: 4px;\n")
    markdown_file.write("}\n")
    markdown_file.write("td.pic\n")
    markdown_file.write("{\n")
    markdown_file.write("    width: 80px;\n")
    markdown_file.write("    text-align: center;\n")
    markdown_file.write("    vertical-align: top;\n")
    markdown_file.write("    padding-top: 10px;\n")
    markdown_file.write("    padding-bottom: 10px;\n")
    markdown_file.write("    padding-left: 0px;\n")
    markdown_file.write("    padding-right: 0px;\n")
    markdown_file.write("}\n")
    markdown_file.write("td.text\n")
    markdown_file.write("{\n")
    markdown_file.write("    width: 470px;\n")
    markdown_file.write("    text-align: left;\n")
    markdown_file.write("    vertical-align: top;\n")
    markdown_file.write("    padding-top: 10px;\n")
    markdown_file.write("    padding-bottom: 10px;\n")
    markdown_file.write("    padding-left: 10px;\n")
    markdown_file.write("    padding-right: 0px;\n")
    markdown_file.write("}\n")
    markdown_file.write("table.pubs\n")
    markdown_file.write("{\n")
    markdown_file.write("    border: none;\n")
    markdown_file.write("    width: 550px;\n")
    markdown_file.write("    margin-left: auto;\n")
    markdown_file.write("    margin-right: auto;\n")
    markdown_file.write("}\n")
    markdown_file.write("</style>\n")

    markdown_file.write("<h1>Publications</h1>\n")
    library = content.items()
    library = sorted(library, reverse=True)
    for collection in library:
        markdown_file.write("\n")
        markdown_file.write("<h2>" + collection[0] + "</h2>\n")
        markdown_file.write("<table class=\"pubs\">\n")
        for paper in collection[1]:
            markdown_file.write(paper)
        markdown_file.write("</table>\n")
    markdown_file.close()
