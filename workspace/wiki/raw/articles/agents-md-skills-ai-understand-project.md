---
source_url: https://mp.weixin.qq.com/s/...
ingested: 2026-05-21
sha256: 2eabd572ef13fe7b
title: AGENTS.md + Skills：让 AI 真正理解你的项目
author: AI布道官
source: 微信公众号
level: standard
---

🔥 一条 /init 命令，AI 就能读懂你整个项目。这不是魔法，这是 AGENTS.md。

通用 AI 不知道你的团队规矩、代码风格、目录约定——AGENTS.md 是你给 AI 写的「项目说明书」，Skills 是你给 AI 装的「技能包」。两者配合，让 OpenCode 从「通用助手」变成「项目专家」。
📌 核心概念：为什么需要 AGENTS.md？通用 AI 的「痛点」
想象你新招了一个能力很强但不了解项目的开发者。他写的代码可能功能正确，但：
• 不知道你们用 camelCase 还是 snake_case• 不清楚 packages/core/ 是放共享逻辑的地方• 不知道部署前必须跑 pnpm lint• 不了解你们团队的 Git 提交规范
OpenCode 也一样。 默认情况下，它是一个通用的 AI 编程助手——技术很强，但对你项目的上下文一无所知。
AGENTS.md 就是「项目说明书」
AGENTS.md 是项目级的 AI 配置文件。你可以把它理解为：

.editorconfig  →  告诉编辑器怎么格式化代码
.gitignore     →  告诉 Git 哪些文件要忽略
AGENTS.md      →  告诉 AI 怎么理解你的项目
💡 类比：.editorconfig 给编辑器看，AGENTS.md 给 AI 看。两者都是项目级配置，都应该提交到 Git。
AGENTS.md 如何影响 AI 的行为
Mermaid 渲染失败: Failed to fetch dynamically imported module: http://127.0.0.1:8800/static/js/md-sequenceDiagram-FGHM5R23-BIxt3VcS.js

OpenCode 启动时，会将 AGENTS.md 的内容作为系统提示词（System Prompt）的一部分注入到每次对话中。这意味着 AI 在处理任何任务时，都会自动遵循你在 AGENTS.md 中定义的规范。
📝 AGENTS.md 详解/init 命令：一键生成项目说明书
OpenCode 内置了 /init 命令，可以自动分析项目并生成 AGENTS.md：

你：/init

OpenCode：
🔍 正在扫描项目结构...
📦 检测到 Go 项目，使用 Gin 框架
📁 分析目录组织...
📝 分析代码规范...
✅ 已生成 AGENTS.md
/init 的工作流程：

/init 命令
扫描项目文件识别技术栈分析目录结构提取代码规范
生成 AGENTS.md

⚠️ 注意：如果项目已存在 AGENTS.md，/init 会在现有内容基础上补充，而不是覆盖。这保护了你手动编写的自定义内容。
AGENTS.md 的推荐结构
一份好的 AGENTS.md 应该包含以下模块：

AGENTS.md

项目概述

代码规范

项目结构

特殊约定

构建和测试

已知问题
做什么、技术栈命名、格式化、架构目录组织说明环境配置、部署常用命令坑和注意事项
模块 1：项目概述
告诉 AI 这个项目是做什么的、用了什么技术栈。

## 项目概述

这是一个用户认证微服务，基于 Go 语言开发。
- 语言：Go 1.22
- 框架：Gin v1.9
- 数据库：PostgreSQL 15 + GORM
- 缓存：Redis 7
- 认证：JWT（RS256 算法）模块 2：代码规范
定义团队遵循的编码标准和风格。

## 代码规范

- 使用驼峰命名法（camelCase）命名变量和函数
- 使用 PascalCase 命名结构体和接口
- 错误处理必须显式检查，不使用 panic
- 所有公开函数必须有 godoc 注释
- 单个函数不超过 80 行
- import 分组：标准库 / 第三方库 / 项目内部包，每组空行分隔模块 3：项目结构说明
让 AI 了解目录的组织逻辑。

## 项目结构

- `cmd/server/` - 程序入口
- `internal/handler/` - HTTP 请求处理器
- `internal/service/` - 业务逻辑层
- `internal/repository/` - 数据访问层
- `internal/model/` - 数据模型
- `pkg/auth/` - 认证相关可复用包
- `config/` - 配置文件
- `migrations/` - 数据库迁移脚本模块 4：特殊约定
记录项目特有的全局变量、环境配置、部署流程等。

## 特殊约定

- 环境变量通过 `.env` 文件管理，不硬编码到代码中
- 数据库迁移使用 golang-migrate，文件命名格式：`000001_create_users_table.up.sql`
- API 响应统一使用 `{"code": 0, "message": "", "data": {}}` 格式
- 分页参数统一使用 `page` 和 `pageSize`，默认 pageSize=20
- 部署使用 Docker + GitHub Actions，主分支为 main模块 5：构建和测试命令
告诉 AI 如何构建、测试、部署你的项目。

## 构建和测试

```bash
# 运行项目
go run cmd/server/main.go

# 运行所有测试
go test ./...

# 运行特定包测试
go test ./internal/service/...

# 构建二进制文件
go build -o bin/server cmd/server/main.go

# 数据库迁移
migrate -path migrations -database "postgres://..." up

#### 模块 6：已知问题和注意事项

记录项目中的「坑」，帮 AI 避开常见陷阱。

```markdown
## 已知问题和注意事项

- Redis 连接池大小不能超过 50，否则会触发服务端限制
- 用户表的 email 字段有唯一约束，更新时要注意
- `internal/service/user.go` 中的 `CreateUser` 方法有缓存一致性问题，暂时通过 TTL 缓解
- 不要修改 `pkg/auth/jwt.go` 中的签名算法，已有线上用户依赖 RS256最佳实践：要写什么、不要写什么应该写不应该写项目概述和技术栈冗长的背景介绍命名规范和代码风格通用编程常识目录结构和模块职责每个文件的详细说明特定的 API 约定HTTP 协议基础知识构建/测试/部署命令基础工具的使用教程已知的坑和注意事项过于笼统的描述团队特有的工作流约定行业通用的最佳实践
⚠️ 关键原则：AGENTS.md 应该只包含项目特有的信息。通用知识 AI 已经会了，不需要重复教。
实战示例示例 1：Go 项目 AGENTS.md
# User Service

用户管理微服务，负责用户注册、登录、权限管理。

## Tech Stack

- Go 1.22 + Gin v1.9
- PostgreSQL 15 + GORM v2
- Redis 7 (session cache)
- gRPC (inter-service communication)
- Docker + Kubernetes

## Project Structure

- `cmd/` - 程序入口 (server, worker, migration)
- `internal/handler/` - HTTP handlers
- `internal/service/` - Business logic
- `internal/repository/` - Data access layer
- `internal/model/` - Database models
- `pkg/` - Shared packages
- `api/proto/` - gRPC proto definitions
- `deploy/` - Kubernetes manifests

## Code Standards

- Follow effective Go guidelines
- Use camelCase for variables, PascalCase for exported names
- Error handling: always check errors, never panic in production
- All exported functions must have godoc comments
- Keep functions under 80 lines

## Commands

```bash
go run cmd/server/main.go      # Run server
go test ./...                   # Run all tests
go test -race ./...             # Run tests with race detector
docker compose up -d            # Start dependencies
make build                      # Build binaryImportant Notes• Proto files must be compiled before building: make proto• Database uses soft deletes (gorm.DeletedAt)• Rate limiting is enforced at gateway level, not here• JWT token TTL: access=15min, refresh=7d

#### 示例 2：Java/Spring Boot 项目 AGENTS.md

```markdown
# Order Management System

订单管理系统后端服务，处理订单创建、支付、发货全流程。

## Tech Stack

- Java 17 + Spring Boot 3.2
- Gradle (Kotlin DSL)
- MySQL 8.0 + MyBatis Plus
- Redis (distributed lock)
- RabbitMQ (async messaging)
- Spring Security + JWT

## Project Structure

- `src/main/java/com/example/oms/`
  - `controller/` - REST API controllers
  - `service/` - Business logic layer
  - `mapper/` - MyBatis mappers (data access)
  - `entity/` - Database entities
  - `dto/` - Data Transfer Objects
  - `config/` - Spring configurations
  - `common/` - Shared utilities and constants
  - `exception/` - Global exception handling
- `src/main/resources/`
  - `mapper/` - MyBatis XML mappers
  - `db/migration/` - Flyway migration scripts

## Code Standards

- Follow Alibaba Java Development Manual
- Use Lombok to reduce boilerplate
- Use Java Stream API for collection operations
- Controller only handles request/response, no business logic
- Service layer handles all business logic
- Use `@Transactional` for database operations
- All API responses use `Result<T>` wrapper

## Naming Conventions

- Database tables: `t_order`, `t_order_item`, `t_payment`
- REST endpoints: `/api/v1/orders`, `/api/v1/orders/{id}`
- DTO naming: `OrderCreateDTO`, `OrderQueryDTO`

## Commands

```bash
./gradlew bootRun                # Run application
./gradlew test                   # Run tests
./gradlew clean build -x test    # Build without tests
./gradlew flywayMigrate          # Run database migration
docker compose up -d             # Start dependenciesImportant Notes• Flyway migration versioning: V{version}__{description}.sql• Order status transitions must follow state machine rules• Payment callback uses idempotent design• Distributed lock for inventory deduction (Redis + Redisson)

#### 示例 3：前端项目 AGENTS.md

```markdown
# Dashboard Web App

数据可视化后台管理系统，基于 React + TypeScript。

## Tech Stack

- React 18 + TypeScript 5
- Vite 5 (build tool)
- TanStack Router (routing)
- TanStack Query (data fetching)
- TailwindCSS 3 (styling)
- shadcn/ui (component library)
- Vitest + Playwright (testing)

## Project Structure

- `src/components/` - Reusable components
  - `ui/` - shadcn/ui base components
  - `forms/` - Form components
  - `charts/` - Chart wrappers
- `src/features/` - Feature-based modules
- `src/hooks/` - Custom React hooks
- `src/lib/` - Utility functions
- `src/routes/` - Route definitions (file-based routing)
- `src/types/` - TypeScript type definitions
- `src/mocks/` - MSW mock handlers

## Code Standards

- Use TypeScript strict mode
- Functional components only, no class components
- Use `const` + arrow functions for components
- Colocate styles with components (Tailwind classes)
- Custom hooks for reusable stateful logic
- Use `@/` path alias for imports

## Component Conventions

- Component files: PascalCase (e.g., `UserList.tsx`)
- Hook files: camelCase with `use` prefix (e.g., `useAuth.ts`)
- One component per file
- Export component as default export
- Props interface named `ComponentNameProps`

## Commands

```bash
pnpm dev              # Development server
pnpm build            # Production build
pnpm test             # Run unit tests
pnpm test:e2e         # Run e2e tests
pnpm lint             # Run ESLint
pnpm storybook        # Start StorybookImportant Notes• API base URL configured via VITE_API_URL env variable• All API calls go through src/lib/api-client.ts• Auth tokens stored in httpOnly cookies (not localStorage)• Use React Query for all server state, avoid local state for API data

---

## 🎯 Skills 系统：给 AI 装上「技能包」

### Skills 是什么

如果说 `AGENTS.md` 是「项目说明书」，那 **Skills（技能）** 就是「操作手册」。

Skills 是预定义的**可复用指令模块**，AI 可以在需要时按需加载。它们不同于 `AGENTS.md` 的「始终存在」，而是**按需发现、按需加载**。

```mermaid
graph LR
    A["AGENTS.md"] -->|"始终加载"| B["AI 上下文"]
    C["Skills"] -->|"按需加载"| B

    A -.->|"项目知识<br/>编码规范"| B
    C -.->|"专项技能<br/>操作流程"| B

    style A fill:#4F46E5,color:#fff
    style C fill:#059669,color:#fff
    style B fill:#D97706,color:#fffSkill 文件结构
每个 Skill 是 .opencode/skills/ 目录下的一个文件夹，包含一个 SKILL.md 文件：

.opencode/
└── skills/
    ├── git-release/
    │   └── SKILL.md        # Git 发版技能
    ├── pr-review/
    │   └── SKILL.md        # PR 审查技能
    └── db-migration/
        └── SKILL.md        # 数据库迁移技能
Skill 的存放位置有多个，OpenCode 按以下路径搜索：
路径作用域说明.opencode/skills/<name>/SKILL.md项目级团队共享，提交到 Git~/.config/opencode/skills/<name>/SKILL.md全局个人技能，不共享.claude/skills/<name>/SKILL.mdClaude 兼容从 Claude Code 迁移的技能~/.claude/skills/<name>/SKILL.mdClaude 全局Claude Code 全局兼容
💡 命名规则：Skill 名称（文件夹名）只能包含小写字母、数字和单个连字符，长度 1-64 字符，例如 git-release、pr-review。
SKILL.md 的 Frontmatter
每个 SKILL.md 必须以 YAML frontmatter 开头：

---
name: git-release
description: Create consistent releases and changelogs
license: MIT
compatibility: opencode
metadata:
  audience: maintainers
  workflow: github
---

## What I do

- Draft release notes from merged PRs
- Propose a version bump
- Provide a copy-pasteable `gh release create` command

## When to use me

Use this when you are preparing a tagged release.
Ask clarifying questions if the target versioning scheme is unclear.
Frontmatter 字段说明：
字段必填说明name是技能名称，必须与文件夹名一致，1-64 字符description是技能描述，1-1024 字符，帮助 AI 判断何时使用license否许可证信息compatibility否兼容性标记metadata否自定义元数据（键值对）Skill 的发现与加载机制
Mermaid 渲染失败: Failed to fetch dynamically imported module: http://127.0.0.1:8800/static/js/md-sequenceDiagram-FGHM5R23-BIxt3VcS.js

关键点：
1. 启动时：OpenCode 只扫描技能列表（名称 + 描述），不会加载全部内容2. 按需加载：只有当 AI 判断需要某个技能时，才会通过 skill 工具加载完整内容3. 智能选择：AI 根据 description 字段自动判断何时使用哪个技能实战：创建自定义 Skill示例 1：Git 发版技能
创建 .opencode/skills/git-release/SKILL.md：

---
name: git-release
description: Create consistent releases and changelogs from merged PRs
metadata:
  audience: maintainers
  workflow: github
---

## What I do

- Analyze merged PRs since the last tag
- Draft release notes grouped by type (feat/fix/breaking)
- Propose the next version number following semver
- Generate a copy-pasteable `gh release create` command

## Steps

1. Run `git log <last-tag>..HEAD --oneline` to find merged changes
2. Categorize changes: features, bug fixes, breaking changes
3. Propose version bump (major/minor/patch) based on changes
4. Generate release notes in Keep a Changelog format
5. Provide the `gh release create` command

## Rules

- Always ask for confirmation before creating the release
- Include PR numbers and author mentions in release notes
- Flag any breaking changes prominently
使用效果：

你：帮我准备 v2.3.0 的发布

OpenCode：
🔧 Loading skill: git-release
📋 Analyzing changes since v2.2.0...

## Release v2.3.0

### Features
- Add user export to CSV (#142 by @alice)
- Support dark mode toggle (#145 by @bob)

### Bug Fixes
- Fix pagination overflow on mobile (#143)

### Command
gh release create v2.3.0 --title "v2.3.0" --notes "..."示例 2：数据库迁移技能
创建 .opencode/skills/db-migration/SKILL.md：

---
name: db-migration
description: Create and manage database migrations with proper naming and safety checks
metadata:
  category: database
---

## What I do

- Create new migration files with proper naming
- Review migration SQL for safety (no data loss)
- Generate rollback scripts
- Validate migration order

## Migration Naming Convention

- Format: `V{version}__{description}.sql`
- Version must be sequential
- Description in snake_case
- Example: `V005__add_user_phone_column.sql`

## Safety Rules

- NEVER use DROP COLUMN without creating a backup first
- ALWAYS provide a rollback script
- Data migration must be done in batches (max 1000 rows per batch)
- Test migration on local database before suggesting

## Steps for New Migration

1. Determine the next version number
2. Write the UP migration SQL
3. Write the DOWN (rollback) migration SQL
4. Add comments explaining non-obvious operations
5. Suggest a local test command示例 3：代码审查技能
创建 .opencode/skills/pr-review/SKILL.md：

---
name: pr-review
description: Perform thorough code review focusing on security, performance, and maintainability
metadata:
  category: review
---

## What I do

- Review code changes with a structured checklist
- Focus on security, performance, and maintainability
- Provide actionable suggestions with code examples
- Generate a review summary

## Review Checklist

### Security
- [ ] Input validation and sanitization
- [ ] SQL injection prevention
- [ ] Authentication and authorization checks
- [ ] Sensitive data exposure

### Performance
- [ ] N+1 query detection
- [ ] Unnecessary re-renders (frontend)
- [ ] Missing indexes
- [ ] Memory leaks

### Maintainability
- [ ] Function length (< 50 lines)
- [ ] Proper error handling
- [ ] Meaningful naming
- [ ] Adequate test coverage

## Output Format

### Summary
Brief overall assessment

### Critical Issues
Issues that must be fixed before merge

### Suggestions
Nice-to-have improvements

### Positive Notes
Good practices worth highlightingSkill 权限控制
你可以在 opencode.json 中控制 AI 可以访问哪些技能：

{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "skill": {
      "*": "allow",
      "internal-*": "deny",
      "experimental-*": "ask"
    }
  }
}权限值行为allow技能立即加载，无需确认deny完全隐藏技能，AI 无法看到和使用ask每次加载前询问用户确认⚖️ AGENTS.md vs opencode.json：谁负责什么？定位对比

opencode.json — 工具的配置
模型选择

API 密钥

权限控制

MCP 服务器

插件管理
AGENTS.md — AI 的知识
项目概述

代码规范

目录结构

特殊约定

构建命令

详细对比维度AGENTS.mdopencode.json本质Markdown 文本，给 AI 读的JSON 配置，给 OpenCode 框架读的内容项目知识、编码规范、团队约定模型、权限、MCP、插件等技术配置格式Markdown（自由文本）JSON/JSONC（结构化数据）作用对象LLM 模型（影响 AI 输出）OpenCode 框架（影响工具行为）位置项目根目录项目根目录或 ~/.config/opencode/是否提交 Git是，团队共享是（但 API Key 用环境变量）什么时候用 AGENTS.md• 定义项目的代码规范和风格指南• 说明目录结构和模块职责• 记录构建、测试、部署命令• 列出已知的技术债务和注意事项• 描述团队的 Git 提交规范• 定义 API 约定和数据格式什么时候用 opencode.json• 配置使用哪个 LLM 模型• 管理 API 密钥和提供商• 设置文件编辑和 bash 命令的权限• 配置 MCP 服务器连接• 加载插件和自定义命令• 配置主题和快捷键两者如何配合
一个典型项目的配置组合：

my-project/
├── AGENTS.md              # 项目知识（提交 Git）
├── opencode.json          # 工具配置（提交 Git，API Key 用环境变量）
├── .opencode/
│   ├── agents/            # 自定义代理
│   ├── commands/          # 自定义命令
│   └── skills/            # 自定义技能
└── .env                   # 环境变量（不提交 Git）
opencode.json 还可以通过 instructions 字段引用额外的规则文件，与 AGENTS.md 合并生效：

{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-5",
  "instructions": [
    "CONTRIBUTING.md",
    "docs/coding-standards.md",
    ".cursor/rules/*.md"
  ]
}
💡 instructions 中的所有文件会和 AGENTS.md 一起注入到 AI 的上下文中。这意味着你可以复用团队已有的规范文档，无需重复维护。
👥 团队共享最佳实践1. 把 AGENTS.md 提交到 Git
# AGENTS.md 应该被版本控制
git add AGENTS.md
git commit -m "docs: add AGENTS.md for AI project context"

# 敏感信息不要放在 AGENTS.md 里
# 使用 .env + opencode.json 的 {env:XXX} 来管理密钥2. 利用分层配置满足个性化需求
OpenCode 支持多层配置，每层有不同的作用域：

团队公共规范

个人偏好

项目级 AGENTS.md(Git 共享)
AI 上下文
全局 AGENTS.md(~/.config/opencode/)

instructions 引用(opencode.json)

Skills(.opencode/skills/)

文件作用域是否提交 Git用途AGENTS.md项目是团队共享的项目知识~/.config/opencode/AGENTS.md全局否个人偏好（如「用中文回复」）.opencode/skills/项目是团队共享的技能包~/.config/opencode/skills/全局否个人技能包3. 全局 AGENTS.md 示例
~/.config/opencode/AGENTS.md——你个人的 AI 偏好：

# Personal Preferences

- Always respond in Chinese (Simplified)
- Use concise explanations, avoid verbosity
- When generating code, include brief Chinese comments
- Prefer functional programming style when possible4. 多项目共享规范
如果你的团队有多个项目共享相同的规范，有两种方式：

方式 A：使用远程 URL 指令

{
  "instructions": [
    "https://raw.githubusercontent.com/my-org/shared-rules/main/java-standards.md",
    "https://raw.githubusercontent.com/my-org/shared-rules/main/git-conventions.md"
  ]
}
方式 B：使用 Git 子模块或符号链接

# 把共享规范作为 Git 子模块引入
git submodule add https://github.com/my-org/shared-rules.git shared-rules

# 在 opencode.json 中引用
# "instructions": ["shared-rules/java-standards.md"]💡 进阶技巧技巧 1：在 AGENTS.md 中引用外部规则文件
虽然 OpenCode 不会自动解析 AGENTS.md 中的文件引用，但你可以在文件中提供明确指令，教 AI 按需读取外部文件：

# Project Rules

## External File Loading

CRITICAL: When you encounter a file reference (e.g., @rules/general.md),
use your Read tool to load it on a need-to-know basis.

Instructions:
- Do NOT preemptively load all references
- When loaded, treat content as mandatory instructions
- Follow references recursively when needed

## Development Guidelines

For TypeScript code style: @docs/typescript-guidelines.md
For API design patterns: @docs/api-standards.md
For testing strategies: @test/testing-guidelines.md
⚠️ 推荐使用 opencode.json 的 instructions 字段替代这种方式，因为 instructions 由框架自动处理，更可靠。
技巧 2：为不同代理定制不同的行为
结合代理系统和 AGENTS.md，可以让不同代理有不同的行为倾向。在 AGENTS.md 中使用条件指令：

# Project Rules

## General

- All code must pass linting before commit
- Use TypeScript strict mode

## For Build Agent

- When creating new files, always add corresponding test files
- Run `pnpm lint --fix` after each code change

## For Plan Agent

- Always estimate complexity (S/M/L) for each task
- List dependencies before suggesting implementation order技巧 3：Claude Code 无缝迁移
如果你从 Claude Code 迁移到 OpenCode，无需立即修改配置文件：

Claude Code 配置

OpenCode 兼容层

CLAUDE.md → AGENTS.md

~/.claude/CLAUDE.md → 全局 AGENTS.md

~/.claude/skills/ → Skills

OpenCode 会自动识别：
• 项目目录的 CLAUDE.md（当没有 AGENTS.md 时）• 全局的 ~/.claude/CLAUDE.md（当没有 ~/.config/opencode/AGENTS.md 时）• ~/.claude/skills/ 下的技能文件
如果需要禁用 Claude Code 兼容模式：

# 完全禁用 .claude 支持
export OPENCODE_DISABLE_CLAUDE_CODE=1

# 只禁用 ~/.claude/CLAUDE.md
export OPENCODE_DISABLE_CLAUDE_CODE_PROMPT=1

# 只禁用 .claude/skills
export OPENCODE_DISABLE_CLAUDE_CODE_SKILLS=1技巧 4：动态更新 AGENTS.md
当项目发生重大变更时（比如引入新框架、调整目录结构），记得同步更新 AGENTS.md：

# 方法 1：再次运行 /init，会在现有基础上补充
/init

# 方法 2：手动编辑 AGENTS.md
# 只更新变更的部分，保持其他内容不变
💡 建议：在代码审查流程中加入 AGENTS.md 的检查项。当项目结构或规范发生变更时，PR 中应该同步更新 AGENTS.md。
⚠️ 常见问题（FAQ）Q1：AGENTS.md 和 CLAUDE.md 有什么区别？
AGENTS.md 是 OpenCode 的原生格式，CLAUDE.md 是 Claude Code 的格式。OpenCode 优先读取 AGENTS.md，如果没有才回退到 CLAUDE.md。建议使用 AGENTS.md 以获得最佳兼容性。
Q2：AGENTS.md 内容太长会不会影响性能？
会。AGENTS.md 的内容会作为系统提示词注入每次对话，过长的内容会占用上下文窗口。建议控制在 500 行以内，聚焦项目特有信息。详细规范可以通过 instructions 字段按需加载。
Q3：可以在 monorepo 的子目录中放 AGENTS.md 吗？
可以。OpenCode 会从当前目录向上遍历到 Git 根目录，沿途加载所有 AGENTS.md。这意味着你可以在 packages/api/AGENTS.md 中放 API 模块特有的规范，同时在根目录的 AGENTS.md 放全局规范。
Q4：Skill 和自定义命令有什么区别？维度Skill自定义命令加载方式AI 按需自动加载用户手动触发（/command）定义位置.opencode/skills/.opencode/commands/适用场景通用操作流程（发版、迁移）固定步骤的快捷操作参数支持无（AI 自行判断）支持 $ARGUMENTS灵活性AI 决定是否使用用户决定何时使用Q5：如何验证 AGENTS.md 是否生效？
在 OpenCode 中直接提问：

你：你知道我们项目的代码规范是什么吗？

OpenCode：
根据项目配置：
- 使用 Go 1.22 + Gin 框架
- 变量用 camelCase 命名
- 公开函数必须有 godoc 注释
...
如果 AI 能准确复述你定义的规范，说明 AGENTS.md 已生效。
Q6：多个规则文件之间会冲突吗？
OpenCode 按优先级加载规则文件，后面的覆盖前面的：
1. 本地 AGENTS.md（项目根目录向上遍历）2. 全局 ~/.config/opencode/AGENTS.md3. Claude Code 兼容 ~/.claude/CLAUDE.md
在同一类别中，AGENTS.md 优先于 CLAUDE.md。instructions 字段中的文件会和 AGENTS.md 合并生效。
📚 总结
项目 AI 理解 = AGENTS.md（始终在线的项目知识） + Skills（按需加载的操作技能）
通过本文，你已经掌握了：
• ✅ 为什么需要 AGENTS.md——通用 AI 不知道你的团队规矩• ✅ AGENTS.md 的推荐结构和最佳实践——写什么、不写什么• ✅ 三种项目类型（Go / Java / 前端）的实战示例• ✅ Skills 系统的工作原理——发现机制、frontmatter、按需加载• ✅ AGENTS.md 与 opencode.json 的定位区别——谁负责什么• ✅ 团队共享和多项目协作的配置策略• ✅ 从 Claude Code 无缝迁移的兼容方案
👉 AGENTS.md 是团队 AI 协作的关键，关注我，持续获取 AI 编程干货。

接下来，建议按顺序阅读本系列后续文章：
篇目主题你将学到第 6 篇自定义命令——把重复操作变成一条指令命令创建、模板变量、Shell 注入、团队命令库🔗 延伸阅读• OpenCode 官方文档 - 规则[1]• OpenCode 官方文档 - 代理技能[2]• OpenCode 官方文档 - 代理[3]• OpenCode 官方文档 - 配置[4]• OpenCode GitHub 仓库[5]
💬 互动时间

你现在用的什么 AI 编程工具？体验如何？评论区聊聊👇

如果这个系列帮到了你，点个**「关注」、「在看」**，转发给需要的同事，让更多人看到。

作者：AI布道官 | 系列：《OpenCode 完全指南》第 5 篇（共 12 篇）
引用链接
[1] OpenCode 官方文档 - 规则: https://opencode.ai/docs/zh-cn/rules/
[2] OpenCode 官方文档 - 代理技能: https://opencode.ai/docs/zh-cn/skills/
[3] OpenCode 官方文档 - 代理: https://opencode.ai/docs/zh-cn/agents/
[4] OpenCode 官方文档 - 配置: https://opencode.ai/docs/zh-cn/config/
[5] OpenCode GitHub 仓库: https://github.com/opencode-ai/opencode

