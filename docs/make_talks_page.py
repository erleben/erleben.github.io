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


def generate_talk_table_row(root, data):
    paper = ""
    paper += "<tr>\n"
    #paper += "  <td class=\"pic\">\n"
    #paper += "    " + genereate_icon_tag(root, data) + "\n"
    #paper += "  </td>\n"
    paper += "  <td  class=\"text\">\n"
    paper += "<b>" + trim(data["title"]) + "</b>. "
    paper += trim(data["venue"]) + " "
    paper += " in " + data["month"] + " " + data["year"] + ".\n"
    links = []
    if "venue-link" in data.keys():
        generate_html_links("Venue", root, data["venue-link"], links)
    if "linkedin-link" in data.keys():
        generate_html_links("LinkedIn", root, data["linkedin-link"], links)
    if "twitter-link" in data.keys():
        generate_html_links("Twitter", root, data["twitter-link"], links)
    if "video-link" in data.keys():
        generate_html_links("Video", root, data["video-link"], links)
    if "image-link" in data.keys():
        generate_html_links("Image", root, data["image-link"], links)
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
                    html_paper = generate_talk_table_row(root, data)
                    if year not in content.keys():
                        content[year] = []
                    content[year].append(html_paper)
                except ValueError as e:
                    print("ERROR: ", absolute_path, " was corrupt?")
                    print(e)
                json_file.close()
    return content


if __name__ == '__main__':

    content = read_json("talks")

    output_file = open("talks.html", 'w')
    output_file.write("---\n")
    output_file.write("layout : default\n")
    output_file.write("permalink : /talks/\n")
    output_file.write("---\n")

    output_file.write("<table class=\"main\"><tr><td>\n")
    output_file.write("<h1>Talks and Outreach</h1>\n")
    output_file.write("<p>Here is a small collection of selected talks that I have done over the years.</p>\n")
    output_file.write("</td></tr></table>\n")
    library = content.items()
    library = sorted(library, reverse=True)
    output_file.write("<table class=\"main\">\n")
    for collection in library:
        output_file.write("\n")
        for talk in collection[1]:
            output_file.write(talk)
    output_file.write("</table>\n")
    output_file.close()
