#!/usr/bin/env bash
# ==============================================================================
# Dream Equipment — 发布与元数据一致性门禁脚本
# ==============================================================================
# 用途：
#   1. 本地或 GitHub Actions 中快速校验 gradle.properties、build.gradle、
#      fabric.mod.json、dream_equipment.mixins.json、Java 源码及数据包/资源包的一致性。
#   2. 在缺少 Java / Maven 网络的受限沙箱中，提供无需启动 Gradle 的静态防回归门禁。
#
# 用法：
#   bash scripts/check_release_consistency.sh [--strict]
# ==============================================================================

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

STRICT=0
if [[ "${1:-}" == "--strict" ]]; then
  STRICT=1
fi

FAILURES=0

pass() {
  printf '  [PASS] %s\n' "$1"
}

fail() {
  printf '  [FAIL] %s\n' "$1" >&2
  FAILURES=$((FAILURES + 1))
}

warn() {
  printf '  [WARN] %s\n' "$1"
}

echo "==> [1/7] Checking required repository files..."
REQUIRED_FILES=(
  "gradle.properties"
  "build.gradle"
  "settings.gradle"
  "gradle/wrapper/gradle-wrapper.properties"
  "src/main/resources/fabric.mod.json"
  "src/main/resources/dream_equipment.mixins.json"
  "src/main/resources/data/dream_equipment/equipment_families.json"
  "src/main/resources/data/dream_equipment/set_effects.json"
  "README.md"
  "AGENT_BRIEF.md"
  "CURRENT_BASELINE.md"
  "CHANGELOG.md"
  "docs/ci/README.md"
  "docs/ci/compile-check.yml"
  "docs/ci/build.yml"
  "docs/ci/consistency.yml"
)

for f in "${REQUIRED_FILES[@]}"; do
  if [[ -f "$f" ]]; then
    pass "File exists: $f"
  else
    fail "Missing required file: $f"
  fi
done

echo "==> [2/7] Checking gradle.properties..."
prop() {
  local key="$1"
  grep -E "^${key}=" gradle.properties | head -n1 | cut -d'=' -f2- | tr -d '[:space:]'
}

MC_VERSION="$(prop minecraft_version)"
LOADER_VERSION="$(prop loader_version)"
LOOM_VERSION="$(prop loom_version)"
FAPI_VERSION="$(prop fabric_api_version)"
MOD_VERSION="$(prop mod_version)"
MAVEN_GROUP="$(prop maven_group)"
ARCHIVES_BASE="$(prop archives_base_name)"

for kv in \
  "minecraft_version:$MC_VERSION" \
  "loader_version:$LOADER_VERSION" \
  "loom_version:$LOOM_VERSION" \
  "fabric_api_version:$FAPI_VERSION" \
  "mod_version:$MOD_VERSION" \
  "maven_group:$MAVEN_GROUP" \
  "archives_base_name:$ARCHIVES_BASE"; do
  k="${kv%%:*}"
  v="${kv#*:}"
  if [[ -n "$v" ]]; then
    pass "gradle.properties $k = $v"
  else
    fail "gradle.properties $k is empty or missing"
  fi
done

if [[ "$FAPI_VERSION" == *"+${MC_VERSION}"* ]]; then
  pass "fabric_api_version ($FAPI_VERSION) suffix matches minecraft_version ($MC_VERSION)"
else
  fail "fabric_api_version ($FAPI_VERSION) does not match minecraft_version ($MC_VERSION)"
fi

if [[ "$STRICT" -eq 1 ]]; then
  if [[ "$MC_VERSION" == "26.3" ]]; then
    pass "Strict target: minecraft_version is 26.3"
  else
    fail "Strict target: expected minecraft_version=26.3, got $MC_VERSION"
  fi
  if [[ "$LOADER_VERSION" == "0.19.5" ]]; then
    pass "Strict target: loader_version is 0.19.5"
  else
    fail "Strict target: expected loader_version=0.19.5, got $LOADER_VERSION"
  fi
  if [[ "$FAPI_VERSION" == "0.160.7+26.3" ]]; then
    pass "Strict target: fabric_api_version is 0.160.7+26.3"
  else
    fail "Strict target: expected fabric_api_version=0.160.7+26.3, got $FAPI_VERSION"
  fi
fi

echo "==> [3/7] Checking Gradle Wrapper & Java 25 toolchain..."
WRAPPER_URL="$(grep -E '^distributionUrl=' gradle/wrapper/gradle-wrapper.properties | cut -d'=' -f2-)"
if [[ "$WRAPPER_URL" == *"gradle-9."* ]]; then
  pass "Gradle Wrapper uses Gradle 9.x ($WRAPPER_URL)"
else
  fail "Gradle Wrapper must be Gradle 9.x for Loom 1.17+ / Java 25 (got: $WRAPPER_URL)"
fi

if grep -q "JavaLanguageVersion.of(25)" build.gradle; then
  pass "build.gradle targets Java 25 (JavaLanguageVersion.of(25))"
else
  fail "build.gradle is missing Java 25 configuration"
fi

echo "==> [4/7] Checking fabric.mod.json & dream_equipment.mixins.json..."
python3 - "$MC_VERSION" "$LOADER_VERSION" "$FAPI_VERSION" <<'PY' || FAILURES=$((FAILURES + 1))
import json
import pathlib
import sys

mc_ver, loader_ver, fapi_ver = sys.argv[1:4]
errors = []

mod_json_path = pathlib.Path("src/main/resources/fabric.mod.json")
with mod_json_path.open("r", encoding="utf-8") as f:
    mod = json.load(f)

if mod.get("id") != "dream_equipment":
    errors.append(f"fabric.mod.json id mismatch: {mod.get('id')}")

depends = mod.get("depends", {})
mc_dep = depends.get("minecraft", "")
if mc_dep not in (mc_ver, f"~{mc_ver}", f">={mc_ver}"):
    errors.append(f"fabric.mod.json depends.minecraft='{mc_dep}' does not match '{mc_ver}'")

loader_dep = depends.get("fabricloader", "")
if loader_dep != f">={loader_ver}":
    errors.append(f"fabric.mod.json depends.fabricloader='{loader_dep}' expected '>={loader_ver}'")

fapi_dep = depends.get("fabric-api", "")
if fapi_dep != f">={fapi_ver}":
    errors.append(f"fabric.mod.json depends.fabric-api='{fapi_dep}' expected '>={fapi_ver}'")

java_dep = depends.get("java", "")
if java_dep != ">=25":
    errors.append(f"fabric.mod.json depends.java='{java_dep}' expected '>=25'")

for ep_group, classes in mod.get("entrypoints", {}).items():
    for cls in classes:
        java_path = pathlib.Path("src/main/java") / (cls.replace(".", "/") + ".java")
        if not java_path.is_file():
            errors.append(f"Entrypoint [{ep_group}] class missing: {java_path}")

for mixin_cfg in mod.get("mixins", []):
    cfg_path = pathlib.Path("src/main/resources") / mixin_cfg
    if not cfg_path.is_file():
        errors.append(f"Mixin config missing: {cfg_path}")
        continue
    with cfg_path.open("r", encoding="utf-8") as mf:
        mdata = json.load(mf)
    if mdata.get("compatibilityLevel") != "JAVA_25":
        errors.append(f"{mixin_cfg} compatibilityLevel='{mdata.get('compatibilityLevel')}' expected 'JAVA_25'")
    pkg = mdata.get("package", "")
    for key in ("mixins", "client", "server"):
        for mcls in mdata.get(key, []):
            full_path = pathlib.Path("src/main/java") / ((pkg + "." + mcls).replace(".", "/") + ".java")
            if not full_path.is_file():
                errors.append(f"Mixin class [{key}] missing: {full_path}")

if errors:
    for e in errors:
        print(f"  [FAIL] {e}", file=sys.stderr)
    sys.exit(1)
else:
    print("  [PASS] fabric.mod.json and dream_equipment.mixins.json validated successfully")
PY

echo "==> [5/7] Checking Minecraft 26.3 Java API invariants..."
if [[ "$STRICT" -eq 1 ]]; then
  if grep -rn "FuelValueEvents" src/main/java/ >/dev/null 2>&1; then
    fail "Removed Fabric API FuelValueEvents still referenced in src/main/java (use DataComponents.COOKING_FUEL via DefaultItemComponentEvents.MODIFY)"
  else
    pass "No removed FuelValueEvents references in src/main/java"
  fi

  if grep -rn -E "import net\.minecraft\.world\.item\.(AxeItem|ShovelItem|HoeItem);" src/main/java/ >/dev/null 2>&1; then
    fail "Removed vanilla 26.3 AxeItem/ShovelItem/HoeItem imports found in src/main/java"
  else
    pass "No removed AxeItem/ShovelItem/HoeItem imports in src/main/java"
  fi

  if grep -rn -E "\.drop\([^,]+,\s*(true|false)\s*\)" src/main/java/ >/dev/null 2>&1; then
    fail "Removed 2-arg Player#drop(ItemStack, boolean) call found in src/main/java (use 3-arg Prediction.SERVER_ONLY overload)"
  else
    pass "All drop(...) calls use 3-arg Prediction overload"
  fi

  if grep -rn "\.hurtMarked\b" src/main/java/ >/dev/null 2>&1; then
    fail "Renamed Entity#hurtMarked field found in src/main/java (use Entity#syncVelocity in 26.3)"
  else
    pass "All entity velocity sync flags use Entity#syncVelocity"
  fi

  if grep -rn "net\.minecraft\.world\.level\.block\.RedStoneWireBlock" src/main/java/ >/dev/null 2>&1; then
    fail "Renamed RedStoneWireBlock import found in src/main/java (use RedstoneWireBlock in 26.3)"
  else
    pass "RedStoneWireBlockMixin targets net.minecraft.world.level.block.RedstoneWireBlock"
  fi

  if grep -rn -E "\.knockback\([^,]+,\s*[^,]+,\s*[^,]+\s*\)" src/main/java/ >/dev/null 2>&1; then
    fail "Removed 3-arg LivingEntity#knockback(double, double, double) call found in src/main/java"
  else
    pass "All LivingEntity#knockback calls pass DamageSource and damage"
  fi
else
  warn "Skipping strict 26.3 API source checks (run with --strict to enforce)"
fi

echo "==> [6/7] Running Python data, resource, asset, and balance validators..."
for py_script in \
  "scripts/generate_equipment_resources.py" \
  "scripts/validate_equipment_families_json.py" \
  "scripts/validate_set_effects_json.py" \
  "scripts/audit_equipment_balance.py" \
  "scripts/validate_dream_equipment_assets.py"; do
  if python3 "$py_script"; then
    pass "Validator passed: $py_script"
  else
    fail "Validator failed: $py_script"
  fi
done

echo "==> [7/7] Checking documentation baseline references..."
if [[ "$STRICT" -eq 1 ]]; then
  for doc in README.md AGENT_BRIEF.md CURRENT_BASELINE.md; do
    if grep -q "26.3" "$doc"; then
      pass "$doc references Minecraft 26.3"
    else
      fail "$doc does not reference Minecraft 26.3"
    fi
  done
else
  pass "Documentation baseline check skipped in non-strict mode"
fi

echo ""
if [[ "$FAILURES" -gt 0 ]]; then
  echo "Consistency check FAILED with $FAILURES error(s)." >&2
  exit 1
fi

echo "All consistency checks PASSED."
