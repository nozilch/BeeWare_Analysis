import pytest

from briefcase.exceptions import BriefcaseCommandError

def test_single_app_update(build_command, first_app, second_app):
    """请求更新单个应用时，只有该应用会被更新。"""
    # 添加两个应用
    build_command.apps = {
        "first": first_app,
        "second": second_app,
    }

    # 配置命令行选项以仅更新第一个应用
    options, _ = build_command.parse_options(["-u", "first"])

    # 运行构建命令只构建第一个应用
    build_command(**options)

    # 正确的操作顺序
    assert build_command.actions == [
        # 验证主机操作系统
        ("verify-host",),
        # 验证工具
        ("verify-tools",),
        # 最终化第一个应用的配置
        ("finalize-app-config", "first"),
        # 第一个应用存在，它将被更新然后构建
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
        # 验证第一个应用的模板
        ("verify-app-template", "first"),
        # 验证第一个应用的工具
        ("verify-app-tools", "first"),
        ("build", "first", {"update_state": "first", "test_mode": False}),
    ]



