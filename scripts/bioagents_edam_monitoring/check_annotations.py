from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import glob
import json
import argparse
import yaml

VERBOSE = False


def remote_query(query, endpoint):
    endpoint.setQuery(query)
    try:
        result = endpoint.queryAndConvert()
        df = pd.DataFrame(result['results']['bindings'])
        df = df.applymap(lambda x: x['value'])
        return df
    except Exception as e:
        print(e)


def verbose_print(message):
    global VERBOSE
    if VERBOSE:
        print(message)


def main():
    global VERBOSE

    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--endpoint', required=True, help='Define endpoint in format http(s)://endpoint:port/repositories/name')
    parser.add_argument('-f', '--file', help='File path to output data')
    parser.add_argument('-q', '--query', help='Path to files with queries in regex format, e.g. ./queries/*.yaml',
                        default='./queries/*.yaml')
    parser.add_argument('-v', dest='verbose', action='store_true', default=False)
    args = parser.parse_args()

    VERBOSE = args.verbose

    ep_bioagents = SPARQLWrapper(args.endpoint)
    ep_bioagents.setReturnFormat(JSON)

    verbose_print('Running checks!')

    checks = glob.glob(args.query)
    if not len(checks):
        raise Exception('No queries were loaded.')

    verbose_print(f'Number of query files: {len(checks)}')

    results = {}
    for query_definition in checks:
        with open(query_definition, encoding='utf-8') as f:
            query = yaml.safe_load(f.read())
            verbose_print(f'> Running query: {query["metadata"]["name"]} (id: {query["metadata"]["id"]})')
            q_results = remote_query(query=query['query'], endpoint=ep_bioagents)
            match query['metadata']['output_type']:
                case 'listing':
                    output = json.loads(q_results.to_json(orient='records'))
                case 'count':
                    output = int(q_results['count'][0])
            results[query['metadata']['id']] = {'output_type': query['metadata']['output_type'], 'output': output}
            verbose_print(f'> Results: {json.dumps(output, indent=4)}')
            verbose_print('---')

    if args.file:
        with open(args.file, mode='w', encoding='utf-8') as f:
            json.dump(results, f)
    else:
        verbose_print('Final results:')
        print(json.dumps(results, indent=4))


if __name__ == '__main__':
    main()
