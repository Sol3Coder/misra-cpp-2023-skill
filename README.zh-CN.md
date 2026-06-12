# MISRA C++:2023 通用 Agent Skill

[English](README.md) | 中文

本仓库提供一个通用 AI agent skill，用于围绕 MISRA C++:2023 进行 C++ 项目评审、新代码编写指导，以及启发式安全门禁检查。

本 skill 由 GPT-5.5 在 xhigh reasoning effort 下创建。

## 内容

- `.agents/skills/misra-cpp-2023/SKILL.md` - 通用 skill 入口。
- `.agents/skills/misra-cpp-2023/references/` - 评审流程、编码指导、工具说明和轻量规则索引。
- `.agents/skills/misra-cpp-2023/scripts/scan_cpp_misra.py` - 启发式 C++ 安全扫描器。
- `.agents/skills/misra-cpp-2023/scripts/extract_rule_index.py` - 本地规则索引生成脚本。
- `docs/misra-cpp-2023-study-notes.md` - 可公开的学习摘要和执行模型，不复制标准正文。

## 本地源材料

本仓库中的轻量规则索引，是基于已授权的 MISRA C++:2023 PDF 在本地转换出的文本生成的。由于版权原因，本仓库不放置原始 PDF，也不放置转换后的全文文本。

如需重新生成本地规则索引或查看完整规则措辞，请把你已授权的本地材料放到 `docs/source-material/`：

- `MISRA-CPP-2023_2.pdf`
- `misra-cpp-2023.txt`

该目录已被 git 忽略，不会发布到本仓库。可公开的学习摘要位于 `docs/misra-cpp-2023-study-notes.md`。

## 扫描器

```powershell
python .agents\skills\misra-cpp-2023\scripts\scan_cpp_misra.py <项目或文件> --format markdown
```

该扫描器是评审辅助工具，不是认证级 MISRA 检查器。

## 版权边界

本仓库刻意排除了 MISRA PDF 和提取出的全文文本。完整规则措辞、示例、依据和例外应在本地使用已授权的 MISRA C++:2023 文档查看。

## 验证

```powershell
python -m unittest discover -s .agents\skills\misra-cpp-2023\scripts\tests -v
```

如果你的 agent 运行时提供 skill 校验器，请对 `.agents/skills/misra-cpp-2023` 执行校验。
