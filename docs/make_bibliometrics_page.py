import os
import json
import numpy as np


class PaperInfo:

    def __init__(self):
        self.is_first_author = False
        self.is_last_author = False
        self.is_single_author = False
        self.is_corresponding_author = False
        self.is_peer_reviewed = False
        self.has_prize = False
        self.year = 0
        self.BFI = None
        self.is_journal = False
        self.is_conference = False
        self.is_workshop = False
        self.is_book = False
        self.is_book_chapter = False
        self.is_course_notes = False
        self.is_abstract = False
        self.is_poster = False
        self.is_thesis = False
        self.is_star = False
        self.is_proceedings = False
        self.is_tech_report = False
        self.is_editorial = False
        self.is_booklet = False
        self.venue = None


def parse_json_paper_data(json_paper_data):
    paper_info = PaperInfo()

    paper_info.venue = json_paper_data["venue"]

    if "True" in json_paper_data["reviewed"]:
        paper_info.is_peer_reviewed = True
    if "True" in json_paper_data["corresponding"]:
        paper_info.is_corresponding_author = True
    if "prize" in json_paper_data.keys():
        paper_info.has_prize = True
    paper_info.BFI = json_paper_data["BFI"]
    if "journal" in json_paper_data["type"]:
        paper_info.is_journal = True
    elif "Journal" in json_paper_data["type"]:
        paper_info.is_journal = True
    elif "course" in json_paper_data["type"]:
        paper_info.is_course_notes = True
    elif "conference" in json_paper_data["type"]:
        paper_info.is_conference = True
    elif "abstract" in json_paper_data["type"]:
        paper_info.is_abstract = True
    elif "chapter" in json_paper_data["type"]:
        paper_info.is_book_chapter = True
    elif "Chapter" in json_paper_data["type"]:
        paper_info.is_book_chapter = True
    elif "book" in json_paper_data["type"]:
        paper_info.is_book = True
    elif "poster" in json_paper_data["type"]:
        paper_info.is_poster = True
    elif "star" in json_paper_data["type"]:
        paper_info.is_star = True
    elif "techreport" in json_paper_data["type"]:
        paper_info.is_tech_report = True
    elif "Editorial" in json_paper_data["type"]:
        paper_info.is_editorial = True
    elif "editorial" in json_paper_data["type"]:
        paper_info.is_editorial = True
    elif "booklet" in json_paper_data["type"]:
        paper_info.is_booklet = True
    elif "Booklet" in json_paper_data["type"]:
        paper_info.is_booklet = True
    elif "Proceedings" in json_paper_data["type"]:
        paper_info.is_proceedings = True
    elif "proceedings" in json_paper_data["type"]:
        paper_info.is_proceedings = True
    elif "thesis" in json_paper_data["type"]:
        paper_info.is_thesis = True
    else:
        print("Unknown publication type =", json_paper_data["type"])

    my_author_name = "Kenny Erleben"
    author_data = json_paper_data["authors"]
    if isinstance(author_data, list):
        if len(author_data) == 1:
            # Verify that author name is me
            if my_author_name in author_data[0]:
                paper_info.is_single_author = True
        else:
            # Determine if I am the first or last author
            if my_author_name in author_data[0]:
                paper_info.is_first_author = True
            if my_author_name in author_data[-1]:
                paper_info.is_last_author = True
    else:
        # Verify that author name is me
        if my_author_name in author_data:
            paper_info.is_single_author = True

    year_str = json_paper_data["year"]
    paper_info.year = int(year_str)
    return paper_info


def parse_json_files_in_directory(directory: str, papers):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                absolute_path = os.path.join(root, file)
                json_file = open(absolute_path)
                try:
                    json_paper_data = json.load(json_file)
                    paper_info = parse_json_paper_data(json_paper_data)
                    papers.append(paper_info)
                except ValueError as e:
                    print("ERROR: ", absolute_path, " was corrupt?")
                    print(e)
                json_file.close()


if __name__ == '__main__':
    papers = []
    parse_json_files_in_directory("pubs", papers)

    nb_first_author = 0
    nb_single_author = 0
    nb_last_author = 0
    nb_prizes = 0
    nb_corresponding_author = 0
    nb_peer_reviewed = 0
    nb_journals = 0
    nb_conferences = 0
    nb_workshops = 0
    nb_books = 0
    nb_book_chapters = 0
    nb_course_notes = 0
    nb_abstracts = 0
    nb_posters = 0
    nb_theses = 0
    nb_stars = 0
    nb_proceedings = 0
    nb_editorials = 0
    nb_techreports = 0
    nb_booklets = 0

    venues = {"ACM Transactions on Graphics": 0, "VRIPHYS": 0, "Symposium on Computer Animation": 0, "SIGGRAPH": 0,
              "Computer Graphics Forum": 0, "MIG": 0, "Computers & Graphics": 0,
              "Transactions on Visualization and Computer Graphics": 0, "Visual Computer": 0,
              "Proceedings of the ACM on Computer Graphics and Interactive Techniques": 0}
    production = {}

    for paper in papers:
        if paper.is_corresponding_author:
            nb_corresponding_author += 1
        if paper.is_peer_reviewed:
            nb_peer_reviewed += 1
        if paper.is_journal:
            nb_journals += 1
        if paper.is_conference:
            nb_conferences += 1
        if paper.is_workshop:
            nb_workshops += 1
        if paper.is_book:
            nb_books += 1
        if paper.is_book_chapter:
            nb_book_chapters += 1
        if paper.is_course_notes:
            nb_course_notes += 1
        if paper.is_abstract:
            nb_abstracts += 1
        if paper.is_poster:
            nb_posters += 1
        if paper.is_thesis:
            nb_theses += 1
        if paper.is_star:
            nb_stars += 1
        if paper.is_proceedings:
            nb_proceedings += 1
        if paper.is_editorial:
            nb_editorials += 1
        if paper.is_booklet:
            nb_booklets += 1
        if paper.is_tech_report:
            nb_techreports += 1

        for key in venues.keys():
            if key in paper.venue:
                venues[key] += 1

        if paper.year in production.keys():
            production[paper.year] += 1
        else:
            production[paper.year] = 1
        if paper.is_first_author:
            nb_first_author += 1
        if paper.is_last_author:
            nb_last_author += 1
        if paper.is_single_author:
            nb_single_author += 1
        if paper.has_prize:
            nb_prizes += 1

    output_file = open("bibliometrics.html", 'w')
    output_file.write("---\n")
    output_file.write("layout : default\n")
    output_file.write("permalink : /bibliometrics/\n")
    output_file.write("---\n")
    output_file.write("<table class=\"main\"><tr><td>\n")
    output_file.write("<h1>Bibliometrics</h1>\n")
    output_file.write("</td></tr></table>\n")
    output_file.write("\n")
    output_file.write("<table class=\"main\">\n")

    txt = "Here is a list of links for various online places that keep track of all my research papers:" + "\n"
    output_file.write(txt)
    output_file.write("<br>\n")
    output_file.write("<br>\n")
    txt = "<ul>" \
          + "<li> Google Scholar: <a class =""link_button"" href=""https://scholar.google.com/citations?user=CQkvlpUAAAAJ&hl""> CQkvlpUAAAAJ & hl </a></li>\n" \
          + "<li> ResearchGate: <a class =""link_button"" href=""https://www.researchgate.net/profile/Kenny-Erleben/4"" > Kenny-Erleben </a></li>\n" \
          + "<li> ORCID: <a class =""link_button"" href=""https://orcid.org/0000-0001-6808-4747"" >0000-0001-6808-4747 </a></li>\n" \
          + "<li> DBLP: <a class =""link_button"" href=""https://dblp.org/pid/88/4453.html"" > 88 / 4453 </a></li>\n" \
          + "<li> Semantic Scholar: <a class =""link_button"" href=""https://www.semanticscholar.org/author/Kenny-Erleben/2253410"" > 2253410 </a></li>\n" \
          + "</ul>"
    output_file.write(txt)
    output_file.write("<br>\n")
    txt = "Total of " \
          + str(len(papers)) \
          + " works. " \
          + str(nb_first_author) \
          + " First authored works, " \
          + str(nb_last_author) \
          + " last authored works, " \
          + str(nb_single_author) \
          + " single authored works, and "\
          + str(nb_prizes) \
          + " prizes received.\n"
    output_file.write(txt)
    txt = "Corresponding author on " \
          + str(nb_corresponding_author) \
          + " works and a total of " \
          + str(nb_peer_reviewed) \
          + " peer reviewed works."\
          + "\n"
    output_file.write(txt)
    output_file.write("<br>")
    output_file.write("<br>")

    years = sorted(production.items(), reverse=False)
    first_year = years[0][0]
    last_year = years[-1][0]
    nb_active_years = last_year - first_year + 1
    txt = "Published for " \
          + str(nb_active_years) \
          + " years."\
          + "\n"
    output_file.write(txt)
    txt = "First work published in " \
          + str(first_year) \
          + " and last published work in " \
          + str(last_year) \
          + ".\n"
    output_file.write(txt)
    for year in range(first_year, last_year):
        if year not in production.keys():
            production[year] = 0
    data = list(sorted(production.items(), reverse=False))
    production_array = np.array(data)
    txt = "Average production per year is " \
          + "{:.1f}".format(np.average(production_array[:, 1])) \
          + " works.\n"
    output_file.write(txt)
    txt = "Standard deviation of number of works per year is " \
          + "{:.1f}".format(np.std(production_array[:, 1])) \
          + ".\n"
    output_file.write(txt)
    best_idx = np.argmax(production_array[:, 1])
    txt = "Most productive year was " \
          + str(production_array[best_idx, 0]) \
          + " with " + str(production_array[best_idx, 1]) \
          + " published works."\
          + "\n"
    output_file.write(txt)
    output_file.write("<br>")
    output_file.write("<br>")

    # + str(nb_workshops) + " workshops, " \
    txt = "Published works distributed as follows: " \
          + str(nb_journals) + " journals, " \
          + str(nb_conferences) + " conferences, " \
          + str(nb_books) + " books, " \
          + str(nb_book_chapters) + " book chapters, " \
          + str(nb_booklets) + " booklets, " \
          + str(nb_course_notes) + " course notes, " \
          + str(nb_abstracts) + " abstracts, " \
          + str(nb_posters) + " posters, " \
          + str(nb_techreports) + " technical reports, " \
          + str(nb_theses) + " theses, " \
          + str(nb_stars) + " state-of-the-art reports, " \
          + str(nb_proceedings) + " proceedings, " \
          + str(nb_editorials) + " editorials."\
          + "\n"
    output_file.write(txt)
    output_file.write("<br>")
    output_file.write("<br>")

    txt = "Distribution of works in most noticeable computer graphics venues are as follows:"\
          + "\n"
    output_file.write(txt)
    output_file.write("<br>\n")
    output_file.write("<br>\n")
    txt = "<ul>"
    for venue in list(sorted(venues.items())):
        txt += "<li>" \
               + str(venue[0]) \
              + " with " \
              + str(venue[1]) \
              + " works."\
              + "</li>"\
              + "\n"
    txt += "</ul>"
    output_file.write(txt)
    output_file.write("<br>")
    output_file.write("<br>")
    output_file.write("</table>\n")
    output_file.close()
