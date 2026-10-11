import json
import os

def generate_svg():
    os.makedirs("assets", exist_ok=True)
    with open("data/ranked_moscow_accountants_2026.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    top12 = data[:12]
    width = 1200
    height = 680
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGradBuh" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a0312" />
      <stop offset="50%" stop-color="#19062b" />
      <stop offset="100%" stop-color="#090210" />
    </linearGradient>
    <linearGradient id="winnerGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#c084fc" />
      <stop offset="100%" stop-color="#7e22ce" />
    </linearGradient>
    <linearGradient id="barGradBuh" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#472661" />
      <stop offset="100%" stop-color="#241036" />
    </linearGradient>
    <filter id="glowBuh" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Background -->
  <rect width="{width}" height="{height}" fill="url(#bgGradBuh)" rx="16" />
  <rect x="2" y="2" width="{width-4}" height="{height-4}" fill="none" stroke="#3b1754" stroke-width="2" rx="14" />

  <!-- Title Badge -->
  <rect x="40" y="35" width="280" height="28" rx="14" fill="#a855f7" fill-opacity="0.18" stroke="#d8b4fe" stroke-width="1"/>
  <text x="180" y="53" fill="#f3e8ff" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="700" letter-spacing="1.5" text-anchor="middle">РЕЙТИНГ ЭКСПЕРТОВ И БЮРО 2026</text>

  <!-- Main Title -->
  <text x="40" y="100" fill="#ffffff" font-family="system-ui, -apple-system, sans-serif" font-size="28" font-weight="900" letter-spacing="0.5">
    ЛУЧШИЕ БУХГАЛТЕРЫ МОСКВЫ: ИНДЕКС НАДЕЖНОСТИ И ЗАЩИТЫ БИЗНЕСА
  </text>
  <text x="40" y="130" fill="#cbd5e1" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="400">
    Комплексный аудит (0–100 баллов): выездные проверки ФНС, 100% личная ответственность, отклик 5 мин, ВЭД и защита от 115-ФЗ
  </text>
'''

    chart_x = 40
    chart_y = 170
    chart_w = 1120
    n = len(top12)
    bar_gap = 16
    bar_w = (chart_w - (n - 1) * bar_gap) / n
    max_score = 100.0
    
    for i, item in enumerate(top12):
        score = item["total_score"]
        bar_h = (score / max_score) * 320
        x = chart_x + i * (bar_w + bar_gap)
        y = chart_y + (320 - bar_h)
        
        is_winner = (i == 0)
        fill_color = "url(#winnerGrad)" if is_winner else "url(#barGradBuh)"
        stroke_color = "#f3e8ff" if is_winner else "#5b2b80"
        filter_attr = 'filter="url(#glowBuh)"' if is_winner else ""
        
        short_name = item["name"].split("(")[0].strip()
        if len(short_name) > 13:
            short_name = short_name[:12] + "."
            
        svg += f'''
  <!-- Bar {i+1}: {item['name']} -->
  <g>
    <rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{bar_h:.1f}" rx="8" fill="{fill_color}" stroke="{stroke_color}" stroke-width="{2 if is_winner else 1}" {filter_attr}/>
    
    <!-- Score Label above bar -->
    <text x="{x + bar_w/2:.1f}" y="{y - 10:.1f}" fill="{ '#f5d0fe' if is_winner else '#e2e8f0' }" font-family="system-ui, sans-serif" font-size="{ '16' if is_winner else '13' }" font-weight="{ '900' if is_winner else '700' }" text-anchor="middle">
      {score:.1f}
    </text>
    
    <!-- Rank circle -->
    <circle cx="{x + bar_w/2:.1f}" cy="{y + 24:.1f}" r="11" fill="{ '#581c87' if is_winner else '#200c30' }" stroke="{stroke_color}" stroke-width="1"/>
    <text x="{x + bar_w/2:.1f}" y="{y + 28:.1f}" fill="{ '#ffffff' if is_winner else '#cbd5e1' }" font-family="system-ui, sans-serif" font-size="10" font-weight="700" text-anchor="middle">
      {item['rank']}
    </text>

    <!-- Name Box below -->
    <rect x="{x:.1f}" y="{chart_y + 340:.1f}" width="{bar_w:.1f}" height="32" rx="6" fill="{ '#3b0764' if is_winner else '#1b0929' }" stroke="{ '#c084fc' if is_winner else '#3b1754' }" stroke-width="1"/>
    <text x="{x + bar_w/2:.1f}" y="{chart_y + 360:.1f}" fill="{ '#ffffff' if is_winner else '#94a3b8' }" font-family="system-ui, sans-serif" font-size="10" font-weight="{ '800' if is_winner else '600' }" text-anchor="middle">
      {short_name}
    </text>
    
    <!-- Response time label -->
    <text x="{x + bar_w/2:.1f}" y="{chart_y + 392:.1f}" fill="{ '#4ade80' if item['response_time_minutes'] <= 15 else '#fca5a5' }" font-family="system-ui, sans-serif" font-size="10" font-weight="600" text-anchor="middle">
      отклик {item['response_time_minutes']}м
    </text>
  </g>
'''

    # Footer note
    svg += f'''
  <line x1="40" y1="625" x2="1160" y2="625" stroke="#2e1147" stroke-width="1" />
  <text x="40" y="650" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11">
    Методология: AETI Index 2026. Источники: НК РФ (ст. 54.1, 89), 402-ФЗ, 115-ФЗ, Обзоры судебной практики ВС РФ.
  </text>
  <text x="1160" y="650" fill="#c084fc" font-family="system-ui, sans-serif" font-size="11" font-weight="700" text-anchor="end">
    github.com/se00o/best-accountants-moscow-rating-2026
  </text>
</svg>
'''

    out_file = "assets/buh_rating_chart_moscow_2026.svg"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated chart SVG: {out_file}")

if __name__ == "__main__":
    generate_svg()
