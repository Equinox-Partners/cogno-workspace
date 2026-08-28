import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

plt.rcParams["font.family"] = "Hiragino Sans"

# Palette (dataviz skill reference palette, light mode)
BLUE = "#2a78d6"      # slot1 - Briquet (own)
AQUA = "#1baf7a"       # slot2 - 専門・マニア特化型
YELLOW = "#eda100"     # slot3 - 総合・低価格訴求型
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"
SURFACE = "#fcfcfb"

# x: 品揃えの専門性（0=万人向け総合 → 10=マニア/ニッチ特化）
# y: 購入体験の利便性（0=アナログ・書類手続き重視 → 10=モダンでスムーズ）
players = [
    # name, x, y, group, (dx, dy) offset in fontsize units
    ("ブリケオンライン\n（自社）", 3.4, 8.8, "own", (0.28, 0.28)),
    ("いづみや", 1.6, 3.0, "general", (0.28, 0.28)),
    ("第一商事", 3.8, 2.2, "general", (0.28, 0.28)),
    ("クロード", 7.0, 3.4, "specialist", (0.28, 0.28)),
    ("ダイショー\nたばこショップ", 6.2, 4.4, "specialist", (-2.2, 0.28)),
    ("丑山タバコ\n合同会社", 5.0, 2.0, "specialist", (0.28, 0.28)),
    ("シリウスたばこ", 7.2, 4.6, "specialist", (-2.6, 0.5)),
    ("たばこ専門店\nさくらんぼ", 8.0, 4.2, "specialist", (0.28, -1.6)),
]

colors = {"own": BLUE, "general": YELLOW, "specialist": AQUA}
labels_group = {"own": "ブリケオンライン（自社）", "general": "総合・低価格訴求型", "specialist": "専門・マニア特化型"}

fig, ax = plt.subplots(figsize=(14, 9.5), dpi=100)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)

# Quadrant guide lines
ax.axvline(5, color=GRID, linewidth=1, zorder=1)
ax.axhline(5, color=GRID, linewidth=1, zorder=1)

# Gridlines
ax.set_xticks(range(0, 11, 2))
ax.set_yticks(range(0, 11, 2))
ax.grid(True, color=GRID, linewidth=1, zorder=0)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.spines["left"].set_visible(True)
ax.spines["bottom"].set_visible(True)
ax.spines["left"].set_color(BASELINE)
ax.spines["bottom"].set_color(BASELINE)

plotted_groups = set()
for name, x, y, group, (dx, dy) in players:
    size = 420 if group == "own" else 260
    z = 5 if group == "own" else 3
    label = labels_group[group] if group not in plotted_groups else None
    plotted_groups.add(group)
    ax.scatter(
        [x], [y], s=size, color=colors[group], edgecolor=SURFACE, linewidth=2,
        zorder=z, label=label,
    )
    weight = "bold" if group == "own" else "normal"
    fontsize = 13 if group == "own" else 11.5
    ax.annotate(
        name, (x, y), xytext=(dx, dy), textcoords="offset fontsize",
        fontsize=fontsize, color=TEXT_PRIMARY, weight=weight, va="bottom", zorder=6,
        linespacing=1.3,
    )

ax.set_xlim(0, 10.6)
ax.set_ylim(0, 10.6)
ax.set_xlabel("品揃えの専門性 → 万人向け総合　⇔　マニア・ニッチ特化", fontsize=13, color=TEXT_SECONDARY, labelpad=14)
ax.set_ylabel("購入体験の利便性 → アナログ・書類手続き重視　⇔　モダン・スムーズ", fontsize=13, color=TEXT_SECONDARY, labelpad=14)
ax.tick_params(colors=MUTED, labelsize=10)

# Quadrant hints
quad_style = dict(fontsize=10.5, color=MUTED, style="italic")
ax.text(0.2, 10.2, "低価格・総合型 × デジタル利便性◎", ha="left", va="top", **quad_style)
ax.text(10.4, 10.2, "専門特化型 × デジタル利便性◎（空白ゾーン）", ha="right", va="top", **quad_style)
ax.text(0.2, 0.3, "総合型 × アナログ手続き中心", ha="left", va="bottom", **quad_style)
ax.text(10.4, 0.3, "専門特化型 × アナログ手続き中心", ha="right", va="bottom", **quad_style)

ax.set_title(
    "タバコEC市場 競合ポジショニングマップ（デイリータバコ／シガー領域）",
    fontsize=17, color=TEXT_PRIMARY, weight="bold", pad=34, loc="left",
)

legend = ax.legend(
    loc="lower center", bbox_to_anchor=(0.5, -0.2), ncol=3, frameon=False,
    fontsize=11.5, handletextpad=0.6, columnspacing=1.6,
)
for text in legend.get_texts():
    text.set_color(TEXT_SECONDARY)

fig.text(
    0.5, -0.01,
    "軸の値は公開情報（各社サイト・比較記事）に基づく定性評価。円の大きさはブリケオンラインを強調表示。",
    fontsize=10, color=MUTED, ha="center",
)

fig.tight_layout(rect=[0, 0.05, 1, 1])
fig.savefig("positioning_map.png", facecolor=SURFACE, bbox_inches="tight", dpi=140)
print("saved")
