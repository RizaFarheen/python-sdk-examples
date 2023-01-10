from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.workflow.task.simple_task import SimpleTask
from conductor.client.workflow.task.switch_task import SwitchTask
from conductor.client.workflow.task.task import TaskInterface

from examples.api import api_util
from examples.workflow.workflow_input import NotificationPreference

WORKFLOW_EXECUTOR = WorkflowExecutor(api_util.get_configuration())


def create_complex_workflow() -> ConductorWorkflow:
    global WORKFLOW_EXECUTOR
    return ConductorWorkflow(
        executor=WORKFLOW_EXECUTOR,
        name='user_notification',
        version=1,
    ).input_parameters(
        ['userId', 'notificationPref']
    ).add(
        create_get_user_details_task()
    ).add(
        create_email_or_sms_task()
    )


def create_get_user_details_task() -> TaskInterface:
    return SimpleTask(
        'get_user_info', 'get_user_info'
    ).input(
        'userId', '${workflow.input.userId}'
    )


def create_email_or_sms_task() -> TaskInterface:
    return SwitchTask(
        'emailorsms', '${workflow.input.notificationPref}'
    ).switch_case(
        NotificationPreference.EMAIL, create_send_email_task()
    ).switch_case(
        NotificationPreference.SMS, create_send_sms_task()
    )


def create_send_email_task() -> TaskInterface:
    return SimpleTask(
        'send_email', 'send_email'
    ).input(
        'email', '${get_user_info.output.email}'
    )


def create_send_sms_task() -> TaskInterface:
    return SimpleTask(
        'send_sms', 'send_sms'
    ).input(
        'phoneNumber', '${get_user_info.output.phoneNumber}'
    )
