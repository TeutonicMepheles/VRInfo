const summaryData = [
  {
    title: "1) 具身交互与多模态融合成为主线",
    points: [
      "手势 + 眼动 + 语音 + 触觉反馈的组合式交互成为 2025 年后最稳定增长方向。",
      "研究重点从“识别准确率”转向“任务连续性”和“认知负荷最小化”。"
    ]
  },
  {
    title: "2) AI 驱动的自适应界面快速增加",
    points: [
      "大模型与行为建模用于动态调整虚拟控件布局、提示强度与交互路径。",
      "设计研究更多关注可解释性、人机共控以及错误恢复流程。"
    ]
  },
  {
    title: "3) 协同 VR 的交互协议标准化",
    points: [
      "远程协作场景中，跨设备一致性与低时延反馈成为论文高频关键词。",
      "ACM / IEEE 论文中可复现工具链与基准任务集数量上升。"
    ]
  },
  {
    title: "4) 可访问性与包容性设计受到持续重视",
    points: [
      "更多成果开始覆盖老年人、低视力用户与运动能力受限人群。",
      "“可访问性默认开启”逐渐成为交互组件的设计建议。"
    ]
  },
  {
    title: "5) 评测从单次实验向长期生态评估迁移",
    points: [
      "2025 年后论文更强调纵向用户研究、真实任务迁移与部署成本。",
      "出现“体验质量 + 效率 + 疲劳/晕动症 + 隐私风险”的多指标联合评估。"
    ]
  }
];

function renderSummary() {
  const wrap = document.getElementById("summary");
  summaryData.forEach((item) => {
    const block = document.createElement("article");
    const h = document.createElement("h3");
    h.textContent = item.title;
    const ul = document.createElement("ul");
    item.points.forEach((p) => {
      const li = document.createElement("li");
      li.textContent = p;
      ul.appendChild(li);
    });
    block.append(h, ul);
    wrap.appendChild(block);
  });
}

function cardTemplate(card) {
  const papers = card.papers.length ? card.papers.map((p) => `
    <li>
      <strong>${p.title}</strong>
      <div class="meta">来源：${p.source} · 发表日期：${p.published || "未知"}</div>
      <a href="${p.url}" target="_blank" rel="noopener noreferrer">原文链接</a>
    </li>
  `).join("") : "<li>暂无可展示论文，系统将在下一次抓取时自动更新。</li>";

  return `
    <article class="card">
      <div class="meta">
        <span class="tag">${card.date}</span>
        <span>${card.topic}</span>
      </div>
      <h3>${card.title}</h3>
      <p>${card.summary}</p>
      <ul>${papers}</ul>
    </article>
  `;
}

async function renderCards() {
  const res = await fetch("data/cards.json");
  const cards = await res.json();
  if (!cards.length) return;

  const today = document.getElementById("today-card");
  const history = document.getElementById("history");

  today.innerHTML = cardTemplate(cards[0]);
  history.innerHTML = cards.slice(1).map(cardTemplate).join("") || "<p>暂无历史卡片。</p>";
}

renderSummary();
renderCards();
