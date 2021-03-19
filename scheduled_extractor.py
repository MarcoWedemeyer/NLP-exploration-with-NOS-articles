import extractor # Custom functions
from datetime import date
from time import sleep

print("""|----------------------------------------------|
| Executing daily scheduled NOS article scrape |
|----------------------------------------------|""")

link_categories = ["binnenland","buitenland","regio","politiek","economie","koningshuis",
                   "tech","cultuur-en-media","opmerkelijk"]

n_new, db_size = extractor.scrape(link_categories)
today = date.today().strftime("%d/%m/%Y")

with open("extractor_log.txt", "a") as log:
    log.write(f"{today}, {db_size}, {n_new}\n")

print()
print(f"{today}, {db_size}, {n_new}\n")
sleep(10)