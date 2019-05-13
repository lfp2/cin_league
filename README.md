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

## Disclaimer

_CIn League_ isn’t endorsed by Riot Games and doesn’t reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.
