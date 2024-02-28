import os
import json
import requests
import cv2


def exist_url(url):
    if not url:
        return False
    print("exist_url( ", url, " )")
    try:
        r = requests.head(url, allow_redirects=True, timeout=10)
        if r.status_code == 200:
            return True
        elif r.status_code == 503:
            print("\tWARNING: " + url + " resulted in status code " + str(r.status_code))
            return True
        else:
            print("\tERROR: " + url + " resulted in status code " + str(r.status_code))
            return False
    except:
        return False


def create_safe_link(root, link: str, permalink=False):
    print("create_safe_link( ", root, ",", link, ", permalink=",permalink, " )")
    if exist_url(link):
        return link
    else:
        filename = root + "/" + link
        if os.path.exists(filename):
            if permalink:
                return "/" + filename
            else:
                return filename
    print("\tERROR: Could not find link =", link)
    return link


def verify_image_size(link):
    print("verify_image_size(", link, ")")
    if link is None:
        print("\tERROR:  verify_image_size was called with None")
        return False
    image = cv2.imread(link)
    if image is None:
        print("\tERROR:  verify_image_size did not find a file")
    height, width = image.shape[:2]
    if height == 128 and width == 128:
        return True
    else:
        print("\tERROR: ", link, " was not 128x128")
        return False


def style_name(name):
    if "Kenny" in name:
        return "<u>" + name + "</u>"
    return "<i>" + name + "</i>"


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
            if link:
                href = create_safe_link(root, link, permalink=True)
                link_name = base_name + str(idx + 1)
                links.append("<a class=\"link_button\" href=\"" + href + "\">" + link_name + "</a>")
    elif data:
        href = create_safe_link(root, data, permalink=True)
        links.append("<a class=\"link_button\" href=\"" + href + "\">" + base_name + "</a>")


def genereate_icon_tag(root, data):
    link = create_safe_link(root, data["icon-link"], permalink=False)  # We need to local file path and not the permalink file on the server
    verify_image_size(link)
    tag = ""
    tag += "<img src=\"/" + link + "\" alt=\"paper icon\""             # Observe we added the slash here to get the permalink path on the server.
    tag += " class =\"icon\""
    tag += ">"
    return tag


def trim(text):
    if text.endswith("."):
        return text[:-1]
    return text


def generate_paper_table_row(root, data):
    paper = ""
    paper += "<tr>\n"
    paper += "  <td class=\"pic\">\n"
    paper += "    " + genereate_icon_tag(root, data) + "\n"
    paper += "  </td>\n"
    paper += "  <td  class=\"text\">\n"
    if "prize" in data.keys():
        paper += "    " + trim(data["prize"]) + ": "
    paper += "<b>" + trim(data["title"]) + "</b>, by "
    paper += generate_authors_text(data["authors"]) + ". "
    paper += trim(data["venue"]) + " "
    paper += "(" + data["year"] + ").\n"
    paper += "<br>\n"

    links = []
    if "paper-link" in data.keys():
        generate_html_links("paper", root, data["paper-link"], links)
    if "book-link" in data.keys():
        generate_html_links("book", root, data["book-link"], links)
    if "thesis-link" in data.keys():
        generate_html_links("thesis", root, data["thesis-link"], links)
    if "abstract-link" in data.keys():
        generate_html_links("abstract", root, data["abstract-link"], links)
    if "poster-link" in data.keys():
        generate_html_links("poster", root, data["poster-link"], links)
    if "supp-link" in data.keys():
        generate_html_links("supplementary", root, data["supp-link"], links)
    if "video-link" in data.keys():
        generate_html_links("video", root, data["video-link"], links)
    if "code-link" in data.keys():
        generate_html_links("code", root, data["code-link"], links)
    if "data-link" in data.keys():
        generate_html_links("data", root, data["data-link"], links)
    if "web-link" in data.keys():
        generate_html_links("web", root, data["web-link"], links)
    if "publisher-link" in data.keys():
        generate_html_links("publisher", root, data["publisher-link"], links)
    if "doi-link" in data.keys():
        generate_html_links("DOI", root, data["doi-link"], links)
    if "slides-link" in data.keys():
        generate_html_links("slides", root, data["slides-link"], links)
    if "researchgate-link" in data.keys():
        generate_html_links("ResearchGate", root, data["researchgate-link"], links)
    N = len(links)
    if N > 0:
        paper += links[0]
        if N > 1:
            paper += ", \n"
        for i in range(1, N):
            paper += "    " + links[i]
            if i < N - 1:
                paper += ",\n"
        paper += ".\n"
    # 2024-02-28: BFI is no longer used in Denmark
    #if data["BFI"] != "None":
    #    paper += " (BFI " + data["BFI"] + ").\n"
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
                    html_paper = generate_paper_table_row(root, data)
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

    output_file = open("publications.html", 'w')
    output_file.write("---\n")
    output_file.write("layout : default\n")
    output_file.write("permalink : /publications/\n")
    output_file.write("---\n")

    output_file.write("<table class=\"main\"><tr><td>\n")
    output_file.write("<h1>Publications</h1>\n")
    output_file.write("</td></tr></table>\n")
    library = content.items()
    library = sorted(library, reverse=True)
    for collection in library:
        output_file.write("\n")
        output_file.write("<table class=\"main\"><tr><td>\n")
        output_file.write("<h2>" + collection[0] + "</h2>\n")
        output_file.write("</td></tr></table>\n")
        output_file.write("<table class=\"main\">\n")
        for paper in collection[1]:
            output_file.write(paper)
        output_file.write("</table>\n")
    output_file.close()
