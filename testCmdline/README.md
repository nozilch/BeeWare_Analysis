# Briefcase Cmdline 测试

此目录包含对 Briefcase 命令行工具（`briefcase`）进行的单元测试，测试内容涵盖了 `briefcase -V` 命令、`dev` 和 `run` 命令，以及在不同操作系统（如 macOS 和 Windows）上的兼容性测试。

## 测试内容

- **Briefcase 版本检查命令 (`briefcase -V`)**：
  - 测试了 `briefcase -V` 命令，确保正确输出当前安装的 Briefcase 版本。
  
- **`dev` 和 `run` 命令**：
  - 对 `briefcase dev` 和 `briefcase run` 命令进行了功能性测试，确保命令执行时能够正常运行且符合预期行为。

- **macOS 兼容性**：
  - 测试了 Briefcase 是否能够在 macOS 系统上正确运行，包括平台相关的异常处理。
  
- **Windows 兼容性**：
  - 进行了对 Windows 平台上 Briefcase 命令行工具的兼容性测试，确保跨平台的一致性。


## 依赖

- Python 版本 >= 3.12
- `pytest`：用于测试框架。
- `pytest-mock`：用于在测试中进行对象和方法的模拟。

你可以通过以下命令安装依赖：

```bash
pip install -r requirements.txt
pip install pytest
```
## 运行测试

你可以使用 `pytest` 命令运行所有测试：

```bash
pytest
```
如果只想运行特定的测试文件，可以指定测试文件的路径：
```bash
pytest test_cmdline.py
```
