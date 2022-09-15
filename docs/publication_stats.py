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

    print("Total of ",
          len(papers),
          "works. ",
          nb_first_author,
          " First authored works, ",
          nb_last_author,
          " last authored works, and ",
          nb_single_author,
          " single authored works.",
          nb_prizes,
          " prizes received."
          )

    print("Corresponding author on ",
          nb_corresponding_author,
          "works. Total of ",
          nb_peer_reviewed,
          "peer reviewed works."
          )

    print(
          "Published works distributed as follows:\n \t",
          nb_journals,
          " journals, ",
          nb_conferences,
          " conferences, ",
          nb_workshops,
          " workshops, ",
          nb_books,
          " books, ",
          nb_book_chapters,
          " book chapters, ",
          nb_booklets,
          " booklets, ",
          nb_course_notes,
          " course notes, ",
          nb_abstracts,
          " abstracts, ",
          nb_posters,
          " posters, ",
          nb_techreports,
          " tech reports, ",
          nb_theses,
          " theses, ",
          nb_stars,
          " state-of-the-art reports.",
          nb_proceedings,
          " proceedings",
          nb_editorials,
          " editorials."
          )

    years = sorted(production.items(), reverse=False)
    first_year = years[0][0]
    last_year = years[-1][0]

    nb_active_years = last_year - first_year + 1
    print("Published work for ",
          nb_active_years,
          "years."
          )
    print("First work published in",
          first_year,
          "Last published work in ",
          last_year,
          "."
          )
    for year in range(first_year, last_year):
        if year not in production.keys():
            production[year] = 0

    data = list(sorted(production.items(), reverse=False))
    production_array = np.array(data)
    print("Average production of works per year is ",
          "{:.1f}".format(np.average(production_array[:, 1])),
          "works."
          )
    print("Standard deviation of number of works per year is ",
          "{:.1f}".format(np.std(production_array[:, 1])),
          "."
          )
    best_idx = np.argmax(production_array[:,1])
    print("Most productive year was, ",
          production_array[best_idx, 0],
          " with ",
          production_array[best_idx, 1],
          "published works."
          )

    print("")
    print("Distribution of works in most noticeable computer graphics venues are as follows")
    for venue in list(sorted(venues.items())):
        print(venue[0], "with", venue[1], " works.")
