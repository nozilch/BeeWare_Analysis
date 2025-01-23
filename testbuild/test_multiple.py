import pytest

from briefcase.exceptions import BriefcaseCommandError

def test_multiple_apps_update(build_command, first_app, second_app, third_app):
    """Requesting an update of multiple specific apps updates only those apps."""
    # Add three apps
    build_command.apps = {
        "first": first_app,
        "second": second_app,
        "third": third_app,
    }

    # Configure command line options to update the first and third apps
    options, _ = build_command.parse_options(["-u", "first", "third"])

    # Run the build command for the first and third apps
    build_command(**options)

    # The right sequence of things will be done
    assert build_command.actions == [
        # Host OS is verified
        ("verify-host",),
        # Tools are verified
        ("verify-tools",),
        # App configs have been finalized for the first and third apps
        ("finalize-app-config", "first"),
        ("finalize-app-config", "third"),
        # First App exists, it will be updated then built.
        (
            "update",
            "first",
            {
                "test_mode": False,
                "update_requirements": False,
                "update_resources": False,
                "update_support": False,
                "update_stub": False,
            },
        ),
        # App template is verified for first app
        ("verify-app-template", "first"),
        # App tools are verified for first app
        ("verify-app-tools", "first"),
        ("build", "first", {"update_state": "first", "test_mode": False}),
        # Third App exists, it will be updated then built.
        (
            "update",
            "third",
            {
                "test_mode": False,
                "update_requirements": False,
                "update_resources": False,
                "update_support": False,
                "update_stub": False,
            },
        ),
        # App template is verified for third app
        ("verify-app-template", "third"),
        # App tools are verified for third app
        ("verify-app-tools", "third"),
        ("build", "third", {"update_state": "third", "test_mode": False}),
    ]



