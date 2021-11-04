# Apriori analysis

Analyzing csv file with pandas and apriori algorithm.

## Team members

- Jason Carneiro
- Marcos Paulo
- Nicolas Fernando

## Setup (docker)

Clone the `.env.sample` file to `.env` and set the variable values.

```bash
cp .env.sample .env
```

### Database setup

Turn on database container using docker-compose file

```bash
docker-compose up
```

Run `setup-db` make command and put database password (`dba` as user and password)

```bash
make setup-db
```

Run Python script to populate the database

```bash
make run # takes you to the container
python populate_db.py # executes python script
```

### Analysis scripts

Install application requirements

**Obs: Using Python 3.9**

```bash
pip install -r requirements
```

Run analysis script

```bash
python analysis.py
```

Run apriori script

```bash
python apriori.py --min-sup 0.05 --min-conf 0.5
```

#### Output example (apriori script)

```text
ALL TRANSACTIONS
[{'support': 0.03518225039619651, 'confidence': 0.5692307692307692, 'rule': '9_7', 'combination': 'Medialuna - Coffee'}, {'support': 0.023666138404648707, 'confidence': 0.7044025157232704, 'rule': '60_7', 'combination': 'Toast - Coffee'}]
[RelationRecord(items=frozenset({9, 7}), support=0.03518225039619651, ordered_statistics=[OrderedStatistic(items_base=frozenset({9}), items_add=frozenset({7}), confidence=0.5692307692307692, lift=1.1898783636857841)]), RelationRecord(items=frozenset({60, 7}), support=0.023666138404648707, ordered_statistics=[OrderedStatistic(items_base=frozenset({60}), items_add=frozenset({7}), confidence=0.7044025157232704, lift=1.4724314954330286)])]
MORNING TRANSACTIONS
[{'support': 0.028515720204728246, 'confidence': 0.6, 'rule': '5_7', 'combination': 'Cookies - Coffee'}, {'support': 0.035827443334145746, 'confidence': 0.7205882352941176, 'rule': '60_7', 'combination': 'Toast - Coffee'}]
[RelationRecord(items=frozenset({7}), support=0.5149890324153059, ordered_statistics=[OrderedStatistic(items_base=frozenset(), items_add=frozenset({7}), confidence=0.5149890324153059, lift=1.0)]), RelationRecord(items=frozenset({5, 7}), support=0.028515720204728246, ordered_statistics=[OrderedStatistic(items_base=frozenset({5}), items_add=frozenset({7}), confidence=0.6, lift=1.1650733554188357)]), RelationRecord(items=frozenset({60, 7}), support=0.035827443334145746, ordered_statistics=[OrderedStatistic(items_base=frozenset({60}), items_add=frozenset({7}), confidence=0.7205882352941176, lift=1.3992302552824252)])]
AFTERNOON TRANSACTIONS
[{'support': 0.062291216348988016, 'confidence': 0.5372881355932203, 'rule': '30_7', 'combination': 'Sandwich - Coffee'}, {'support': 0.025545293770878365, 'confidence': 0.5579399141630901, 'rule': '8_7', 'combination': 'Pastry - Coffee'}]
[RelationRecord(items=frozenset({8, 7}), support=0.025545293770878365, ordered_statistics=[OrderedStatistic(items_base=frozenset({8}), items_add=frozenset({7}), confidence=0.5579399141630901, lift=1.2134000953743442)]), RelationRecord(items=frozenset({30, 7}), support=0.062291216348988016, ordered_statistics=[OrderedStatistic(items_base=frozenset({30}), items_add=frozenset({7}), confidence=0.5372881355932204, lift=1.1684868897580765)])]
EVENING TRANSACTIONS
[{'support': 0.06130268199233716, 'confidence': 0.5714285714285714, 'rule': '24_7', 'combination': 'Cake - Coffee'}, {'support': 0.022988505747126436, 'confidence': 0.6, 'rule': '82_80', 'combination': 'Postcard - Tshirt'}]
[RelationRecord(items=frozenset({24, 7}), support=0.06130268199233716, ordered_statistics=[OrderedStatistic(items_base=frozenset({24}), items_add=frozenset({7}), confidence=0.5714285714285714, lift=1.9885714285714287)]), RelationRecord(items=frozenset({80, 82}), support=0.022988505747126436, ordered_statistics=[OrderedStatistic(items_base=frozenset({82}), items_add=frozenset({80}), confidence=0.6000000000000001, lift=7.457142857142858)])]

```
