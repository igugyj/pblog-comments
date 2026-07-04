# 如何添加友链？

![Friend Links Check](https://github.com/csy214-beep/pblog-comments/actions/workflows/check_friends.yml/badge.svg)

<!-- [![Sync to Gitee](https://github.com/csy214-beep/pblog-comments/actions/workflows/sync-to-gitee.yml/badge.svg?branch=main)](https://github.com/csy214-beep/pblog-comments/actions/workflows/sync-to-gitee.yml) -->

欢迎来和本博客互换友链！你可以通过以下任意一种方式提交你的网站信息。

## 友链数据格式

请提供如下 JSON 格式的信息（一个对象或数组均可）：

```json
{
  "name": "你的网站名称",
  "link": ["https://你的网址.com", "https://另一个链接.com"],
  "description": "简短介绍（建议不超过 50 字）",
  "avatar": "https://example.com/avatar.png"
}
```

- `name`：必填，你的网站名称
- `link`：必填，一个或多个链接（支持多平台链接，如博客、GitHub、Twitter 等）
- `description`：必填，一句话介绍
- `avatar`：必填，头像图片的直链（正方形，建议 200x200 以上），如果失效会显示名称首字母

## 提交方式

### 1. 提交 GitHub Issue (推荐)

- 点击 issues
- 选择申请友链的 issue 模板
- 按格式填写并提交
- GitHub Action 自动审核完成友链添加

### 2. 发起 Pull Request

- Fork
- 编辑 `friends.json` 文件（若不存在请新建），将你的信息追加到 JSON 数组中
- 提交 Pull Request，等待合并

### 3. 发送邮件

- 将你的友链信息（JSON 格式）发送至 `hello@pg25-lsae.eu.org`
- 邮件主题请注明「友链申请」

### 4. 私信

- 如果你拥有我的联系方式，可直接私信我。

<details>
<summary>中文邮件模板</summary>

**收件人**: <hello@pg25-lsae.eu.org>

**主题**: 友链申请 - 你的网站名称

```
你好！

我想申请与 FunRadiusP 博客交换友链，以下是我的网站信息（JSON 格式）：

{
  "name": "我的网站名称",
  "link": ["https://myblog.com"],
  "description": "一个专注技术分享的个人博客",
  "avatar": "https://myblog.com/avatar.png"
}

感谢你的审核，期待相互链接！
（如有其他想说的可在此补充）
```

</details>

<details>
<summary>English Email Template</summary>

**To**: <hello@pg25-lsae.eu.org>

**Subject**: Friend Link Request - Your Site Name

```
Hi there,

I'd like to apply for a friend link with FunRadiusP. Here are my site details in JSON format:

{
  "name": "My Awesome Blog",
  "link": ["https://myblog.com"],
  "description": "A tech-focused personal blog sharing coding tips and projects.",
  "avatar": "https://myblog.com/avatar.png"
}

Thanks for your review, looking forward to the mutual link!
(Feel free to add any extra message here)
```

</details>

---

## 审核标准

- 本站没有静态/动态站限制
- 网站内容健康、无违法内容
- 稳定运行，无大量 404 或挂掉
- 希望你也能在网站中添加本站的链接（互惠互利）

<details>
<summary>我的数据</summary>

```json
{
  "name": "Pfolg",
  "link": ["https://pg25-lsae.eu.org","https://github.com/igugyj"],
  "description": "Seeking between the ebb and flow of binary tides.",
  "avatar": "https://avatars.githubusercontent.com/u/237149328"
}
```

> 不强制要求您添加我的链接

</details>

## 常见问题

**Q：可以添加多个链接吗？**
A：可以，`link` 字段支持字符串数组，每个链接都会独立显示。

**Q：头像可以不用图片吗？**
A：如果不提供或图片加载失败，页面会自动显示名称的首字母作为头像。

**Q：我的信息多久能上线？**
A：采用 ISSUE/PR 方式，我处理后更新在`friends.json`即可显示在网站上；邮件方式可能会稍慢。通常在 1-2 天内完成。

**Q：如何修改/删除友链？**
A: 可以用Issue、PR、邮件、私信等方式，欢迎**随时**增删改！

---

期待你的友链！🌐
