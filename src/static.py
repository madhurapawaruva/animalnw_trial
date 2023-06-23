import os
import glob

# ==================================================
# Constants
# ==================================================

LANDING_PAGE_TITLE = "Social Network Analysis of Animals"
LANDING_PAGE_WIDTH = 500
LANDING_PAGE_HEIGHT = 100

MAIN_WINDOW_HEIGHT = 800
MAIN_WINDOW_WIDTH = 1000

DATA_ROOT = "./datasets"
GRAPH_VERSION_FOLDER = "./results/graphs/"

GRAPH_DATA = {
    k.split("/")[-1].split(".")[0].replace("_", " "): {
        "path": k,
        "title": k.split("/")[-1].split(".")[0].replace("_", " "),
    } for k in glob.glob(os.path.join(DATA_ROOT, "**.graphml"))
}
#
# GRAPH_DATA = {
#     "bat": {
#         "path": os.path.join(
#             DATA_ROOT, "vampirebats_carter_mouth_licking_attribute_new.graphml"
#         ),
#         "title": "Placeholder for bat title",
#     },
#     "junglefowl": {
#         "path": os.path.join(
#             DATA_ROOT, "junglefowl_mcdonald_sexual_network_group9_attribute.graphml"
#         ),
#         "title": "Placeholder for junglefowl title",
#     },
# }

IDS = list(GRAPH_DATA.keys())

# Generated version table
versions = {}
for animal in GRAPH_DATA.keys():
    animal_folder = os.path.join(GRAPH_VERSION_FOLDER, animal)
    versions[animal] = ["default"]
    if os.path.isdir(animal_folder):
        filenames = [x for x in os.listdir(animal_folder) if x.endswith(".pkl")]
        filenames.sort()
        versions[animal].extend([x[:-4] for x in filenames])  # removing .pkl

# ==================================================
# Variables
# ==================================================


# static class of variables
class PageState:
    id = None
    path = None
    title = None
    landing_page = None
    welcome_page = None
    # TODO move selected_nodes, selected_edges here

    @staticmethod
    def clear():
        PageState.id = None

    @staticmethod
    def select_id(id):
        PageState.id = id
        PageState.graph_path = GRAPH_DATA[id]["path"]
        PageState.title = GRAPH_DATA[id]["title"]

    @staticmethod
    def select_version(version, is_next_version=False):
        if not is_next_version:  # this call is called when "select" button is clicked for dropdown.
            PageState.curr_version = version
            PageState.version = version
        else:  # this call is called when "save" button is called for retraining
            # PageState.curr_version = version
            PageState.version = version
        PageState.version_path = os.path.join(GRAPH_VERSION_FOLDER, PageState.id, version + ".pkl")
