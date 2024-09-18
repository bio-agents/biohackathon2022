INSTALLATION INSTRUCTIONS
=========================

These are the setup instructions that will allow you to run the notebooks available in this repository. Before starting to set this up, make sure you have **git** and **python** available on your machine.

Clone the repository
--------------------

From a shell, the command line should be:

`git clone git@github.com:bio-agents/biohackathon2022.git`

Set up Python dependencies and Jupyter
--------------------------------------

1. set up a virtual environment, and activate it!
This will prevent poluting your global python setup with libraries used only for this project

```
# navigate to the notebooks folder
cd biohackathon2022/notebooks
# set up virtualenv
python3 -m virtualenv .venv
# activate the virtualenv
. .venv/bin/activate
# (you can leave the virtualenv anytime if you type 'deactivate')
```

2. install python dependencies

we are going to use pip to install all python dependencies necessary to run jupyter and the notebooks

```
python -m pip install -r requirements.txt
```

3. run jupyter

just type the following in your shell:

```
jupyter-lab
```

The jupyter server will launch, and the web interface will be available locally on http://localhost:8888/tree

You can also use VisualSudioCode to visualise and run the *.ipynb notebook files.

Congrats, you're done with jupyter!

Set up GraphDB
--------------

1. Go to the GraphDB website to download it

You should register with an online form at https://www.ontotext.com/products/graphdb/download/. You will then receive a download link by email, and choose the appropriate installer for your OS.

2. Run the GraphDB installer

3. Run GraphDB!

Set up a New GraphDB repository
---------------

On the left panel, go to "Setup" and "Repositories" to create a new GraphDB repository.

<img src="https://user-images.githubusercontent.com/1140736/200505350-306912ac-ce99-44c9-98bc-3d603fa7421c.png" width="50%" style="display: flex; justify-content: center;">

Set up your GraphDB repository name to "Project25" (so all partcipants have the same name, it avoid conflicts down the line)
Leave all default options for the GraphDB repository.

<img src="https://user-images.githubusercontent.com/1140736/200505620-deeacd96-fcdf-4e98-a773-c2978fc7acb1.png" width="50%" style="display: flex; justify-content: center;">

Import the Data
-----------------

Click on the "Import" button on the left panel of the GraphDB Web interface, where you can upload bio.agents and EDAM from the following URLs:

EDAM: https://raw.githubusercontent.com/edamontology/edamontology/main/EDAM_dev.owl

bio.agents: https://raw.githubusercontent.com/bio-agents/content/master/datasets/bioschemas-dump.ttl

<img src="https://user-images.githubusercontent.com/1140736/200507732-c1640b5e-0b22-4781-be4f-bf5892f6a82a.png" width="50%" style="display: flex; justify-content: center;">

<img src="https://user-images.githubusercontent.com/1140736/200508241-62c52fb1-5c23-4bbe-9119-6bb0b6380ed3.png" width="50%" style="display: flex; justify-content: center;">


Dataset information
---------------------

As of today 10th of November, it seems like around 400 agents are missing from the bio.agents bioschemas turtle dump. The numbers are bound to change when the queries are re-run
