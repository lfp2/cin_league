# CIn League

Scripts written to gather, scrap and pre-process data for our project for the Data Mining course taken at the Informatics Center, Federal University of Pernambuco.<br>
Our idea is to build a decision machine for winning League of Legends matches.<br><br>

## Getting the data

Because the requested files are so large, we can't upload them with this project. In order to get them, run:

-   `python seed_matches.py` to get the seed JSON's from the Riot API;
-   `python get_match_ids.py` to scrap the ID's from seed JSON's;
-   `python match_decorator.py` to get more match informations based on the seeds

## Group

-   Gabriel Melo | gvmgs@cin.ufpe.br
-   Henrique Caúla | lhtc@cin.ufpe.br
-   Lavínia Pagannini | lfp2@cin.ufpe.br
