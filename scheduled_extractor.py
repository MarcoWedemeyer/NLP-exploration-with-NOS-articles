import extractor # Custom functions

link_categories = ["binnenland","buitenland","regio","politiek","economie","koningshuis",
                   "tech","cultuur-en-media","opmerkelijk"]

extractor.scrape(link_categories, path=".\\articles")
