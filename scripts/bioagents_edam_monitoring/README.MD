# Demo of framework for continuos integration
This is demo of a script, that could be run periodicaly and monitor important metrics about EDAM and it's usage in bio.agents.

## How to run
```
pip3 install -r requirements.txt
```
To run checks
```
cd ./scripts/bioagents_edam_monitoring
python3 check_annotations.py -e http://localhost:7200/repositories/Project25
```
## Available arguments
| Argument       | Description                                                                                  |
|----------------|----------------------------------------------------------------------------------------------|
| -h, --help     | show this help message and exit                                                              |
| -e, --endpoint | GraphDB endpoint with repository name, e.g. __http://localhost:7200/repositories/Project25__ |
| -f, --file     | Path to file, where JSON output is stored                                                    |
| -q, --query    | Pattern where query files are stored e.g. __./queries/*.query__                              |
| -v             | shows debug information while running script                                                 |

## Sample of query definition file (yaml)
```yaml
metadata:
    id: ID-OF-THE-METRIC
    description: METRIC-DESCRIPTION
    name: METRIC-NAME
    output_type: LISTING|COUNT
query: >
    SPARQL-QUERY (can span multiple lines)
```

## Contact
Contact me at adrian(at)ics.muni.cz