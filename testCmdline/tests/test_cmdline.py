import shlex
import sys
from typing import Union
from mock import mock
import pytest
from briefcase import __version__, cmdline
from briefcase.commands import ConvertCommand, DevCommand, NewCommand, UpgradeCommand
from briefcase.console import Console, LogLevel
from briefcase.exceptions import (
    InvalidFormatError,
    InvalidPlatformError,
    NoCommandError,
    UnsupportedCommandError,
)
from briefcase.platforms.linux.system import LinuxSystemCreateCommand
from briefcase.platforms.macOS.app import (
    macOSAppCreateCommand,
    macOSAppPublishCommand,
    macOSAppRunCommand,
)
from briefcase.platforms.windows.app import WindowsAppCreateCommand
# 定义一个pytest fixture，创建并返回一个Console实例
@pytest.fixture
def console() -> Console:
    return Console()
# 模拟命令行解析过程
def do_cmdline_parse(args: list, console: Console):
    """模拟解析命令行的过程。"""
    Command, extra_cmdline = cmdline.parse_cmdline(args)  # 解析命令行参数
    cmd = Command(console=console)  # 根据解析出的命令创建相应的Command对象
    options, overrides = cmd.parse_options(extra=extra_cmdline)  # 解析选项和覆盖项
    return cmd, options, overrides
# 测试`briefcase -V`命令，返回当前版本号
def test_version_only(capsys):
    """``briefcase -V`` 返回当前版本。"""
    with pytest.raises(SystemExit) as excinfo:
        cmdline.parse_cmdline("-V".split())  # 测试带有-V的输入
    # 正常退出，显示帮助
    assert excinfo.value.code == 0
    # 输出版本号
    output = capsys.readouterr().out
    assert output == f"{__version__}\n"
# 针对dev和run命令的公共测试。
@pytest.mark.skipif(sys.platform != "linux", reason="需要Linux系统")
def test_linux_default(console):
    """``briefcase create`` 在Linux上返回Linux创建系统命令。"""
    cmd, options, overrides = do_cmdline_parse("create".split(), console)
    assert isinstance(cmd, LinuxSystemCreateCommand)  # 检查cmd是否为LinuxSystemCreateCommand类型
    assert cmd.platform == "linux"  # 检查平台是否为linux
    assert cmd.output_format == "system"  # 检查输出格式是否为system
    assert cmd.console.input_enabled  # 检查Console是否启用了输入
    assert cmd.console.verbosity == LogLevel.INFO  # 检查Console的日志级别
    assert options == {}  # 确认选项为空

# 针对macOS平台的测试，确保在macOS上运行
@pytest.mark.skipif(sys.platform != "darwin", reason="需要macOS系统")
def test_macOS_default(console):
    """``briefcase create`` 在macOS上返回macOS创建命令。"""
    cmd, options, overrides = do_cmdline_parse("create".split(), console)
    assert isinstance(cmd, macOSAppCreateCommand)  # 检查cmd是否为macOSAppCreateCommand类型
    assert cmd.platform == "macOS"  # 检查平台是否为macOS
    assert cmd.output_format == "app"  # 检查输出格式是否为app
    assert cmd.console.input_enabled  # 检查Console是否启用了输入
    assert cmd.console.verbosity == LogLevel.INFO  # 检查Console的日志级别
    assert options == {}  # 确认选项为空
    assert overrides == {}  # 确认覆盖项为空

# 针对Windows平台的测试，确保在Windows上运行
@pytest.mark.skipif(sys.platform != "win32", reason="需要Windows系统")
def test_bare_command_version(capsys, console):
    """``briefcase create -V`` 返回版本号。"""
    with pytest.raises(SystemExit) as excinfo:
        do_cmdline_parse("create -V".split(), console)  # 测试带有-V的输入
    # 正常退出，显示帮助
    assert excinfo.value.code == 0
    # 输出版本号
    output = capsys.readouterr().out
    assert output == f"{__version__}\n"


def test_command_unknown_platform(monkeypatch, console):
    """``briefcase create foobar`` 会抛出一个未知平台错误。"""
    # 使用 monkeypatch 模拟当前系统为 macOS，无论测试实际在哪个系统运行。
    monkeypatch.setattr(sys, "platform", "darwin")

    # 定义预期的异常信息，匹配错误信息中的平台无效提示。
    expected_exc_regex = r"Invalid platform 'foobar'; \(choose from: .*\)"

    # 测试运行 "create foobar" 命令时，应该抛出 InvalidPlatformError 异常，并且匹配错误信息。
    with pytest.raises(InvalidPlatformError, match=expected_exc_regex):
        do_cmdline_parse("create foobar".split(), console)


def test_command_unknown_format(monkeypatch, console):
    """``briefcase create macOS foobar`` 返回一个格式无效的错误。"""
    # 使用 monkeypatch 模拟当前系统为 macOS，无论测试实际在哪个系统运行。
    monkeypatch.setattr(sys, "platform", "darwin")

    # 定义预期的异常信息，匹配错误信息中的格式无效提示。
    expected_exc_regex = r"Invalid format 'foobar'; \(choose from: app, Xcode\)"

    # 测试运行 "create macOS foobar" 命令时，应该抛出 InvalidFormatError 异常，并且匹配错误信息。
    with pytest.raises(InvalidFormatError, match=expected_exc_regex):
        do_cmdline_parse("create macOS foobar".split(), console)


def test_command_explicit_unsupported_format(monkeypatch, console):
    """``briefcase create macOS homebrew`` 会抛出错误，因为该格式暂时不支持。"""
    # 使用 monkeypatch 模拟输出格式，加入一个名为 "homebrew" 的格式，但该格式没有对应的命令实现。
    monkeypatch.setattr(
        cmdline,
        "get_output_formats",
        mock.MagicMock(return_value={"homebrew": None}),  # 模拟返回一个没有实现命令的 "homebrew" 格式
    )

    # 使用 monkeypatch 模拟当前系统为 macOS，无论测试实际在哪个系统运行。
    monkeypatch.setattr(sys, "platform", "darwin")

    # 测试运行 "create macOS homebrew" 命令时，应该抛出 UnsupportedCommandError 异常，并且匹配错误信息。
    with pytest.raises(
            UnsupportedCommandError,
            match=r"The create command for the macOS homebrew format has not been implemented \(yet!\).",
    ):
        do_cmdline_parse("create macOS homebrew".split(), console)

