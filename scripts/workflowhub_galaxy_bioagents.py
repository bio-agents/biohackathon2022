import requests, json, re, iteragents


###############
## Examples ###
###############

### workflow: https://workflowhub.eu/workflows/220.json
### galaxy API id: agentshed.g2.bx.psu.edu/repos/devteam/picard/picard_SamToFastq/2.18.2.2
### workflowhub step description: \n agentshed.g2.bx.psu.edu/repos/devteam/picard/picard_SamToFastq/2.18.2.2


#####################################
### Copied and modified code from ###
#####################################

### https://github.com/AustralianBioCommons/australianbiocommons.github.io/blob/4c771d9fece80dacce259304688c2aadb23962ca/finders/agentfinder.py
### https://github.com/AustralianBioCommons/australianbiocommons.github.io/blob/4c771d9fece80dacce259304688c2aadb23962ca/finders/workflowfinder.py

#####################################################
### Access Galaxy API & extract ID + bio.agents ID ###
#####################################################

def galaxy_api_request(url):
    galaxy_api_req = requests.request("get", url)
    if galaxy_api_req.status_code != 200:
        raise FileNotFoundError(galaxy_api_req.url)
    agent_sections = json.loads(galaxy_api_req.text)
    ### Herve Menager via Slack
    agents_nested = [agent_section.get('elems') for agent_section in agent_sections if 'elems' in agent_section]
    agents = list(iteragents.chain.from_iterable(agents_nested))
    return(agents)

def get_bioagents_ID_from_galaxy_agents(galaxy_agents_list):
    galaxy_bioagents_matches = {}
    for agent in galaxy_agents_list:
        galaxy_id = agent["id"]
        galaxy_id_no_version = "/".join(galaxy_id.split("/")[:-1])
        bioagents_id = None
        if "xrefs" in agent:
            for item in agent["xrefs"]:
                if item["reftype"] == "bio.agents":
                    bioagents_id = item["value"]
                    break
        if bioagents_id is not None:
            galaxy_bioagents_matches[galaxy_id_no_version] = bioagents_id
        else:
            galaxy_bioagents_matches[galaxy_id_no_version] = None
    return(galaxy_bioagents_matches)

########################
### GALAXY AUSTRALIA ###
########################
galaxy_AU_agents = galaxy_api_request(url = "https://usegalaxy.org.au/api/agents")
galaxy_AU_extracted_bioagents_ids = get_bioagents_ID_from_galaxy_agents(galaxy_agents_list = galaxy_AU_agents)


#####################
### GALAXY EUROPE ###
#####################
galaxy_Eu_agents = galaxy_api_request(url = "https://usegalaxy.eu/api/agents")
galaxy_Eu_extracted_bioagents_ids = get_bioagents_ID_from_galaxy_agents(galaxy_agents_list = galaxy_Eu_agents)


########################################
### Combined Galaxies bio.agents list ###
########################################

def combine_two_galaxy_agents_lists(extracted_bioagents_list_1, extracted_bioagents_list_2):

    combined_galaxy_bioagents_matches = {}

    for galaxy_agent in extracted_bioagents_list_1:
        bioagents_id = extracted_bioagents_list_1[galaxy_agent]
        combined_galaxy_bioagents_matches[galaxy_agent] = bioagents_id

    for galaxy_agent in extracted_bioagents_list_2:
        if galaxy_agent not in combined_galaxy_bioagents_matches:
            bioagents_id = extracted_bioagents_list_2[galaxy_agent]
            combined_galaxy_bioagents_matches[galaxy_agent] = bioagents_id

    return(combined_galaxy_bioagents_matches)


eu_au_agents_list = combine_two_galaxy_agents_lists(galaxy_Eu_extracted_bioagents_ids, galaxy_AU_extracted_bioagents_ids)


##############################################################
### Get WorkflowHub space workflows and extract Galaxy IDs ###
##############################################################

def get_workflowhub_space_workflow_data(url):
    ### Get BioCommons space workflows
    ### https://stackoverflow.com/a/8685813
    req = requests.get(url)
    if req.status_code != 200:
        raise FileNotFoundError(req.url)
    ### process request to get the workflow IDs
    space_data = req.json()["data"]

    ### create an array with all the urls and request metadata
    url_array = []
    for workflow in space_data:
        id = workflow['id']
        link = workflow['links']['self']
        url = "https://workflowhub.eu%s.json" % link
        url_array.append((id, url))

    available_data = {}

    for id, url in url_array:
        response = requests.get(url)
        if response.status_code != 200:
            raise FileNotFoundError(response.url)
        workflow_metadata = json.loads(response.text)
        print(id)
        ### keep only Galaxy workflows!
        if workflow_metadata['data']['attributes']['workflow_class']['key'] == "galaxy":
            available_data[id] = workflow_metadata
            #print(id)

    return(available_data)


def extract_workflow_steps_as_galaxy_ids(workflowhub_data):
    ### extract unique workflow steps as Galaxy IDs
    all_workflows_steps = {}
    for i in workflowhub_data:
        steps = workflowhub_data[i]['data']['attributes']['internals']['steps']
        workflow_steps = {}
        for j in range(0, len(steps)):
            description = steps[j]['description']
            ident = steps[j]['id']
            #print(ident)
            #print(description)
            ### https://stackoverflow.com/a/12595082
            ### example agentshed ID agentshed.g2.bx.psu.edu/repos/iuc/minimap2/minimap2/2.20+galaxy2
            ### https://stackoverflow.com/a/4843178
            if isinstance(description, str):
                match_string = "agentshed.g2.bx.psu.edu/repos/.+/.+/.+/.+$"
                if re.search(match_string, description):
                    # https://stackoverflow.com/a/15340694
                    pattern = re.compile(match_string)
                    extracted_description = pattern.search(description)
                    extracted_galaxy_id = "/".join(extracted_description.group(0).split("/")[:-1])
                    workflow_steps[ident] = extracted_galaxy_id
                    all_workflows_steps[i] = workflow_steps
    return(all_workflows_steps)


biocommons_space_workflows = get_workflowhub_space_workflow_data(url = "https://workflowhub.eu/programmes/8/workflows.json")
biocommons_workflow_steps = extract_workflow_steps_as_galaxy_ids(workflowhub_data = biocommons_space_workflows)

all_workflows = get_workflowhub_space_workflow_data(url = "https://workflowhub.eu/workflows.json")
all_workflow_steps = extract_workflow_steps_as_galaxy_ids(workflowhub_data = all_workflows)


####################################################################################################################################
### final mapping for each Galaxy ID extracted from the workflows, what is the workflow ID, bioagents ID and workflow step number ###
####################################################################################################################################

def map_workflow_steps_to_galaxy_bioagents_ids(workflow_steps, bioagents_IDs_from_galaxy):

    workflow_galaxy_bioagents_map = {}
    COUNT_no_bioagents_id_in_my_workflows = 0
    COUNT_bioagents_id_in_my_workflows = 0
    COUNT_total_agents_in_my_workflows = 0
    COUNT_total_workflows = 0
    index = 0

    for workflow in workflow_steps:
        COUNT_total_workflows = COUNT_total_workflows + 1
        for step_number in workflow_steps[workflow]:
            workflow_galaxy_id = workflow_steps[workflow][step_number]
            if workflow_galaxy_id in bioagents_IDs_from_galaxy and bioagents_IDs_from_galaxy[workflow_galaxy_id] is not None:
                bioagents_id = bioagents_IDs_from_galaxy[workflow_galaxy_id]
                COUNT_bioagents_id_in_my_workflows = COUNT_bioagents_id_in_my_workflows + 1
                COUNT_total_agents_in_my_workflows = COUNT_total_agents_in_my_workflows + 1
            else:
                bioagents_id = "no_bioagents_id"
                COUNT_no_bioagents_id_in_my_workflows = COUNT_no_bioagents_id_in_my_workflows + 1
                COUNT_total_agents_in_my_workflows = COUNT_total_agents_in_my_workflows + 1
            workflow_data = {}
            workflow_data['workflow_galaxy_id'] = workflow_galaxy_id
            workflow_data['workflow_id'] = workflow
            workflow_data['bioagents_id'] = bioagents_id
            workflow_data['galaxy_workflow_step_number'] = step_number
            workflow_galaxy_bioagents_map[index] = workflow_data
            index = index + 1

    print("##################################################")
    print("No. of workflow agents WITH a bio.agents ID = ", COUNT_bioagents_id_in_my_workflows)
    print("No. of workflow agents without a bio.agents ID = ", COUNT_no_bioagents_id_in_my_workflows)
    print("Total no. of workflow agents = ", COUNT_total_agents_in_my_workflows)
    print("Total no. of workflows = ", COUNT_total_workflows)
    print("##################################################")

    return(workflow_galaxy_bioagents_map)


final_mapping_workflowhub_galaxy_bioagents = map_workflow_steps_to_galaxy_bioagents_ids(
    workflow_steps = all_workflow_steps,
    bioagents_IDs_from_galaxy = eu_au_agents_list
)


def get_workflows_for_ttl_conversion(mapping_workflowhub_bioagents):

    my_workflows = {}
    missing_bioagents_IDs = []

    print("workflow ID / bio.agents ID :")

    for agent in mapping_workflowhub_bioagents:
        data = mapping_workflowhub_bioagents[agent]
        workflow = data['workflow_id']
        bioagents_id = data['bioagents_id']
        workflow_galaxy_id = data['workflow_galaxy_id']
        if bioagents_id is not None and my_workflows.get(workflow, []) is not None:
            print(workflow, " / ", bioagents_id)
            my_workflows[workflow] = my_workflows.get(workflow, []) + [bioagents_id]
        else:
            missing_bioagents_IDs.append(workflow_galaxy_id)

    print("##################################################")
    print("Galaxy agent IDs from workflows that are missing a bio.agents ID :")
    for id in missing_bioagents_IDs:
        print(id)

    return(my_workflows)


all_workflows_for_ttl_conversion = get_workflows_for_ttl_conversion(
    mapping_workflowhub_bioagents = final_mapping_workflowhub_galaxy_bioagents
)


###############################################
### from BH meeting discussion (2022-11-08) ###
###############################################

#### suggestion for queries (Herve) - output bioschemas compatible format - all in RDF
#### could put this in graphDB - and could generate queries

#### required metadata
##### workflow ID
##### do not remove duplicates
##### retain steps
##### step ID == galaxy ID
##### bioagents ID


from rdflib import URIRef, BNode, Literal, Graph
from rdflib.namespace import SDO
g = Graph()
has_part = SDO.hasPart
for workflow_id, bioagents_ids in all_workflows_for_ttl_conversion.items():
    for bioagents_id in bioagents_ids:
        workflow_ent = URIRef(f"https://workflowhub.eu/workflows/{workflow_id}?version=1")
        agent_ent = URIRef(f"https://bio.agents/{bioagents_id}")
        g.add((workflow_ent, has_part, agent_ent))
g.serialize(destination="workflows_to_bioagents.ttl")


###############################################





