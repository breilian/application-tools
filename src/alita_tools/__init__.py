import logging
from importlib import import_module

from .github import get_tools as get_github, AlitaGitHubToolkit
from .openapi import get_tools as get_openapi
from .jira import get_tools as get_jira, JiraToolkit
from .confluence import get_tools as get_confluence, ConfluenceToolkit
from .gitlab import get_tools as get_gitlab, AlitaGitlabToolkit
from .gitlab_org import get_tools as get_gitlab_org, AlitaGitlabSpaceToolkit
from .zephyr import get_tools as get_zephyr, ZephyrToolkit
from .browser import get_tools as get_browser, BrowserToolkit
from .report_portal import get_tools as get_report_portal, ReportPortalToolkit
from .bitbucket import get_tools as get_bitbucket, AlitaBitbucketToolkit
from .testrail import get_tools as get_testrail, TestrailToolkit
from .testio import get_tools as get_testio, TestIOToolkit
from .xray import get_tools as get_xray_cloud, XrayToolkit
from .sharepoint import get_tools as get_sharepoint, SharepointToolkit
from .qtest import get_tools as get_qtest, QtestToolkit
from .zephyr_scale import get_tools as get_zephyr_scale, ZephyrScaleToolkit
from .zephyr_enterprise import get_tools as get_zephyr_enterprise, ZephyrEnterpriseToolkit
from .ado import get_tools as get_ado
from .ado.repos import AzureDevOpsReposToolkit
from .ado.test_plan import AzureDevOpsPlansToolkit
from .ado.work_item import AzureDevOpsWorkItemsToolkit
from .ado.wiki import AzureDevOpsWikiToolkit
from .rally import get_tools as get_rally, RallyToolkit
from .sql import get_tools as get_sql, SQLToolkit
from .code.sonar import get_tools as get_sonar, SonarToolkit
from .google_places import get_tools as get_google_places, GooglePlacesToolkit
from .yagmail import get_tools as get_yagmail, AlitaYagmailToolkit
from .cloud.aws import AWSToolkit
from .cloud.azure import AzureToolkit
from .cloud.gcp import GCPToolkit
from .cloud.k8s import KubernetesToolkit
from .custom_open_api import OpenApiToolkit as CustomOpenApiToolkit
from .elastic import ElasticToolkit
from .keycloak import KeycloakToolkit
from .localgit import AlitaLocalGitToolkit
from .pandas import PandasToolkit
from .azure_ai.search import AzureSearchToolkit, get_tools as get_azure_search

logger = logging.getLogger(__name__)

def get_tools(tools_list, *args, **kwargs):
    tools = []
    for tool in tools_list:
        if tool['type'] == 'openapi':
            tools.extend(get_openapi(tool))
        elif tool['type'] == 'github':
            tools.extend(get_github(tool))
        elif tool['type'] == 'jira':
            tools.extend(get_jira(tool))
        elif tool['type'] == 'confluence':
            tools.extend(get_confluence(tool))
        elif tool['type'] == 'gitlab':
            tools.extend(get_gitlab(tool))
        elif tool['type'] == 'gitlab_org':
            tools.extend(get_gitlab_org(tool))
        elif tool['type'] == 'zephyr':
            tools.extend(get_zephyr(tool))
        elif tool['type'] == 'browser':
            tools.extend(get_browser(tool))
        elif tool['type'] == 'yagmail':
            tools.extend(get_yagmail(tool))
        elif tool['type'] == 'report_portal':
            tools.extend(get_report_portal(tool))
        elif tool['type'] == 'bitbucket':
            tools.extend(get_bitbucket(tool))
        elif tool['type'] == 'testrail':
            tools.extend(get_testrail(tool))
        elif tool['type'] in ['ado_boards', 'ado_wiki', 'ado_plans', 'ado_repos']:
            tools.extend(get_ado(tool['type'], tool))
        elif tool['type'] == 'testio':
            tools.extend(get_testio(tool))
        elif tool['type'] == 'xray_cloud':
            tools.extend(get_xray_cloud(tool))
        elif tool['type'] == 'sharepoint':
            tools.extend(get_sharepoint(tool))
        elif tool['type'] == 'qtest':
            tools.extend(get_qtest(tool))
        elif tool['type'] == 'zephyr_scale':
            tools.extend(get_zephyr_scale(tool))
        elif tool['type'] == 'zephyr_enterprise':
            tools.extend(get_zephyr_enterprise(tool))
        elif tool['type'] == 'rally':
            tools.extend(get_rally(tool))
        elif tool['type'] == 'sql':
            tools.extend(get_sql(tool))
        elif tool['type'] == 'sonar':
            tools.extend(get_sonar(tool))
        elif tool['type'] == 'google_places':
            tools.extend(get_google_places(tool))
        elif tool['type'] == 'azure_search':
            tools.extend(get_azure_search(tool))
        else:
            if tool.get("settings", {}).get("module"):
                try:
                    settings = tool.get("settings", {})
                    mod = import_module(settings.pop("module"))
                    tkitclass = getattr(mod, settings.pop("class"))
                    toolkit = tkitclass.get_toolkit(**tool["settings"])
                    tools.extend(toolkit.get_tools())
                except Exception as e:
                    logger.error(f"Error in getting toolkit: {e}")
    return tools

def get_toolkits():
    return [
        AlitaGitHubToolkit.toolkit_config_schema(),
        TestrailToolkit.toolkit_config_schema(),
        JiraToolkit.toolkit_config_schema(),
        AzureDevOpsPlansToolkit.toolkit_config_schema(),
        AzureDevOpsWikiToolkit.toolkit_config_schema(),
        AzureDevOpsWorkItemsToolkit.toolkit_config_schema(),
        RallyToolkit.toolkit_config_schema(),
        QtestToolkit.toolkit_config_schema(),
        ReportPortalToolkit.toolkit_config_schema(),
        TestIOToolkit.toolkit_config_schema(),
        SQLToolkit.toolkit_config_schema(),
        SonarToolkit.toolkit_config_schema(),
        GooglePlacesToolkit.toolkit_config_schema(),
        BrowserToolkit.toolkit_config_schema(),
        XrayToolkit.toolkit_config_schema(),
        AlitaGitlabToolkit.toolkit_config_schema(),
        ConfluenceToolkit.toolkit_config_schema(),
        AlitaBitbucketToolkit.toolkit_config_schema(),
        AlitaGitlabSpaceToolkit.toolkit_config_schema(),
        ZephyrScaleToolkit.toolkit_config_schema(),
        ZephyrEnterpriseToolkit.toolkit_config_schema(),
        ZephyrToolkit.toolkit_config_schema(),
        AlitaYagmailToolkit.toolkit_config_schema(),
        SharepointToolkit.toolkit_config_schema(),
        AzureDevOpsReposToolkit.toolkit_config_schema(),
        AWSToolkit.toolkit_config_schema(),
        AzureToolkit.toolkit_config_schema(),
        GCPToolkit.toolkit_config_schema(),
        KubernetesToolkit.toolkit_config_schema(),
        CustomOpenApiToolkit.toolkit_config_schema(),
        ElasticToolkit.toolkit_config_schema(),
        KeycloakToolkit.toolkit_config_schema(),
        AlitaLocalGitToolkit.toolkit_config_schema(),
        PandasToolkit.toolkit_config_schema(),
        AzureSearchToolkit.toolkit_config_schema(),
    ]
