import bs4 as bs
import urllib2
import pandas as pd

column_labels = ["Rank", "Person", "Total Gross", "Number of Movies",
                 "Average Gross", "Highest Gross Movie", "Gross"]
unstructured_list = []
structured_list = []

for i in range(1, 12):
    source = urllib2.urlopen\
        ("http://www.boxofficemojo.com/people/?view=Actor&pagenum={}&sort=sumgross&order=DESC&&p=.htm".format(i)).read()
    soup = bs.BeautifulSoup(source, "lxml")

    page = soup.get_text()
    page_lines = page.splitlines()

    gate = False
    for line in page_lines:
        if line.startswith("Sort: Alphabetical"):
            if not gate:
                gate = True
                starting_number = line.split("PictureGross")[1]
                unstructured_list.append(starting_number.encode("UTF8"))
            elif gate:
                gate = False
        if gate and not line.startswith("Sort: Alphabetical"):
            if line.strip():
                unstructured_list.append(line.encode("UTF8"))

for i in range(0, len(unstructured_list), 7):
    structured_list.append(unstructured_list[i: i+7])

df = pd.DataFrame.from_records(structured_list, columns=column_labels, index="Rank")
df.drop_duplicates(inplace=True)
print df

df.to_csv("top_actors_list.csv")