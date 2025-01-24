def test_update_app_with_all_components(update_command, first_app, tmp_path):
    """如果用户请求更新所有组件，则所有组件都会被更新。"""
    update_command.update_app(
        update_command.apps["first"],
        update_requirements=True,
        update_resources=True,
        update_support=True,
        update_stub=True,
        test_mode=False,
    )

    # 正确的操作顺序
    assert update_command.actions == [
        ("verify-app-template", "first"),
        ("verify-app-tools", "first"),
        ("code", "first", False),
        ("requirements", "first", False),
        ("resources", "first"),
        ("cleanup-support", "first"),
        ("support", "first"),
        ("cleanup-stub", "first"),
        ("stub", "first"),
        ("cleanup", "first"),
    ]

    # 所有应用内容都被更新
    assert (tmp_path / "base_path/build/first/tester/dummy/code.py").exists()
    assert (tmp_path / "base_path/build/first/tester/dummy/requirements").exists()
    assert (tmp_path / "base_path/build/first/tester/dummy/resources").exists()
    assert (tmp_path / "base_path/build/first/tester/dummy/support").exists()
    assert (tmp_path / "base_path/build/first/tester/dummy/stub.exe").exists()
    # 并且应用包仍然存在
    assert (tmp_path / "base_path/build/first/tester/dummy/first.bundle").exists()

def test_update_app_failed_template_tool_verification(update_command, first_app, tmp_path, mocker):
    """如果模板或工具验证失败，则更新不应继续进行。"""
    # 模拟 verify_methods 抛出异常
    mocker.patch.object(update_command, 'verify_app_template', side_effect=Exception("模板验证失败"))
    mocker.patch.object(update_command, 'verify_app_tools', side_effect=Exception("工具验证失败"))

    try:
        update_command.update_app(
            update_command.apps["first"],
            update_requirements=False,
            update_resources=False,
            update_support=False,
            update_stub=False,
            test_mode=False,
        )
    except Exception as e:
        assert str(e) in ["模板验证失败", "工具验证失败"]

    # 如果验证失败，则不应执行任何操作
    assert update_command.actions == []
    # 不应更新任何文件
    assert not (tmp_path / "base_path/build/first/tester/dummy/code.py").exists()
    assert not (tmp_path / "base_path/build/first/tester/dummy/requirements").exists()
    assert not (tmp_path / "base_path/build/first/tester/dummy/resources").exists()
    assert not (tmp_path / "base_path/build/first/tester/dummy/support").exists()
    assert not (tmp_path / "base_path/build/first/tester/dummy/stub.exe").exists()
    # 并且应用包仍然存在
    assert (tmp_path / "base_path/build/first/tester/dummy/first.bundle").exists()

def test_update_app_failed_cleanup(update_command, first_app, tmp_path, mocker):
    """如果清理步骤失败，则更新应继续但记录错误。"""
    # 模拟 cleanup 方法抛出异常
    mocker.patch.object(update_command, 'cleanup', side_effect=Exception("清理失败"))

    update_command.update_app(
        update_command.apps["first"],
        update_requirements=False,
        update_resources=False,
        update_support=False,
        update_stub=False,
        test_mode=False,
    )

    # 尽管清理失败，仍应执行其他操作
    assert update_command.actions == [
        ("verify-app-template", "first"),
        ("verify-app-tools", "first"),
        ("code", "first", False),
        ("cleanup", "first"),
    ]

    # 应用内容已被更新
    assert (tmp_path / "base_path/build/first/tester/dummy/code.py").exists()
    # requirements 和 resources 均未被更新
    assert not (tmp_path / "base_path/build/first/tester/dummy/resources").exists()
    assert not (tmp_path / "base_path/build/first/tester/dummy/requirements").exists()
    # Support 未被更新
    assert not (tmp_path / "base_path/build/first/tester/dummy/support").exists()
    # Stub 未被更新
    assert not (tmp_path / "base_path/build/first/tester/dummy/stub.exe").exists()
    # 并且应用包仍然存在
    assert (tmp_path / "base_path/build/first/tester/dummy/first.bundle").exists()

def test_update_app_failed_component_update(update_command, first_app, tmp_path, mocker):
    """如果特定组件更新失败，则更新应停止并记录错误。"""
    # 模拟 update_code 方法抛出异常
    mocker.patch.object(update_command, 'update_code', side_effect=Exception("代码更新失败"))

    try:
        update_command.update_app(
            update_command.apps["first"],
            update_requirements=False,
            update_resources=False,
            update_support=False,
            update_stub=False,
            test_mode=False,
        )
    except Exception as e:
        assert str(e) == "代码更新失败"

    # 操作应在失败的组件后停止
    assert update_command.actions == [
        ("verify-app-template", "first"),
        ("verify-app-tools", "first"),
        ("code", "first", False),
    ]

    # 应用内容未被完全更新
    assert not (tmp_path / "base_path/build/first/tester/dummy/code.py").exists()
    # requirements 和 resources 均未被更新
    assert not (tmp_path / "base_path/build/first/tester/dummy/resources").exists()
    assert not (tmp_path / "base_path/build/first/tester/dummy/requirements").exists()
    # Support 未被更新
    assert not (tmp_path / "base_path/build/first/tester/dummy/support").exists()
    # Stub 未被更新
    assert not (tmp_path / "base_path/build/first/tester/dummy/stub.exe").exists()
    # 并且应用包仍然存在
    assert (tmp_path / "base_path/build/first/tester/dummy/first.bundle").exists()








