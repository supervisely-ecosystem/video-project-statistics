import supervisely as sly
from supervisely.app.widgets import (
    Card,
    SelectDataset,
    Button,
    Container,
    DatasetThumbnail,
    ProjectThumbnail,
    Text,
    Field,
)

import src.globals as g
import src.ui.settings as settings

load_button = Button("Load data")
change_button = Button("Change data")
change_button.hide()

wrong_input = Text("Please, select at least one dataset to continue.", status="warning")
wrong_input.hide()

input_container = Container()

card = Card(
    title="1️⃣ Input",
    description="Select the project and/or dataset to work with.",
    content=input_container,
    collapsable=True,
    content_top_right=change_button,
)

if g.STATE.selected_dataset:
    # * The application is launched of context menu of a dataset.
    sly.logger.info(
        f"The app is launched from the context menu of a dataset. "
        f"Project ID: {g.STATE.selected_project}. Dataset ID: {g.STATE.selected_dataset}."
    )
    project_info = g.api.project.get_info_by_id(g.STATE.selected_project)
    dataset_info = g.api.dataset.get_info_by_id(g.STATE.selected_dataset)
    dataset_thumbnail = DatasetThumbnail(project_info, dataset_info)
    input_container._widgets.append(dataset_thumbnail)

    settings.card.unlock()
    settings.card.uncollapse()
else:
    if g.STATE.selected_project:
        # * The application is launched of context menu of a project.
        sly.logger.info(
            f"The app is launched from the context menu of a project. "
            f"Project ID: {g.STATE.selected_project}."
        )
        project_info = g.api.project.get_info_by_id(g.STATE.selected_project)

        select_dataset = SelectDataset(
            project_id=g.STATE.selected_project,
            multiselect=True,
            compact=True,
            allowed_project_types=[sly.ProjectType.VIDEOS],
            show_label=False,
        )
    else:
        # * The application is launched from the Ecosystem.
        sly.logger.info("The app is launched from the Ecosystem.")

        select_dataset = SelectDataset(
            multiselect=True,
            allowed_project_types=[sly.ProjectType.VIDEOS],
            show_label=False,
        )

    select_field = Field(
        title="Select project",
        content=select_dataset,
    )

    project_thumbnail = ProjectThumbnail()
    project_thumbnail.hide()

    input_container._widgets.append(select_field)
    input_container._widgets.append(load_button)
    input_container._widgets.append(wrong_input)
    input_container._widgets.append(project_thumbnail)
    change_button.show()


@load_button.click
def load_data():
    selected_datasets = select_dataset.get_selected_ids()
    sly.logger.debug(f"Selected datasets: {selected_datasets}")
    if not selected_datasets:
        wrong_input.show()
        return

    wrong_input.hide()
    sly.logger.debug("Calling the API for Project ID of first selected dataset.")

    dataset_info = g.api.dataset.get_info_by_id(selected_datasets[0])
    selected_project = dataset_info.project_id

    sly.logger.debug(f"Selected project: {selected_project}")

    project_info = g.api.project.get_info_by_id(selected_project)
    project_thumbnail.set(project_info)
    project_thumbnail.show()

    g.STATE.selected_project = selected_project
    g.STATE.selected_datasets = selected_datasets

    sly.logger.debug(
        f"Saved selected project: {g.STATE.selected_project} and datasets: "
        f"{g.STATE.selected_datasets} in global state."
    )

    settings.card.unlock()
    settings.card.uncollapse()

    change_button.show()

    card.lock()
    card.collapse()


@change_button.click
def change_data():
    sly.logger.debug("Change data button was clicked")

    project_thumbnail.hide()
    change_button.hide()

    settings.card.lock()
    settings.card.collapse()

    card.unlock()
    card.uncollapse()

    g.STATE.selected_project = None
    g.STATE.selected_datasets = None

    sly.logger.debug("Cleared selected project and datasets in global state.")
