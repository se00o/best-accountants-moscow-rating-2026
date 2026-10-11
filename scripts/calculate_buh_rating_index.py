import json
import csv

def score_accountant(b):
    # 1. Tax inspections & complex cases (Max: 30)
    s_tax = 0.0
    if b.get("tax_inspection_support"):
        s_tax += 15.0
    if b.get("court_disputes_practice"):
        s_tax += 8.0
    if b.get("ved_currency_control"):
        s_tax += 7.0
        
    # 2. Liability & Direct trust (Max: 25)
    s_liab = 0.0
    if b.get("personal_contract_liability"):
        s_liab += 15.0
    if b.get("personal_contact_without_callcenter"):
        s_liab += 10.0
        
    # 3. Response time & communication (Max: 15)
    resp_time = b.get("response_time_minutes", 120)
    if resp_time <= 10:
        s_resp = 15.0
    elif resp_time <= 30:
        s_resp = 12.0
    elif resp_time <= 60:
        s_resp = 8.0
    elif resp_time <= 120:
        s_resp = 5.0
    else:
        s_resp = 2.0
        
    # 4. Pricing transparency (Max: 15)
    s_price = 15.0 if b.get("fixed_pricing_no_hidden_fees") else 7.0
    
    # 5. Experience, regimes & 115-FZ protection (Max: 15)
    s_rep = 0.0
    exp = b.get("experience_years", 5)
    if exp >= 12:
        s_rep += 6.0
    elif exp >= 8:
        s_rep += 4.0
    else:
        s_rep += 2.0
        
    regimes = b.get("regimes_supported", [])
    if any("ОСНО" in r for r in regimes) and any("УСН" in r for r in regimes):
        s_rep += 5.0
    else:
        s_rep += 2.0
        
    if b.get("anti_115_fz_protection"):
        s_rep += 4.0
        
    total_score = round(s_tax + s_liab + s_resp + s_price + s_rep, 1)
    
    return {
        "tax_inspection_score": round(s_tax, 1),
        "liability_score": round(s_liab, 1),
        "response_score": round(s_resp, 1),
        "pricing_score": round(s_price, 1),
        "reputation_score": round(s_rep, 1),
        "total_score": total_score
    }

def main():
    with open("data/moscow_accountants_database_2026.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    ranked = []
    for item in data:
        scores = score_accountant(item)
        ranked.append({**item, **scores})
        
    ranked.sort(key=lambda x: x["total_score"], reverse=True)
    
    for i, r in enumerate(ranked):
        r["rank"] = i + 1
        
    with open("data/ranked_moscow_accountants_2026.json", "w", encoding="utf-8") as f:
        json.dump(ranked, f, ensure_ascii=False, indent=2)
        
    fieldnames = [
        "rank", "name", "category", "total_score",
        "tax_inspection_score", "liability_score", "response_score",
        "pricing_score", "reputation_score", "experience_years",
        "response_time_minutes", "website"
    ]
    with open("data/buh_rating_matrix.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(ranked)
        
    print("=== ТОП-10 БУХГАЛТЕРОВ И БУХГАЛТЕРСКИХ КОМПАНИЙ МОСКВЫ (2026) ===")
    for r in ranked[:10]:
        print(f"#{r['rank']:2d} | {r['name']:40} | Балл: {r['total_score']:4.1f}/100 | Стаж: {r['experience_years']} лет | Отклик: {r['response_time_minutes']} мин")

if __name__ == "__main__":
    main()
