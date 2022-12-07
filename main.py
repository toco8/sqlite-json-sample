import sqlite3
from pathlib import Path


def main():
    con = sqlite3.connect('example.db')
    cur = con.cursor()

    query_create_table = '''\
        CREATE TABLE IF NOT EXISTS models (
            id VARCHAR PRIMARY KEY,
            name VARCHAR,
            metabolites JSON,
            original_bigg_ids JSON,
            annotation JSON,
            model_type VARCHAR
        );'''

    query_insert_values = '''\
        INSERT INTO models (id, name, metabolites, original_bigg_ids, annotation, model_type)
        VALUES (?, ?, ?, ?, ?, ?);'''

    query_select_json = '''\
        SELECT
            *
        FROM models, json_each(models.original_bigg_ids)
        ;'''

    metabolites = [
        (
            'ddca_c',
            'Dodecanoate (n-C12:0)',
            r'''json('{}')''',
            r'''json('{"original_bigg_ids": ["ddca", "ddca[c]", "ddca_c"]}')''',
            r'''json('{"annotation": [["MetaNetX (MNX) Chemical", "http://identifiers.org/metanetx.chemical/MNXM162258"]]}')''',
            'metabolites'
        )
    ]

    reactions = [
        (
            '12DGR120tipp',
            '1,2 diacylglycerol transport via flipping (periplasm to cytoplasm, n-C12:0)',
            r'''json('{"12dgr120_c": 1.0, "12dgr120_p": -1.0}')''',
            r'''json('{"original_bigg_ids": ["12DGR120tipp"]}')''',
            r'''json('{"annotation": [["MetaNetX (MNX) Equation", "http://identifiers.org/metanetx.reaction/MNXR94675"]]}')''',
            'reactions'
        )
    ]

    cur.execute(query_create_table)

    cur.executemany(query_insert_values, metabolites)
    cur.executemany(query_insert_values, reactions)

    cur.execute(query_select_json)
    print(cur.fetchall())

    con.close()
    exit()


if __name__ == '__main__':
    main()
