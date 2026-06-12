# MISRA C++:2023 通用 Agent Skill

[English](README.md) | 中文

本仓库提供一个通用 AI agent skill，用于围绕 MISRA C++:2023 进行 C++ 项目评审、新代码编写指导，以及启发式安全门禁检查。

本 skill 由 GPT-5.5 在 xhigh reasoning effort 下创建。

## 为什么没有 `agents/openai.yaml`

这个 skill 的目标是跨 agent 运行时通用，而不是绑定 OpenAI 或 Codex。因此仓库只保留通用的 `SKILL.md`、参考资料和脚本，不包含 `agents/openai.yaml` 这类 OpenAI/Codex 专属 UI 元数据。

`.agents/skills/misra-cpp-2023/` 只是创建时使用的本地仓库布局。使用时可以把 `misra-cpp-2023` 文件夹复制到你的 agent 运行时所使用的 skill 目录。

## 内容

- `.agents/skills/misra-cpp-2023/SKILL.md` - 通用 skill 入口。
- `.agents/skills/misra-cpp-2023/references/` - 评审流程、编码指导、工具说明和轻量规则索引。
- `.agents/skills/misra-cpp-2023/scripts/scan_cpp_misra.py` - 启发式 C++ 安全扫描器。
- `.agents/skills/misra-cpp-2023/scripts/extract_rule_index.py` - 本地规则索引生成脚本。

## 本地源材料

创建工作区可以在 `docs/source-material/` 下保存已授权的本地材料，例如：

- `MISRA-CPP-2023_2.pdf`
- `misra-cpp-2023.txt`
- `misra-cpp-2023-study-notes.md`

该目录已被 git 忽略，不会发布到本仓库。

## 扫描器

```powershell
python .agents\skills\misra-cpp-2023\scripts\scan_cpp_misra.py <项目或文件> --format markdown
```

该扫描器是评审辅助工具，不是认证级 MISRA 检查器。

## 版权边界

本仓库刻意排除了 MISRA PDF、提取出的全文文本和本地学习笔记。完整规则措辞、示例、依据和例外应在本地使用已授权的 MISRA C++:2023 文档查看。

## 验证

```powershell
python -m unittest discover -s .agents\skills\misra-cpp-2023\scripts\tests -v
```

如果你的 agent 运行时提供 skill 校验器，请对 `.agents/skills/misra-cpp-2023` 执行校验。
