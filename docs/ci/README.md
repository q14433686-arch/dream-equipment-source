# GitHub Actions CI 工作流模板（Dream Equipment 26.3）

> 本目录存放面向 GitHub Actions 的 CI 工作流模板（参考 `{UN}TACZR` / `TaCZ_Refabricated_Unofficial` 与 `chiseled-enchanting-table-26.1.2-source` 的 CI 架构）：
>
> - `compile-check.yml` — push / PR 快速编译门禁（Ubuntu + Temurin JDK 25 + Gradle 9.5.1，`compileJava compileTestJava processResources`）
> - `build.yml` — 完整构建、发布一致性校验、Python 资产/数据/平衡审计与 Jar 产物上传（支持 Tag Release）
> - `consistency.yml` — 轻量级静态一致性与资产/JSON/数值平衡门禁（无需启动 Gradle，耗时 < 30 秒）
>
> **为什么放在 `docs/ci/` 而不是直接写入 `.github/workflows/`？**
>
> Arena 沙箱中的 GitHub App 凭据未授予 `workflows` 权限，任何直接新增或修改 `.github/workflows/*.yml` 的提交在 `git push` 时都会被远端拒绝：
>
> ```text
> ! [remote rejected] ... (refusing to allow a GitHub App to create or update workflow `.github/workflows/...` without `workflows` permission)
> ```
>
> 因此工作流文件统一预置在 `docs/ci/`，由拥有仓库写权限的维护者一键复制到 `.github/workflows/` 激活。

## 激活步骤

在本地克隆仓库后执行：

```bash
mkdir -p .github/workflows
cp docs/ci/compile-check.yml .github/workflows/compile-check.yml
cp docs/ci/build.yml         .github/workflows/build.yml
cp docs/ci/consistency.yml   .github/workflows/consistency.yml
git add .github/workflows/
git commit -m "ci: activate GitHub Actions workflows for 26.3"
git push
```

## 本地等效自检

在无法访问外部 Maven 或未安装 JDK 25 的受限环境中，可直接运行静态一致性门禁与 Python 审计脚本：

```bash
bash scripts/check_release_consistency.sh --strict
python3 scripts/generate_equipment_resources.py
python3 scripts/validate_equipment_families_json.py
python3 scripts/validate_set_effects_json.py
python3 scripts/audit_equipment_balance.py
python3 scripts/validate_dream_equipment_assets.py
```

在具备 JDK 25 与网络环境的机器上，可运行与 `compile-check.yml` / `build.yml` 完全一致的 Gradle 门禁：

```bash
./gradlew --no-daemon compileJava compileTestJava processResources --stacktrace
./gradlew --no-daemon build --stacktrace
```
