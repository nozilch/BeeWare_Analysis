import pytest

from briefcase.exceptions import BriefcaseCommandError

def test_app_creation_failure(build_command, first_app_config, second_app):
    """If creating an app fails, an error is raised."""
    # Add two apps; use the "config only" version of the first app.
    build_command.apps = {
        "first": first_app_config,
        "second": second_app,
    }

    # Simulate a failure during app creation
    def mock_create(*args, **kwargs):
        raise BriefcaseCommandError("Failed to create app: first")

    build_command.create = mock_create

    # Configure command line options
    options, _ = build_command.parse_options(["-u", "--test"])

    # Run the build command
    with pytest.raises(
        BriefcaseCommandError,
        match=r"Failed to create app: first",
    ):
        build_command(**options)



