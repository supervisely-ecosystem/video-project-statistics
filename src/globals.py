import os

import supervisely as sly

from dotenv import load_dotenv

if sly.is_development():
    # * For convinient development, has no effect in the production.
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))

api: sly.Api = sly.Api.from_env()

SLY_APP_DATA_DIR = sly.app.get_data_dir()

STATIC_DIR = os.path.join(SLY_APP_DATA_DIR, "static")
sly.logger.debug(f"Application static dir: {STATIC_DIR}")


class State:
    def __init__(self):
        self.selected_team = sly.io.env.team_id()
        self.selected_workspace = sly.io.env.workspace_id()
        self.selected_project = sly.io.env.project_id(raise_not_found=False)
        self.selected_dataset = sly.io.env.dataset_id(raise_not_found=False)

        self.selected_datasets = None

        self.continue_working = True


STATE = State()

sly.logger.debug(
    f"Selected team: {STATE.selected_team}. Selected workspace: {STATE.selected_workspace}."
    f"Selected project: {STATE.selected_project}. Selected dataset: {STATE.selected_dataset}."
)
