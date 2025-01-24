import pytest

from briefcase.exceptions import BriefcaseCommandError

def test_single_app_test_mode(build_command, first_app, second_app):
    """Requesting a test build of a single app updates and builds only that app."""
    # Add two apps
    build_command.apps = {
        "first": first_app,
        "second": second_app,
    }

    # Configure command line options to test only the first app
    options, _ = build_command.parse_options(["--test", "first"])

    # Run the build command for the first app
    build_command(**options)

    # The right sequence of things will be done
    assert build_command.actions == [
        # Host OS is verified
        ("verify-host",),
        # Tools are verified
        ("verify-tools",),
        # App config has been finalized for the first app
        ("finalize-app-config", "first"),
        # First App exists, it will be updated then built in test mode.
        (
            "update",
            "first",
            {
                "test_mode": True,
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
        ("build", "first", {"update_state": "first", "test_mode": True}),
    ]



