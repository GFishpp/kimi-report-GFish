# OpenClaw 安全配置指南

> 本文档详细介绍 OpenClaw 的安全配置最佳实践，包括权限管理、敏感数据处理、沙箱设置和审计日志。

---

## 目录

1. [权限管理](#1-权限管理)
2. [敏感数据处理](#2-敏感数据处理)
3. [沙箱配置](#3-沙箱配置)
4. [审计日志](#4-审计日志)
5. [安全建议](#5-安全建议)

---

## 1. 权限管理

### 1.1 用户权限层级

OpenClaw 支持多层级权限控制，通过 YAML 配置文件实现细粒度权限管理。

#### 1.1.1 权限配置文件

```yaml
# ~/.openclaw/config/permissions.yaml
permissions:
  # 管理员权限 - 拥有所有操作权限
  admin:
    - "*"  # 通配符表示所有权限
  
  # 开发者权限 - 适合开发人员日常使用
  developer:
    - "exec:allow"           # 允许执行命令
    - "file:read"            # 允许读取文件
    - "file:write"           # 允许写入文件
    - "file:create"          # 允许创建文件
    - "web:search"           # 允许网络搜索
    - "browser:control"      # 允许浏览器控制
    - "kimi:search"          # 允许 Kimi 搜索
    - "message:send"         # 允许发送消息
    - "!exec:sudo"           # 禁止使用 sudo
    - "!exec:rm -rf /"       # 禁止危险删除命令
    - "!file:delete"         # 禁止删除文件
    - "!file:execute"        # 禁止执行文件
  
  # 只读权限 - 适合查看和监控
  readonly:
    - "file:read"
    - "web:search"
    - "kimi:search"
    - "!exec:*"              # 禁止所有执行权限
    - "!file:write"
    - "!file:delete"
    - "!file:create"
    - "!browser:control"
    - "!message:send"
  
  # 受限权限 - 适合自动化任务
  automation:
    - "exec:git"             # 仅允许 git 命令
    - "exec:python3"         # 仅允许 python3
    - "exec:node"            # 仅允许 node
    - "file:read"
    - "file:write"
    - "web:search"
    - "!exec:rm"             # 禁止删除命令
    - "!exec:curl"           # 禁止 curl
    - "!exec:wget"           # 禁止 wget
```

#### 1.1.2 权限配置加载

```python
# lib/permission_manager.py
import yaml
import re
from typing import List, Dict, Set
from functools import lru_cache

class PermissionManager:
    """权限管理器"""
    
    def __init__(self, config_path: str = "~/.openclaw/config/permissions.yaml"):
        self.config_path = config_path
        self.permissions: Dict[str, List[str]] = {}
        self._load_config()
    
    def _load_config(self):
        """加载权限配置"""
        import os
        expanded_path = os.path.expanduser(self.config_path)
        
        try:
            with open(expanded_path, 'r') as f:
                config = yaml.safe_load(f)
                self.permissions = config.get('permissions', {})
        except FileNotFoundError:
            # 使用默认配置
            self.permissions = {
                'default': ['file:read', 'web:search', 'kimi:search']
            }
    
    def check_permission(self, user_role: str, action: str) -> bool:
        """
        检查用户是否有权限执行操作
        
        Args:
            user_role: 用户角色
            action: 操作标识，如 "exec:git"
        
        Returns:
            bool: 是否有权限
        """
        role_perms = self.permissions.get(user_role, [])
        
        # 检查是否有通配符权限
        if "*" in role_perms:
            return True
        
        # 检查显式允许
        has_allow = False
        for perm in role_perms:
            if perm.startswith('!'):
                continue
            if self._match_permission(perm, action):
                has_allow = True
                break
        
        if not has_allow:
            return False
        
        # 检查是否被显式禁止
        for perm in role_perms:
            if perm.startswith('!'):
                denied_perm = perm[1:]  # 移除 ! 前缀
                if self._match_permission(denied_perm, action):
                    return False
        
        return True
    
    def _match_permission(self, pattern: str, action: str) -> bool:
        """匹配权限模式"""
        # 精确匹配
        if pattern == action:
            return True
        
        # 通配符匹配，如 "exec:*" 匹配所有 exec 操作
        if pattern.endswith('*'):
            prefix = pattern[:-1]
            return action.startswith(prefix)
        
        return False
    
    def get_allowed_actions(self, user_role: str) -> List[str]:
        """获取角色允许的所有操作"""
        return [p for p in self.permissions.get(user_role, []) 
                if not p.startswith('!')]
    
    def get_denied_actions(self, user_role: str) -> List[str]:
        """获取角色禁止的所有操作"""
        return [p[1:] for p in self.permissions.get(user_role, []) 
                if p.startswith('!')]

# 使用示例
if __name__ == '__main__':
    pm = PermissionManager()
    
    # 测试权限检查
    print(f"developer can exec:git: {pm.check_permission('developer', 'exec:git')}")
    print(f"developer can exec:sudo: {pm.check_permission('developer', 'exec:sudo')}")
    print(f"readonly can file:read: {pm.check_permission('readonly', 'file:read')}")
    print(f"readonly can exec:ls: {pm.check_permission('readonly', 'exec:ls')}")
```

### 1.2 工具级权限控制

#### 1.2.1 工具策略配置

```yaml
# ~/.openclaw/config/tool_policies.yaml
tools:
  exec:
    # 允许执行的命令白名单
    allowlist:
      - pattern: "^git\s+"
        description: "Git 命令"
      - pattern: "^docker\s+(ps|images|logs|exec)\s*"
        description: "Docker 只读命令"
      - pattern: "^kubectl\s+(get|describe|logs)\s*"
        description: "Kubectl 只读命令"
      - pattern: "^npm\s+(install|run|test)\s*"
        description: "NPM 命令"
      - pattern: "^python3?\s+"
        description: "Python 执行"
      - pattern: "^node\s+"
        description: "Node.js 执行"
      - pattern: "^ls\s*"
        description: "列出目录"
      - pattern: "^cat\s+"
        description: "查看文件"
      - pattern: "^grep\s+"
        description: "文本搜索"
    
    # 禁止执行的命令（优先级高于白名单）
    denylist:
      - pattern: "rm\s+-rf\s+/"
        severity: critical
        description: "删除根目录"
      - pattern: "dd\s+.*of=/dev/"
        severity: critical
        description: "直接磁盘写入"
      - pattern: "mkfs\."
        severity: critical
        description: "格式化文件系统"
      - pattern: ">\s*/dev/sd[a-z]"
        severity: critical
        description: "覆盖磁盘设备"
      - pattern: "curl\s+.*\|\s*sh"
        severity: high
        description: "管道执行远程脚本"
      - pattern: "wget\s+.*-O-\s*\|\s*sh"
        severity: high
        description: "管道执行远程脚本"
      - pattern: "eval\s*\$"
        severity: high
        description: "Eval 执行"
    
    # 需要确认的危险操作
    confirm_required:
      - pattern: "docker\s+(rm|stop|kill)\s+.*-f"
        description: "强制删除/停止容器"
        confirm_message: "确定要强制删除/停止容器吗？此操作不可恢复。"
      - pattern: "kubectl\s+delete\s+"
        description: "删除 K8s 资源"
        confirm_message: "确定要删除 Kubernetes 资源吗？"
      - pattern: "git\s+reset\s+--hard"
        description: "强制重置 Git"
        confirm_message: "确定要强制重置 Git 吗？未提交的更改将丢失。"
      - pattern: "git\s+clean\s+-fd"
        description: "清理 Git 未跟踪文件"
        confirm_message: "确定要删除所有未跟踪的文件吗？"
    
    # 资源限制
    limits:
      max_execution_time: 300  # 5分钟
      max_output_size: 10485760  # 10MB
      max_memory_mb: 1024
  
  browser:
    # 限制访问的域名
    allowed_domains:
      - "*.internal.company.com"
      - "github.com"
      - "stackoverflow.com"
      - "docs.python.org"
      - "developer.mozilla.org"
    
    # 禁止访问的域名
    blocked_domains:
      - "*.malicious.com"
      - "phishing-site.com"
      - "*. gambling.*"
      - "*.adult.*"
    
    # 允许的协议
    allowed_protocols:
      - "https"
    
    # 禁止的操作
    blocked_actions:
      - "file_upload"
      - "download_executable"
    
    # 会话限制
    session_limits:
      max_duration_minutes: 30
      max_pages_per_session: 10
  
  web_search:
    # 每日查询限制
    daily_quota: 1000
    
    # 速率限制
    rate_limit:
      requests_per_minute: 60
      requests_per_hour: 1000
    
    # 禁止的搜索关键词
    blocked_keywords:
      - "黑客工具"
      - "破解软件"
      - "盗版下载"
  
  kimi_search:
    # 每日查询限制
    daily_quota: 500
    
    # 速率限制
    rate_limit:
      requests_per_minute: 30
      requests_per_hour: 500
    
    # 内容过滤
    content_filter:
      enabled: true
      blocked_categories:
        - "adult"
        - "gambling"
        - "violence"
```

#### 1.2.2 命令验证器

```python
# lib/command_validator.py
import re
import yaml
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class ValidationResult(Enum):
    ALLOWED = "allowed"
    DENIED = "denied"
    CONFIRM_REQUIRED = "confirm_required"

@dataclass
class ValidationResponse:
    result: ValidationResult
    message: str
    severity: Optional[str] = None

class CommandValidator:
    """命令验证器"""
    
    def __init__(self, config_path: str = "~/.openclaw/config/tool_policies.yaml"):
        self.config_path = config_path
        self.policies = {}
        self._load_policies()
    
    def _load_policies(self):
        """加载策略配置"""
        import os
        expanded_path = os.path.expanduser(self.config_path)
        
        try:
            with open(expanded_path, 'r') as f:
                config = yaml.safe_load(f)
                self.policies = config.get('tools', {}).get('exec', {})
        except FileNotFoundError:
            self.policies = {}
    
    def validate(self, command: str) -> ValidationResponse:
        """
        验证命令是否允许执行
        
        Args:
            command: 要验证的命令
        
        Returns:
            ValidationResponse: 验证结果
        """
        # 1. 检查黑名单（最高优先级）
        denylist = self.policies.get('denylist', [])
        for item in denylist:
            pattern = item.get('pattern', '')
            if re.search(pattern, command, re.IGNORECASE):
                return ValidationResponse(
                    result=ValidationResult.DENIED,
                    message=f"命令被禁止: {item.get('description', '危险操作')}",
                    severity=item.get('severity', 'high')
                )
        
        # 2. 检查需要确认的操作
        confirm_list = self.policies.get('confirm_required', [])
        for item in confirm_list:
            pattern = item.get('pattern', '')
            if re.search(pattern, command, re.IGNORECASE):
                return ValidationResponse(
                    result=ValidationResult.CONFIRM_REQUIRED,
                    message=item.get('confirm_message', '此操作需要确认'),
                    severity='medium'
                )
        
        # 3. 检查白名单
        allowlist = self.policies.get('allowlist', [])
        if not allowlist:
            # 没有白名单则允许所有（已被黑名单过滤）
            return ValidationResponse(
                result=ValidationResult.ALLOWED,
                message="命令允许执行"
            )
        
        for item in allowlist:
            pattern = item.get('pattern', '')
            if re.search(pattern, command, re.IGNORECASE):
                return ValidationResponse(
                    result=ValidationResult.ALLOWED,
                    message=f"命令在白名单中: {item.get('description', '')}"
                )
        
        # 不在白名单中
        return ValidationResponse(
            result=ValidationResult.DENIED,
            message="命令不在允许列表中",
            severity='medium'
        )
    
    def sanitize_command(self, command: str) -> str:
        """
        清理命令中的危险字符
        
        Args:
            command: 原始命令
        
        Returns:
            str: 清理后的命令
        """
        # 移除 null 字节
        command = command.replace('\x00', '')
        
        # 移除控制字符
        command = ''.join(char for char in command if ord(char) >= 32 or char in '\n\r\t')
        
        # 限制命令长度
        max_length = 10000
        if len(command) > max_length:
            command = command[:max_length]
        
        return command.strip()
    
    def extract_command_info(self, command: str) -> Dict:
        """提取命令信息用于日志记录"""
        parts = command.split()
        return {
            'base_command': parts[0] if parts else '',
            'arguments': parts[1:] if len(parts) > 1 else [],
            'length': len(command),
            'has_pipe': '|' in command,
            'has_redirect': '>' in command or '<' in command,
            'has_sudo': 'sudo' in command.lower()
        }

# 使用示例
if __name__ == '__main__':
    validator = CommandValidator()
    
    test_commands = [
        "git status",
        "docker ps -a",
        "rm -rf /",
        "curl http://example.com | sh",
        "git reset --hard HEAD",
        "unknown_command"
    ]
    
    for cmd in test_commands:
        result = validator.validate(cmd)
        print(f"Command: {cmd}")
        print(f"  Result: {result.result.value}")
        print(f"  Message: {result.message}")
        if result.severity:
            print(f"  Severity: {result.severity}")
        print()
```

---

## 2. 敏感数据处理

### 2.1 密钥管理

#### 2.1.1 密钥管理系统

```bash
#!/bin/bash
# ~/.openclaw/scripts/secrets-manager.sh
# OpenClaw 密钥管理脚本

set -e

SECRETS_DIR="${HOME}/.openclaw/secrets"
KEY_FILE="${SECRETS_DIR}/.master.key"
CONFIG_FILE="${SECRETS_DIR}/.config"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

error() {
    echo -e "${RED}✗${NC} $1" >&2
}

success() {
    echo -e "${GREEN}✓${NC} $1"
}

# 初始化密钥存储
init() {
    log "初始化密钥存储..."
    
    # 创建目录
    mkdir -p "${SECRETS_DIR}"
    chmod 700 "${SECRETS_DIR}"
    
    # 生成主密钥
    if [[ ! -f "${KEY_FILE}" ]]; then
        openssl rand -base64 32 > "${KEY_FILE}"
        chmod 600 "${KEY_FILE}"
        success "主密钥已生成"
    else
        log "主密钥已存在"
    fi
    
    # 创建配置
    cat > "${CONFIG_FILE}" << EOF
# OpenClaw Secrets Configuration
ENCRYPTION_ALGORITHM=aes-256-cbc
KEY_DERIVATION=pbkdf2
ITERATIONS=100000
EOF
    chmod 600 "${CONFIG_FILE}"
    
    success "密钥存储初始化完成"
}

# 存储密钥
store() {
    local name="$1"
    local value="$2"
    
    if [[ -z "${name}" || -z "${value}" ]]; then
        error "用法: secrets-manager.sh store <name> <value>"
        return 1
    fi
    
    # 验证名称（只允许字母数字和下划线）
    if [[ ! "${name}" =~ ^[a-zA-Z0-9_]+$ ]]; then
        error "密钥名称只能包含字母、数字和下划线"
        return 1
    fi
    
    local secret_file="${SECRETS_DIR}/${name}.enc"
    
    # 加密存储
    echo "${value}" | openssl enc -aes-256-cbc -salt \
        -pass "file:${KEY_FILE}" \
        -out "${secret_file}" 2>/dev/null
    
    chmod 600 "${secret_file}"
    success "密钥 '${name}' 已存储"
}

# 读取密钥
get() {
    local name="$1"
    
    if [[ -z "${name}" ]]; then
        error "用法: secrets-manager.sh get <name>"
        return 1
    fi
    
    local secret_file="${SECRETS_DIR}/${name}.enc"
    
    if [[ ! -f "${secret_file}" ]]; then
        error "密钥 '${name}' 不存在"
        return 1
    fi
    
    openssl enc -aes-256-cbc -d \
        -pass "file:${KEY_FILE}" \
        -in "${secret_file}" 2>/dev/null
}

# 删除密钥
remove() {
    local name="$1"
    
    if [[ -z "${name}" ]]; then
        error "用法: secrets-manager.sh remove <name>"
        return 1
    fi
    
    local secret_file="${SECRETS_DIR}/${name}.enc"
    
    if [[ ! -f "${secret_file}" ]]; then
        error "密钥 '${name}' 不存在"
        return 1
    fi
    
    rm -f "${secret_file}"
    success "密钥 '${name}' 已删除"
}

# 列出所有密钥
list() {
    log "已存储的密钥:"
    
    for enc_file in "${SECRETS_DIR}"/*.enc; do
        if [[ -f "${enc_file}" ]]; then
            local name=$(basename "${enc_file}" .enc)
            local size=$(stat -f%z "${enc_file}" 2>/dev/null || stat -c%s "${enc_file}" 2>/dev/null)
            local modified=$(stat -f%Sm "${enc_file}" 2>/dev/null || stat -c%y "${enc_file}" 2>/dev/null)
            echo "  - ${name} (${size} bytes, ${modified})"
        fi
    done
}

# 环境变量注入
export_env() {
    local prefix="${1:-OPENCLAW_SECRET_}"
    
    log "导出密钥到环境变量..."
    
    for enc_file in "${SECRETS_DIR}"/*.enc; do
        [[ -f "${enc_file}" ]] || continue
        
        local name=$(basename "${enc_file}" .enc)
        local value=$(openssl enc -aes-256-cbc -d \
            -pass "file:${KEY_FILE}" \
            -in "${enc_file}" 2>/dev/null)
        
        export "${prefix}${name}=${value}"
        log "已导出: ${prefix}${name}"
    done
    
    success "环境变量导出完成"
}

# 轮换主密钥
rotate_key() {
    log "轮换主密钥..."
    
    local new_key_file="${SECRETS_DIR}/.master.key.new"
    local old_key_file="${KEY_FILE}.old"
    
    # 生成新密钥
    openssl rand -base64 32 > "${new_key_file}"
    chmod 600 "${new_key_file}"
    
    # 重新加密所有密钥
    for enc_file in "${SECRETS_DIR}"/*.enc; do
        [[ -f "${enc_file}" ]] || continue
        
        local name=$(basename "${enc_file}" .enc)
        log "重新加密: ${name}"
        
        # 解密
        local value=$(openssl enc -aes-256-cbc -d \
            -pass "file:${KEY_FILE}" \
            -in "${enc_file}" 2>/dev/null)
        
        # 用新密钥加密
        echo "${value}" | openssl enc -aes-256-cbc -salt \
            -pass "file:${new_key_file}" \
            -out "${enc_file}.tmp" 2>/dev/null
        
        mv "${enc_file}.tmp" "${enc_file}"
    done
    
    # 备份旧密钥，启用新密钥
    mv "${KEY_FILE}" "${old_key_file}"
    mv "${new_key_file}" "${KEY_FILE}"
    
    success "主密钥轮换完成，旧密钥备份为: ${old_key_file}"
}

# 主函数
main() {
    local cmd="${1:-help}"
    
    case "${cmd}" in
        init)
            init
            ;;
        store)
            store "$2" "$3"
            ;;
        get)
            get "$2"
            ;;
        remove|rm|delete)
            remove "$2"
            ;;
        list|ls)
            list
            ;;
        export)
            export_env "$2"
            ;;
        rotate)
            rotate_key
            ;;
        help|*)
            cat << EOF
OpenClaw 密钥管理器

用法:
  secrets-manager.sh init                    初始化密钥存储
  secrets-manager.sh store <name> <value>   存储密钥
  secrets-manager.sh get <name>             读取密钥
  secrets-manager.sh remove <name>          删除密钥
  secrets-manager.sh list                    列出所有密钥
  secrets-manager.sh export [prefix]         导出为环境变量
  secrets-manager.sh rotate                  轮换主密钥

示例:
  secrets-manager.sh store API_KEY "sk-123456"
  secrets-manager.sh get API_KEY
  secrets-manager.sh export MYAPP_
EOF
            ;;
    esac
}

main "$@"
```

#### 2.1.2 Python 密钥管理类

```python
# lib/secrets_manager.py
import os
import json
import base64
from pathlib import Path
from typing import Optional, Dict
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import hashlib

class SecretsManager:
    """
    OpenClaw 密钥管理器
    
    提供安全的密钥存储和检索功能
    """
    
    def __init__(self, secrets_dir: Optional[str] = None):
        if secrets_dir is None:
            secrets_dir = os.path.expanduser("~/.openclaw/secrets")
        
        self.secrets_dir = Path(secrets_dir)
        self.secrets_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        
        self.master_key_file = self.secrets_dir / ".master.key"
        self._master_key: Optional[bytes] = None
    
    def _get_or_create_master_key(self) -> bytes:
        """获取或创建主密钥"""
        if self._master_key is not None:
            return self._master_key
        
        if self.master_key_file.exists():
            with open(self.master_key_file, 'rb') as f:
                self._master_key = base64.urlsafe_b64decode(f.read().strip())
        else:
            # 生成新密钥
            key = Fernet.generate_key()
            with open(self.master_key_file, 'wb') as f:
                f.write(base64.urlsafe_b64encode(key))
            os.chmod(self.master_key_file, 0o600)
            self._master_key = key
        
        return self._master_key
    
    def _get_fernet(self) -> Fernet:
        """获取 Fernet 实例"""
        return Fernet(self._get_or_create_master_key())
    
    def store(self, name: str, value: str) -> None:
        """
        存储密钥
        
        Args:
            name: 密钥名称
            value: 密钥值
        """
        # 验证名称
        if not name.replace('_', '').isalnum():
            raise ValueError("密钥名称只能包含字母、数字和下划线")
        
        secret_file = self.secrets_dir / f"{name}.enc"
        
        fernet = self._get_fernet()
        encrypted = fernet.encrypt(value.encode())
        
        with open(secret_file, 'wb') as f:
            f.write(encrypted)
        os.chmod(secret_file, 0o600)
    
    def get(self, name: str) -> Optional[str]:
        """
        获取密钥
        
        Args:
            name: 密钥名称
        
        Returns:
            密钥值，如果不存在则返回 None
        """
        secret_file = self.secrets_dir / f"{name}.enc"
        
        if not secret_file.exists():
            return None
        
        fernet = self._get_fernet()
        
        with open(secret_file, 'rb') as f:
            encrypted = f.read()
        
        try:
            decrypted = fernet.decrypt(encrypted)
            return decrypted.decode()
        except Exception:
            return None
    
    def delete(self, name: str) -> bool:
        """
        删除密钥
        
        Args:
            name: 密钥名称
        
        Returns:
            是否成功删除
        """
        secret_file = self.secrets_dir / f"{name}.enc"
        
        if not secret_file.exists():
            return False
        
        secret_file.unlink()
        return True
    
    def list_secrets(self) -> Dict[str, Dict]:
        """
        列出所有密钥
        
        Returns:
            密钥信息字典
        """
        secrets = {}
        
        for enc_file in self.secrets_dir.glob("*.enc"):
            name = enc_file.stem
            stat = enc_file.stat()
            secrets[name] = {
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'path': str(enc_file)
            }
        
        return secrets
    
    def export_to_env(self, prefix: str = "OPENCLAW_SECRET_") -> Dict[str, str]:
        """
        导出所有密钥到环境变量
        
        Args:
            prefix: 环境变量前缀
        
        Returns:
            导出的环境变量字典
        """
        exported = {}
        
        for name in self.list_secrets().keys():
            value = self.get(name)
            if value is not None:
                env_name = f"{prefix}{name}"
                os.environ[env_name] = value
                exported[env_name] = value
        
        return exported
    
    def rotate_master_key(self) -> None:
        """轮换主密钥"""
        # 读取所有现有密钥
        secrets_data = {}
        for name in self.list_secrets().keys():
            value = self.get(name)
            if value is not None:
                secrets_data[name] = value
        
        # 备份旧密钥
        old_key_file = self.secrets_dir / ".master.key.old"
        self.master_key_file.rename(old_key_file)
        
        # 重置主密钥
        self._master_key = None
        
        # 重新加密所有密钥
        for name, value in secrets_data.items():
            self.store(name, value)

# 使用示例
if __name__ == '__main__':
    sm = SecretsManager()
    
    # 存储密钥
    sm.store("API_KEY", "sk-1234567890abcdef")
    sm.store("DB_PASSWORD", "mysecretpassword")
    
    # 读取密钥
    api_key = sm.get("API_KEY")
    print(f"API_KEY: {api_key}")
    
    # 列出所有密钥
    print("\n所有密钥:")
    for name, info in sm.list_secrets().items():
        print(f"  - {name}: {info['size']} bytes")
    
    # 导出到环境变量
    env_vars = sm.export_to_env()
    print("\n导出的环境变量:")
    for name in env_vars.keys():
        print(f"  - {name}")
```

### 2.2 日志脱敏

#### 2.2.1 日志脱敏处理器

```python
# lib/log_sanitizer.py
import re
import json
import hashlib
from typing import Pattern, List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class SanitizationRule:
    """脱敏规则"""
    name: str
    pattern: Pattern
    replacement: str
    description: str

class LogSanitizer:
    """
    日志脱敏处理器
    
    自动识别并脱敏日志中的敏感信息
    """
    
    # 预定义的脱敏规则
    DEFAULT_RULES: List[SanitizationRule] = [
        # API Keys
        SanitizationRule(
            name="api_key",
            pattern=re.compile(r'(api[_-]?key\s*[=:]\s*)["\']?[a-zA-Z0-9]{32,}["\']?', re.IGNORECASE),
            replacement=r'\1***API_KEY_REDACTED***',
            description="API密钥"
        ),
        # Secret Keys
        SanitizationRule(
            name="secret_key",
            pattern=re.compile(r'(secret[_-]?key\s*[=:]\s*)["\']?[a-zA-Z0-9]{32,}["\']?', re.IGNORECASE),
            replacement=r'\1***SECRET_KEY_REDACTED***',
            description="Secret密钥"
        ),
        # 密码
        SanitizationRule(
            name="password",
            pattern=re.compile(r'(password\s*[=:]\s*)["\']?[^"\'\s]+["\']?', re.IGNORECASE),
            replacement=r'\1***PASSWORD_REDACTED***',
            description="密码"
        ),
        # Bearer Token
        SanitizationRule(
            name="bearer_token",
            pattern=re.compile(r'(Bearer\s+)[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+', re.IGNORECASE),
            replacement=r'\1***TOKEN_REDACTED***',
            description="Bearer Token"
        ),
        # JWT Token
        SanitizationRule(
            name="jwt_token",
            pattern=re.compile(r'["\']?[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+["\']?'),
            replacement=r'***JWT_TOKEN_REDACTED***',
            description="JWT Token"
        ),
        # 邮箱地址
        SanitizationRule(
            name="email",
            pattern=re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            replacement=r'***EMAIL_REDACTED***',
            description="邮箱地址"
        ),
        # IP地址
        SanitizationRule(
            name="ip_address",
            pattern=re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'),
            replacement=r'***IP_REDACTED***',
            description="IP地址"
        ),
        # 手机号（中国大陆）
        SanitizationRule(
            name="phone_cn",
            pattern=re.compile(r'\b1[3-9]\d{9}\b'),
            replacement=r'***PHONE_REDACTED***',
            description="手机号"
        ),
        # 身份证号（中国大陆）
        SanitizationRule(
            name="id_card_cn",
            pattern=re.compile(r'\b\d{17}[\dXx]|\d{15}\b'),
            replacement=r'***ID_CARD_REDACTED***',
            description="身份证号"
        ),
        # 银行卡号
        SanitizationRule(
            name="bank_card",
            pattern=re.compile(r'\b\d{16,19}\b'),
            replacement=r'***BANK_CARD_REDACTED***',
            description="银行卡号"
        ),
        # 信用卡号（简单匹配）
        SanitizationRule(
            name="credit_card",
            pattern=re.compile(r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})\b'),
            replacement=r'***CREDIT_CARD_REDACTED***',
            description="信用卡号"
        ),
        # AWS Access Key
        SanitizationRule(
            name="aws_access_key",
            pattern=re.compile(r'AKIA[0-9A-Z]{16}'),
            replacement=r'***AWS_KEY_REDACTED***',
            description="AWS Access Key"
        ),
        # AWS Secret Key
        SanitizationRule(
            name="aws_secret_key",
            pattern=re.compile(r'["\']?[A-Za-z0-9/+=]{40}["\']?'),
            replacement=r'***AWS_SECRET_REDACTED***',
            description="AWS Secret Key"
        ),
        # GitHub Token
        SanitizationRule(
            name="github_token",
            pattern=re.compile(r'gh[pousr]_[A-Za-z0-9_]{36,}'),
            replacement=r'***GITHUB_TOKEN_REDACTED***',
            description="GitHub Token"
        ),
        # Slack Token
        SanitizationRule(
            name="slack_token",
            pattern=re.compile(r'xox[baprs]-[0-9a-zA-Z]{10,48}'),
            replacement=r'***SLACK_TOKEN_REDACTED***',
            description="Slack Token"
        ),
        # Private Key
        SanitizationRule(
            name="private_key",
            pattern=re.compile(r'-----BEGIN (?:RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----[\s\S]*?-----END (?:RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----'),
            replacement=r'***PRIVATE_KEY_REDACTED***',
            description="私钥"
        ),
    ]
    
    def __init__(self, custom_rules: Optional[List[SanitizationRule]] = None):
        """
        初始化脱敏处理器
        
        Args:
            custom_rules: 自定义脱敏规则
        """
        self.rules = self.DEFAULT_RULES.copy()
        if custom_rules:
            self.rules.extend(custom_rules)
    
    def sanitize(self, text: str) -> str:
        """
        对文本进行脱敏处理
        
        Args:
            text: 原始文本
        
        Returns:
            脱敏后的文本
        """
        result = text
        for rule in self.rules:
            result = rule.pattern.sub(rule.replacement, result)
        return result
    
    def sanitize_dict(
        self,
        data: Dict[str, Any],
        sensitive_keys: Optional[List[str]] = None,
        max_depth: int = 10
    ) -> Dict[str, Any]:
        """
        对字典中的敏感字段进行脱敏
        
        Args:
            data: 原始字典
            sensitive_keys: 敏感字段名列表
            max_depth: 最大递归深度
        
        Returns:
            脱敏后的字典
        """
        if sensitive_keys is None:
            sensitive_keys = [
                'password', 'token', 'secret', 'key', 'api_key',
                'private_key', 'access_token', 'refresh_token',
                'authorization', 'cookie', 'session'
            ]
        
        return self._sanitize_dict_recursive(data, sensitive_keys, 0, max_depth)
    
    def _sanitize_dict_recursive(
        self,
        data: Any,
        sensitive_keys: List[str],
        current_depth: int,
        max_depth: int
    ) -> Any:
        """递归脱敏字典"""
        if current_depth >= max_depth:
            return data
        
        if isinstance(data, dict):
            result = {}
            for key, value in data.items():
                # 检查键名是否敏感
                if any(sk.lower() in key.lower() for sk in sensitive_keys):
                    if isinstance(value, str):
                        result[key] = '***REDACTED***'
                    else:
                        result[key] = '***REDACTED***'
                elif isinstance(value, (dict, list)):
                    result[key] = self._sanitize_dict_recursive(
                        value, sensitive_keys, current_depth + 1, max_depth
                    )
                elif isinstance(value, str):
                    result[key] = self.sanitize(value)
                else:
                    result[key] = value
            return result
        
        elif isinstance(data, list):
            return [
                self._sanitize_dict_recursive(item, sensitive_keys, current_depth + 1, max_depth)
                for item in data
            ]
        
        elif isinstance(data, str):
            return self.sanitize(data)
        
        return data
    
    def hash_sensitive(self, text: str, salt: Optional[str] = None) -> str:
        """
        对敏感信息进行哈希处理（用于需要保留唯一性的场景）
        
        Args:
            text: 原始文本
            salt: 盐值
        
        Returns:
            哈希值
        """
        if salt:
            text = f"{salt}:{text}"
        return hashlib.sha256(text.encode()).hexdigest()[:16]
    
    def add_custom_rule(self, rule: SanitizationRule) -> None:
        """添加自定义脱敏规则"""
        self.rules.append(rule)
    
    def get_rules_info(self) -> List[Dict[str, str]]:
        """获取所有规则信息"""
        return [
            {
                'name': rule.name,
                'description': rule.description,
                'pattern': rule.pattern.pattern[:50] + '...' if len(rule.pattern.pattern) > 50 else rule.pattern.pattern
            }
            for rule in self.rules
        ]

# 日志处理器集成
import logging

class SanitizingLogHandler(logging.Handler):
    """自动脱敏的日志处理器"""
    
    def __init__(self, base_handler: logging.Handler, sanitizer: Optional[LogSanitizer] = None):
        super().__init__()
        self.base_handler = base_handler
        self.sanitizer = sanitizer or LogSanitizer()
    
    def emit(self, record: logging.LogRecord) -> None:
        """处理日志记录"""
        # 脱敏消息
        if isinstance(record.msg, str):
            record.msg = self.sanitizer.sanitize(record.msg)
        
        # 脱敏参数
        if record.args:
            record.args = tuple(
                self.sanitizer.sanitize(str(arg)) if isinstance(arg, str) else arg
                for arg in record.args
            )
        
        # 脱敏额外字段
        if hasattr(record, 'extra'):
            record.extra = self.sanitizer.sanitize_dict(record.extra)
        
        self.base_handler.emit(record)

# 使用示例
if __name__ == '__main__':
    sanitizer = LogSanitizer()
    
    # 测试文本脱敏
    test_texts = [
        "API Key: sk-1234567890abcdef1234567890abcdef",
        "Email: user@example.com contacted support",
        "IP: 192.168.1.1 accessed the server",
        "Phone: 13800138000 called",
        "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    ]
    
    print("文本脱敏测试:")
    for text in test_texts:
        sanitized = sanitizer.sanitize(text)
        print(f"  原始: {text}")
        print(f"  脱敏: {sanitized}")
        print()
    
    # 测试字典脱敏
    test_dict = {
        'username': 'john_doe',
        'password': 'super_secret_123',
        'api_key': 'sk-abc123',
        'email': 'john@example.com',
        'nested': {
            'secret_token': 'xyz789',
            'normal_field': 'visible'
        }
    }
    
    print("字典脱敏测试:")
    print(f"  原始: {json.dumps(test_dict, indent=2)}")
    sanitized_dict = sanitizer.sanitize_dict(test_dict)
    print(f"  脱敏: {json.dumps(sanitized_dict, indent=2)}")
```

---

## 3. 沙箱配置

### 3.1 容器化沙箱

#### 3.1.1 Docker Compose 配置

```yaml
# ~/.openclaw/docker/sandbox-compose.yaml
version: '3.8'

services:
  openclaw-sandbox:
    image: openclaw/sandbox:latest
    container_name: openclaw-sandbox
    hostname: openclaw-sandbox
    
    # 重启策略
    restart: unless-stopped
    
    # 资源限制
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
          pids: 1000
        reservations:
          cpus: '0.5'
          memory: 512M
    
    # 安全选项
    security_opt:
      - no-new-privileges:true
      - seccomp:./seccomp-profile.json
      - apparmor:docker-default
    
    # 只读根文件系统
    read_only: true
    
    # 临时文件系统
    tmpfs:
      - /tmp:noexec,nosuid,size=100m,uid=1000,gid=1000
      - /var/tmp:noexec,nosuid,size=100m,uid=1000,gid=1000
      - /run:noexec,nosuid,size=10m,uid=1000,gid=1000
    
    # 能力限制
    cap_drop:
      - ALL
    cap_add:
      - CHOWN
      - SETGID
      - SETUID
      - DAC_OVERRIDE
    
    # 用户配置
    user: "1000:1000"
    
    # 网络隔离
    network_mode: bridge
    networks:
      - sandbox-net
    
    # DNS配置
    dns:
      - 8.8.8.8
      - 8.8.4.4
    dns_search:
      - example.com
    
    # 环境变量
    environment:
      - OPENCLAW_ENV=sandbox
      - OPENCLAW_USER=1000
      - HOME=/workspace
      - TMPDIR=/tmp
    
    # 挂载点
    volumes:
      # 工作目录（可写）
      - type: bind
        source: ${WORKSPACE_DIR:-~/.openclaw/workspace}
        target: /workspace
        read_only: false
      
      # 日志目录（可写）
      - type: bind
        source: ${LOGS_DIR:-~/.openclaw/logs}
        target: /logs
        read_only: false
      
      # 配置文件（只读）
      - type: bind
        source: ${CONFIG_DIR:-~/.openclaw/config}
        target: /config
        read_only: true
      
      # 阻止访问敏感文件
      - type: bind
        source: /dev/null
        target: /proc/kcore
        read_only: true
      - type: bind
        source: /dev/null
        target: /proc/sched_debug
        read_only: true
    
    # 健康检查
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    
    # 日志配置
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
        labels: "service,environment"
        env: "OPENCLAW_ENV"

networks:
  sandbox-net:
    driver: bridge
    internal: false
    ipam:
      config:
        - subnet: 172.28.0.0/16
```

#### 3.1.2 Seccomp 安全配置文件

```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": [
    "SCMP_ARCH_X86_64",
    "SCMP_ARCH_X86",
    "SCMP_ARCH_AARCH64"
  ],
  "syscalls": [
    {
      "names": [
        "accept",
        "accept4",
        "access",
        "adjtimex",
        "alarm",
        "bind",
        "brk",
        "capget",
        "capset",
        "chdir",
        "chmod",
        "chown",
        "chown32",
        "clock_adjtime",
        "clock_getres",
        "clock_gettime",
        "clock_nanosleep",
        "clone",
        "clone3",
        "close",
        "close_range",
        "connect",
        "copy_file_range",
        "creat",
        "dup",
        "dup2",
        "dup3",
        "epoll_create",
        "epoll_create1",
        "epoll_ctl",
        "epoll_ctl_old",
        "epoll_pwait",
        "epoll_pwait2",
        "epoll_wait",
        "epoll_wait_old",
        "eventfd",
        "eventfd2",
        "execve",
        "execveat",
        "exit",
        "exit_group",
        "faccessat",
        "faccessat2",
        "fadvise64",
        "fadvise64_64",
        "fallocate",
        "fanotify_mark",
        "fchdir",
        "fchmod",
        "fchmodat",
        "fchmodat2",
        "fchown",
        "fchown32",
        "fchownat",
        "fcntl",
        "fcntl64",
        "fdatasync",
        "fgetxattr",
        "flistxattr",
        "flock",
        "fork",
        "fremovexattr",
        "fsetxattr",
        "fstat",
        "fstat64",
        "fstatat64",
        "fstatfs",
        "fstatfs64",
        "fsync",
        "ftruncate",
        "ftruncate64",
        "futex",
        "futex_waitv",
        "getcpu",
        "getcwd",
        "getdents",
        "getdents64",
        "getegid",
        "getegid32",
        "geteuid",
        "geteuid32",
        "getgid",
        "getgid32",
        "getgroups",
        "getgroups32",
        "getitimer",
        "getpeername",
        "getpgid",
        "getpgrp",
        "getpid",
        "getppid",
        "getpriority",
        "getrandom",
        "getresgid",
        "getresgid32",
        "getresuid",
        "getresuid32",
        "getrlimit",
        "get_robust_list",
        "getrusage",
        "getsid",
        "getsockname",
        "getsockopt",
        "get_thread_area",
        "gettid",
        "gettimeofday",
        "getuid",
        "getuid32",
        "getxattr",
        "inotify_add_watch",
        "inotify_init",
        "inotify_init1",
        "inotify_rm_watch",
        "io_cancel",
        "ioctl",
        "io_destroy",
        "io_getevents",
        "io_pgetevents",
        "io_pgetevents_time64",
        "ioprio_get",
        "ioprio_set",
        "io_setup",
        "io_submit",
        "io_uring_enter",
        "io_uring_register",
        "io_uring_setup",
        "kill",
        "lchown",
        "lchown32",
        "lgetxattr",
        "link",
        "linkat",
        "listen",
        "listxattr",
        "llistxattr",
        "lremovexattr",
        "lseek",
        "lsetxattr",
        "lstat",
        "lstat64",
        "madvise",
        "membarrier",
        "memfd_create",
        "memfd_secret",
        "mincore",
        "mkdir",
        "mkdirat",
        "mknod",
        "mknodat",
        "mlock",
        "mlock2",
        "mlockall",
        "mmap",
        "mmap2",
        "mprotect",
        "mq_getsetattr",
        "mq_notify",
        "mq_open",
        "mq_timedreceive",
        "mq_timedreceive_time64",
        "mq_timedsend",
        "mq_timedsend_time64",
        "mq_unlink",
        "mremap",
        "msgctl",
        "msgget",
        "msgrcv",
        "msgsnd",
        "msync",
        "munlock",
        "munlockall",
        "munmap",
        "nanosleep",
        "newfstatat",
        "open",
        "openat",
        "openat2",
        "pause",
        "pidfd_open",
        "pidfd_send_signal",
        "pipe",
        "pipe2",
        "poll",
        "ppoll",
        "ppoll_time64",
        "prctl",
        "pread64",
        "preadv",
        "preadv2",
        "prlimit64",
        "pselect6",
        "pselect6_time64",
        "pwrite64",
        "pwritev",
        "pwritev2",
        "read",
        "readahead",
        "readdir",
        "readlink",
        "readlinkat",
        "readv",
        "recv",
        "recvfrom",
        "recvmmsg",
        "recvmmsg_time64",
        "recvmsg",
        "remap_file_pages",
        "removexattr",
        "rename",
        "renameat",
        "renameat2",
        "restart_syscall",
        "rmdir",
        "rseq",
        "rt_sigaction",
        "rt_sigpending",
        "rt_sigprocmask",
        "rt_sigqueueinfo",
        "rt_sigreturn",
        "rt_sigsuspend",
        "rt_sigtimedwait",
        "rt_sigtimedwait_time64",
        "rt_tgsigqueueinfo",
        "sched_getaffinity",
        "sched_getattr",
        "sched_getparam",
        "sched_get_priority_max",
        "sched_get_priority_min",
        "sched_getscheduler",
        "sched_rr_get_interval",
        "sched_rr_get_interval_time64",
        "sched_setaffinity",
        "sched_setattr",
        "sched_setparam",
        "sched_setscheduler",
        "sched_yield",
        "seccomp",
        "select",
        "semctl",
        "semget",
        "semop",
        "semtimedop",
        "semtimedop_time64",
        "send",
        "sendfile",
        "sendfile64",
        "sendmmsg",
        "sendmsg",
        "sendto",
        "setfsgid",
        "setfsgid32",
        "setfsuid",
        "setfsuid32",
        "setgid",
        "setgid32",
        "setgroups",
        "setgroups32",
        "setitimer",
        "setpgid",
        "setpriority",
        "setregid",
        "setregid32",
        "setresgid",
        "setresgid32",
        "setresuid",
        "setresuid32",
        "setreuid",
        "setreuid32",
        "setrlimit",
        "set_robust_list",
        "setsid",
        "setsockopt",
        "set_thread_area",
        "set_tid_address",
        "setuid",
        "setuid32",
        "setxattr",
        "shmat",
        "shmctl",
        "shmdt",
        "shmget",
        "shutdown",
        "sigaltstack",
        "signalfd",
        "signalfd4",
        "sigpending",
        "sigprocmask",
        "sigreturn",
        "socket",
        "socketcall",
        "socketpair",
        "splice",
        "stat",
        "stat64",
        "statfs",
        "statfs64",
        "statx",
        "symlink",
        "symlinkat",
        "sync",
        "sync_file_range",
        "syncfs",
        "sysinfo",
        "tee",
        "tgkill",
        "time",
        "timer_create",
        "timer_delete",
        "timerfd_create",
        "timerfd_gettime",
        "timerfd_gettime64",
        "timerfd_settime",
        "timerfd_settime64",
        "timer_getoverrun",
        "timer_gettime",
        "timer_gettime64",
        "timer_settime",
        "timer_settime64",
        "times",
        "tkill",
        "truncate",
        "truncate64",
        "ugetrlimit",
        "umask",
        "uname",
        "unlink",
        "unlinkat",
        "utime",
        "utimensat",
        "utimensat_time64",
        "utimes",
        "vfork",
        "wait4",
        "waitid",
        "waitpid",
        "write",
        "writev"
      ],
      "action": "SCMP_ACT_ALLOW"
    },
    {
      "names": [
        "bpf",
        "clone",
        "fanotify_init",
        "lookup_dcookie",
        "mount",
        "nfsservctl",
        "open_by_handle_at",
        "perf_event_open",
        "personality",
        "pivot_root",
        "ptrace",
        "reboot",
        "setns",
        "swapoff",
        "swapon",
        "syslog",
        "umount2",
        "unshare",
        "uselib",
        "userfaultfd",
        "vm86",
        "vm86old"
      ],
      "action": "SCMP_ACT_ERRNO"
    }
  ]
}
```

### 3.2 运行时沙箱

#### 3.2.1 沙箱管理脚本

```bash
#!/bin/bash
# ~/.openclaw/scripts/sandbox-manager.sh
# OpenClaw 沙箱管理脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="${HOME}/.openclaw/docker/sandbox-compose.yaml"
SANDBOX_NAME="openclaw-sandbox"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}✗${NC} $1" >&2
}

success() {
    echo -e "${GREEN}✓${NC} $1"
}

warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# 检查 Docker 是否安装
check_docker() {
    if ! command -v docker &> /dev/null; then
        error "Docker 未安装"
        exit 1
    fi
    
    if ! docker info > /dev/null 2>&1; then
        error "Docker 守护进程未运行"
        exit 1
    fi
    
    success "Docker 检查通过"
}

# 创建必要的目录
setup_directories() {
    log "设置目录..."
    
    mkdir -p "${HOME}/.openclaw"/{workspace,logs,config,docker}
    mkdir -p "${HOME}/.openclaw/sandbox"/{tmp,cache}
    
    # 设置权限
    chmod 700 "${HOME}/.openclaw"
    chmod 700 "${HOME}/.openclaw/sandbox"
    
    success "目录设置完成"
}

# 启动沙箱
start() {
    log "启动沙箱..."
    
    check_docker
    setup_directories
    
    if [[ ! -f "${COMPOSE_FILE}" ]]; then
        error "Docker Compose 文件不存在: ${COMPOSE_FILE}"
        exit 1
    fi
    
    # 设置环境变量
    export WORKSPACE_DIR="${HOME}/.openclaw/workspace"
    export LOGS_DIR="${HOME}/.openclaw/logs"
    export CONFIG_DIR="${HOME}/.openclaw/config"
    
    # 启动容器
    docker-compose -f "${COMPOSE_FILE}" up -d
    
    # 等待服务就绪
    log "等待沙箱就绪..."
    sleep 5
    
    if docker ps | grep -q "${SANDBOX_NAME}"; then
        success "沙箱启动成功"
        status
    else
        error "沙箱启动失败"
        logs
        exit 1
    fi
}

# 停止沙箱
stop() {
    log "停止沙箱..."
    
    if docker ps | grep -q "${SANDBOX_NAME}"; then
        docker-compose -f "${COMPOSE_FILE}" down
        success "沙箱已停止"
    else
        warn "沙箱未运行"
    fi
}

# 重启沙箱
restart() {
    log "重启沙箱..."
    stop
    sleep 2
    start
}

# 查看状态
status() {
    log "沙箱状态:"
    
    if docker ps | grep -q "${SANDBOX_NAME}"; then
        echo "  状态: 运行中"
        echo "  容器 ID: $(docker ps -q -f name="${SANDBOX_NAME}")"
        echo "  运行时间: $(docker ps -f name="${SANDBOX_NAME}" --format "{{.RunningFor}}")"
        echo "  端口映射:"
        docker port "${SANDBOX_NAME}" 2>/dev/null | sed 's/^/    /' || echo "    无"
        
        # 资源使用
        echo "  资源使用:"
        docker stats --no-stream "${SANDBOX_NAME}" --format \
            "    CPU: {{.CPUPerc}} | 内存: {{.MemUsage}} | 网络: {{.NetIO}}" 2>/dev/null || true
    else
        echo "  状态: 未运行"
    fi
}

# 查看日志
logs() {
    log "沙箱日志:"
    docker logs --tail 100 -f "${SANDBOX_NAME}" 2>/dev/null || error "无法获取日志"
}

# 进入沙箱
shell() {
    log "进入沙箱..."
    docker exec -it "${SANDBOX_NAME}" /bin/sh
}

# 执行命令
exec_cmd() {
    local cmd="$1"
    log "在沙箱中执行: ${cmd}"
    docker exec "${SANDBOX_NAME}" ${cmd}
}

# 清理资源
cleanup() {
    log "清理沙箱资源..."
    
    # 停止并删除容器
    docker-compose -f "${COMPOSE_FILE}" down -v 2>/dev/null || true
    
    # 删除镜像
    docker rmi "openclaw/sandbox:latest" 2>/dev/null || true
    
    # 清理临时文件
    rm -rf "${HOME}/.openclaw/sandbox/tmp/*"
    
    success "清理完成"
}

# 安全扫描
scan() {
    log "运行安全扫描..."
    
    if ! docker ps | grep -q "${SANDBOX_NAME}"; then
        error "沙箱未运行"
        exit 1
    fi
    
    echo "  容器配置:"
    docker inspect "${SANDBOX_NAME}" --format '
    - 只读根文件系统: {{.HostConfig.ReadonlyRootfs}}
    - 特权模式: {{.HostConfig.Privileged}}
    - 用户: {{.Config.User}}
    - 能力: {{.HostConfig.CapAdd}}
    - 安全选项: {{.HostConfig.SecurityOpt}}
    '
    
    echo "  网络隔离:"
    docker inspect "${SANDBOX_NAME}" --format '{{range .NetworkSettings.Networks}}    - {{.IPAddress}}{{end}}'
    
    echo "  挂载点:"
    docker inspect "${SANDBOX_NAME}" --format '{{range .Mounts}}    - {{.Source}} -> {{.Destination}} ({{.Mode}}){{println}}{{end}}'
}

# 主函数
main() {
    local cmd="${1:-help}"
    shift || true
    
    case "${cmd}" in
        start)
            start
            ;;
        stop)
            stop
            ;;
        restart)
            restart
            ;;
        status)
            status
            ;;
        logs)
            logs
            ;;
        shell|sh|bash)
            shell
            ;;
        exec)
            exec_cmd "$@"
            ;;
        cleanup)
            cleanup
            ;;
        scan)
            scan
            ;;
        help|*)
            cat << EOF
OpenClaw 沙箱管理器

用法:
  sandbox-manager.sh start              启动沙箱
  sandbox-manager.sh stop               停止沙箱
  sandbox-manager.sh restart            重启沙箱
  sandbox-manager.sh status             查看状态
  sandbox-manager.sh logs               查看日志
  sandbox-manager.sh shell              进入沙箱 Shell
  sandbox-manager.sh exec <command>    在沙箱中执行命令
  sandbox-manager.sh scan               运行安全扫描
  sandbox-manager.sh cleanup            清理所有资源

示例:
  sandbox-manager.sh start
  sandbox-manager.sh exec "ls -la /workspace"
  sandbox-manager.sh shell
EOF
            ;;
    esac
}

main "$@"
```

---

## 4. 审计日志

### 4.1 审计配置

```yaml
# ~/.openclaw/config/audit.yaml
audit:
  # 启用审计日志
  enabled: true
  
  # 审计级别: basic, detailed, full
  level: detailed
  
  # 日志输出
  output:
    type: file  # file, stdout, syslog, webhook
    file:
      path: "~/.openclaw/logs/audit.log"
      max_size: 100MB
      max_files: 30
      rotate_daily: true
    
    webhook:
      url: "https://security.company.com/audit"
      headers:
        Authorization: "Bearer ${AUDIT_WEBHOOK_TOKEN}"
      timeout: 30
      retry_count: 3
  
  # 审计事件类型
  events:
    # 认证事件
    auth:
      - login
      - logout
      - token_refresh
      - permission_denied
    
    # 文件操作
    file:
      - read
      - write
      - delete
      - execute
      - permission_change
    
    # 命令执行
    exec:
      - command_start
      - command_complete
      - command_failed
      - command_blocked
    
    # 网络操作
    network:
      - http_request
      - web_search
      - browser_action
      - connection_open
      - connection_close
    
    # 配置变更
    config:
      - load
      - reload
      - change
    
    # 系统事件
    system:
      - startup
      - shutdown
      - error
      - security_alert
  
  # 敏感字段过滤
  sensitive_fields:
    - password
    - token
    - secret
    - api_key
    - private_key
    - credit_card
    - ssn
  
  # 保留策略
  retention:
    days: 90
    archive_after_days: 30
    archive_location: "~/.openclaw/audit/archive"
```

### 4.2 审计日志处理器

```python
# lib/audit_logger.py
import json
import hashlib
import hmac
from datetime import datetime
from typing import Dict, Any, Optional, List
from enum import Enum
from dataclasses import dataclass, asdict
import logging
import requests

class AuditEventType(Enum):
    """审计事件类型"""
    AUTH_LOGIN = "auth.login"
    AUTH_LOGOUT = "auth.logout"
    AUTH_DENIED = "auth.denied"
    FILE_READ = "file.read"
    FILE_WRITE = "file.write"
    FILE_DELETE = "file.delete"
    FILE_EXECUTE = "file.execute"
    EXEC_START = "exec.start"
    EXEC_COMPLETE = "exec.complete"
    EXEC_FAILED = "exec.failed"
    EXEC_BLOCKED = "exec.blocked"
    NETWORK_REQUEST = "network.request"
    NETWORK_RESPONSE = "network.response"
    CONFIG_CHANGE = "config.change"
    SYSTEM_STARTUP = "system.startup"
    SYSTEM_SHUTDOWN = "system.shutdown"
    SECURITY_ALERT = "security.alert"

class AuditLevel(Enum):
    """审计级别"""
    BASIC = "basic"
    DETAILED = "detailed"
    FULL = "full"

@dataclass
class AuditEvent:
    """审计事件"""
    timestamp: str
    event_type: str
    event_id: str
    user_id: Optional[str]
    session_id: Optional[str]
    source_ip: Optional[str]
    resource: Optional[str]
    action: str
    status: str
    details: Dict[str, Any]
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=str)

class AuditLogger:
    """
    审计日志记录器
    
    记录所有关键操作和事件，用于安全审计和合规性检查
    """
    
    def __init__(self, config_path: str = "~/.openclaw/config/audit.yaml"):
        import yaml
        import os
        
        self.config_path = os.path.expanduser(config_path)
        self.config = self._load_config()
        
        # 初始化日志处理器
        self.logger = logging.getLogger("openclaw.audit")
        self.logger.setLevel(logging.INFO)
        
        # 添加文件处理器
        if self.config.get('output', {}).get('type') == 'file':
            self._setup_file_handler()
    
    def _load_config(self) -> Dict:
        """加载配置"""
        import yaml
        
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f).get('audit', {})
        except FileNotFoundError:
            return {'enabled': True, 'level': 'basic'}
    
    def _setup_file_handler(self):
        """设置文件日志处理器"""
        from logging.handlers import RotatingFileHandler
        
        file_config = self.config.get('output', {}).get('file', {})
        log_path = file_config.get('path', '~/.openclaw/logs/audit.log')
        log_path = os.path.expanduser(log_path)
        
        # 确保目录存在
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        
        handler = RotatingFileHandler(
            log_path,
            maxBytes=self._parse_size(file_config.get('max_size', '100MB')),
            backupCount=file_config.get('max_files', 30)
        )
        
        formatter = logging.Formatter(
            '%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def _parse_size(self, size_str: str) -> int:
        """解析大小字符串"""
        size_str = size_str.upper()
        multipliers = {'B': 1, 'KB': 1024, 'MB': 1024**2, 'GB': 1024**3}
        
        for suffix, multiplier in multipliers.items():
            if size_str.endswith(suffix):
                return int(size_str[:-len(suffix)]) * multiplier
        
        return int(size_str)
    
    def _sanitize_details(self, details: Dict[str, Any]) -> Dict[str, Any]:
        """脱敏敏感字段"""
        sensitive_fields = self.config.get('sensitive_fields', [])
        sanitized = {}
        
        for key, value in details.items():
            if any(sf.lower() in key.lower() for sf in sensitive_fields):
                if isinstance(value, str):
                    # 哈希处理敏感值
                    sanitized[key] = hashlib.sha256(value.encode()).hexdigest()[:16]
                else:
                    sanitized[key] = '***REDACTED***'
            elif isinstance(value, dict):
                sanitized[key] = self._sanitize_details(value)
            else:
                sanitized[key] = value
        
        return sanitized
    
    def _generate_event_id(self) -> str:
        """生成事件ID"""
        import uuid
        return str(uuid.uuid4())
    
    def log(
        self,
        event_type: AuditEventType,
        action: str,
        status: str,
        details: Dict[str, Any] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        resource: Optional[str] = None
    ) -> AuditEvent:
        """
        记录审计事件
        
        Args:
            event_type: 事件类型
            action: 操作描述
            status: 状态 (success, failed, blocked)
            details: 详细信息
            user_id: 用户ID
            session_id: 会话ID
            resource: 资源标识
        
        Returns:
            AuditEvent: 审计事件对象
        """
        if not self.config.get('enabled', True):
            return None
        
        # 脱敏处理
        if details:
            details = self._sanitize_details(details)
        else:
            details = {}
        
        # 创建事件
        event = AuditEvent(
            timestamp=datetime.utcnow().isoformat() + 'Z',
            event_type=event_type.value,
            event_id=self._generate_event_id(),
            user_id=user_id,
            session_id=session_id,
            source_ip=self._get_source_ip(),
            resource=resource,
            action=action,
            status=status,
            details=details,
            metadata={
                'level': self.config.get('level', 'basic'),
                'version': '1.0'
            }
        )
        
        # 记录到日志
        self.logger.info(event.to_json())
        
        # 发送到 webhook（如果配置）
        webhook_config = self.config.get('output', {}).get('webhook')
        if webhook_config:
            self._send_to_webhook(event, webhook_config)
        
        return event
    
    def _get_source_ip(self) -> Optional[str]:
        """获取源IP地址"""
        import socket
        try:
            return socket.gethostbyname(socket.gethostname())
        except:
            return None
    
    def _send_to_webhook(self, event: AuditEvent, config: Dict):
        """发送事件到 webhook"""
        try:
            url = config.get('url')
            headers = config.get('headers', {})
            timeout = config.get('timeout', 30)
            
            response = requests.post(
                url,
                json=event.to_dict(),
                headers=headers,
                timeout=timeout
            )
            response.raise_for_status()
        except Exception as e:
            # 不抛出异常，避免影响主流程
            self.logger.error(f"Failed to send audit event to webhook: {e}")
    
    # 便捷方法
    def log_auth(self, action: str, status: str, details: Dict = None, **kwargs):
        """记录认证事件"""
        event_type = {
            'login': AuditEventType.AUTH_LOGIN,
            'logout': AuditEventType.AUTH_LOGOUT,
            'denied': AuditEventType.AUTH_DENIED
        }.get(action, AuditEventType.AUTH_LOGIN)
        
        return self.log(event_type, action, status, details, **kwargs)
    
    def log_file(self, action: str, status: str, filepath: str, details: Dict = None, **kwargs):
        """记录文件操作"""
        event_type = {
            'read': AuditEventType.FILE_READ,
            'write': AuditEventType.FILE_WRITE,
            'delete': AuditEventType.FILE_DELETE,
            'execute': AuditEventType.FILE_EXECUTE
        }.get(action, AuditEventType.FILE_READ)
        
        details = details or {}
        details['filepath'] = filepath
        
        return self.log(event_type, action, status, details, resource=filepath, **kwargs)
    
    def log_exec(self, command: str, status: str, details: Dict = None, **kwargs):
        """记录命令执行"""
        event_type = {
            'success': AuditEventType.EXEC_COMPLETE,
            'failed': AuditEventType.EXEC_FAILED,
            'blocked': AuditEventType.EXEC_BLOCKED
        }.get(status, AuditEventType.EXEC_START)
        
        details = details or {}
        details['command'] = command[:1000]  # 限制长度
        
        return self.log(event_type, 'execute', status, details, **kwargs)
    
    def log_security_alert(self, alert_type: str, severity: str, details: Dict = None, **kwargs):
        """记录安全告警"""
        details = details or {}
        details['alert_type'] = alert_type
        details['severity'] = severity
        
        return self.log(
            AuditEventType.SECURITY_ALERT,
            alert_type,
            'alert',
            details,
            **kwargs
        )

# 使用示例
if __name__ == '__main__':
    audit = AuditLogger()
    
    # 记录认证事件
    audit.log_auth('login', 'success', {'method': 'token'}, user_id='user123')
    
    # 记录文件操作
    audit.log_file('read', 'success', '/path/to/file.txt', user_id='user123')
    
    # 记录命令执行
    audit.log_exec('git status', 'success', {'exit_code': 0}, user_id='user123')
    
    # 记录安全告警
    audit.log_security_alert(
        'suspicious_command',
        'high',
        {'command': 'rm -rf /', 'blocked': True}
    )
```

---

## 5. 安全建议

### 5.1 部署安全建议

```markdown
## OpenClaw 部署安全建议

### 1. 系统层面

- [ ] 使用专用用户运行 OpenClaw，避免使用 root
- [ ] 启用 SELinux 或 AppArmor
- [ ] 配置防火墙，仅开放必要端口
- [ ] 定期更新系统和依赖
- [ ] 启用自动安全更新

### 2. 配置安全

- [ ] 使用强密码和密钥
- [ ] 启用 MFA（多因素认证）
- [ ] 定期轮换密钥和令牌
- [ ] 使用最小权限原则配置权限
- [ ] 禁用不必要的服务和功能

### 3. 网络安全

- [ ] 使用 TLS/SSL 加密通信
- [ ] 配置网络隔离和 VLAN
- [ ] 启用 DDoS 防护
- [ ] 使用 VPN 或私有网络访问
- [ ] 定期审查网络访问日志

### 4. 数据安全

- [ ] 加密敏感数据存储
- [ ] 定期备份数据
- [ ] 测试恢复流程
- [ ] 实施数据分类和标记
- [ ] 配置数据保留策略

### 5. 监控和审计

- [ ] 启用全面的日志记录
- [ ] 配置实时监控告警
- [ ] 定期审查审计日志
- [ ] 建立事件响应流程
- [ ] 进行定期安全评估
```

### 5.2 安全检查清单

```bash
#!/bin/bash
# ~/.openclaw/scripts/security-checklist.sh
# OpenClaw 安全检查清单

echo "================================"
echo "OpenClaw 安全检查清单"
echo "================================"
echo ""

CHECKS_PASSED=0
CHECKS_FAILED=0

check() {
    local name="$1"
    local condition="$2"
    
    if eval "${condition}"; then
        echo "✓ ${name}"
        ((CHECKS_PASSED++))
    else
        echo "✗ ${name}"
        ((CHECKS_FAILED++))
    fi
}

echo "1. 文件权限检查"
echo "----------------"
check "配置目录权限正确" "test $(stat -c %a ~/.openclaw 2>/dev/null) = '700'"
check "密钥文件权限正确" "test $(stat -c %a ~/.openclaw/secrets/.master.key 2>/dev/null) = '600'"
check "日志目录权限正确" "test $(stat -c %a ~/.openclaw/logs 2>/dev/null) = '755'"

echo ""
echo "2. 配置检查"
echo "------------"
check "权限配置文件存在" "test -f ~/.openclaw/config/permissions.yaml"
check "工具策略配置存在" "test -f ~/.openclaw/config/tool_policies.yaml"
check "审计配置存在" "test -f ~/.openclaw/config/audit.yaml"

echo ""
echo "3. 密钥管理检查"
echo "----------------"
check "主密钥存在" "test -f ~/.openclaw/secrets/.master.key"
check "密钥目录权限正确" "test $(stat -c %a ~/.openclaw/secrets 2>/dev/null) = '700'"

echo ""
echo "4. 沙箱检查"
echo "------------"
check "Docker 已安装" "command -v docker > /dev/null"
check "Docker 守护进程运行中" "docker info > /dev/null 2>&1"
check "沙箱配置文件存在" "test -f ~/.openclaw/docker/sandbox-compose.yaml"
check "Seccomp 配置文件存在" "test -f ~/.openclaw/docker/seccomp-profile.json"

echo ""
echo "5. 日志和审计检查"
echo "------------------"
check "审计日志目录存在" "test -d ~/.openclaw/logs"
check "审计日志可写" "test -w ~/.openclaw/logs"

echo ""
echo "================================"
echo "检查结果: ${CHECKS_PASSED} 通过, ${CHECKS_FAILED} 失败"
echo "================================"

if [[ ${CHECKS_FAILED} -gt 0 ]]; then
    exit 1
fi
```

---

> 文档版本: 1.0
> 最后更新: 2026-03-01
> 维护者: OpenClaw 安全团队
