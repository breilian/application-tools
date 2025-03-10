from typing import List, Literal

from langchain_core.tools import BaseToolkit, BaseTool

from pydantic import create_model, BaseModel, ConfigDict, Field

from .api_wrapper import ReportPortalApiWrapper
from ..base.tool import BaseAction

name = "report_portal"


def get_tools(tool):
    return ReportPortalToolkit().get_toolkit(
        selected_tools=tool['settings'].get('selected_tools', []),
        endpoint=tool['settings']['endpoint'],
        api_key=tool['settings']['api_key'],
        project=tool['settings']['project']
    ).get_tools()


class ReportPortalToolkit(BaseToolkit):
    tools: list[BaseTool] = []

    @staticmethod
    def toolkit_config_schema() -> BaseModel:
        selected_tools = {x['name']: x['args_schema'].schema() for x in ReportPortalApiWrapper.model_construct().get_available_tools()}
        return create_model(
            name,
            endpoint=(str, Field(description="Report Portal endpoint")),
            project=(str, Field(description="Report Portal project")),
            api_key=(str, Field(description="User API key", json_schema_extra={'secret': True})),
            selected_tools=(List[Literal[tuple(selected_tools)]], Field(default=[], json_schema_extra={'args_schemas': selected_tools})),
            __config__=ConfigDict(json_schema_extra={'metadata': {"label": "Report Portal", "icon_url": None}})
        )

    @classmethod
    def get_toolkit(cls, selected_tools: list[str] | None = None, **kwargs):
        if selected_tools is None:
            selected_tools = []
        report_portal_api_wrapper = ReportPortalApiWrapper(**kwargs)
        available_tools = report_portal_api_wrapper.get_available_tools()
        tools = []
        for tool in available_tools:
            if selected_tools and tool["name"] not in selected_tools:
                continue
            tools.append(BaseAction(
                api_wrapper=report_portal_api_wrapper,
                name=tool["name"],
                description=tool["description"],
                args_schema=tool["args_schema"]
            ))
        return cls(tools=tools)

    def get_tools(self) -> list[BaseTool]:
        return self.tools
