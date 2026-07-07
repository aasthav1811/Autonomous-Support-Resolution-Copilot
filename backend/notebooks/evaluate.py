import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import time
import pandas as pd
from src.graph.workflow import get_workflow
from src.evaluation.evaluator import check_hallucination

# ── 50 Test Cases ──────────────────────────────────────────────────────────
TEST_CASES = [

    # ── BILLING (10) ──────────────────────────────────────────────────────
    {
        "ticket_id": "B001",
        "customer_email": "alice@test.com",
        "subject": "Charged twice this month",
        "body": "I see two identical charges of $29.99 on my bank statement for this month. Please refund one.",
        "expected_category": "billing",
        "expected_urgency": "high",
        "expected_sentiment": "negative",
        "expected_escalation": True,
    },
    {
        "ticket_id": "B002",
        "customer_email": "bob@test.com",
        "subject": "How do I update my credit card?",
        "body": "My old card expired. I need to add a new one before my next billing cycle. Where do I do this?",
        "expected_category": "billing",
        "expected_urgency": "low",
        "expected_sentiment": "neutral",
        "expected_escalation": False,
    },
    {
        "ticket_id": "B003",
        "customer_email": "carol@test.com",
        "subject": "FRAUD — unauthorized charge on my account",
        "body": "I never signed up for a premium plan but was charged $99. This is fraudulent. I want my money back NOW and my account cancelled.",
        "expected_category": "billing",
        "expected_urgency": "critical",
        "expected_sentiment": "angry",
        "expected_escalation": True,
    },
    {
        "ticket_id": "B004",
        "customer_email": "dan@test.com",
        "subject": "Refund request",
        "body": "I accidentally purchased the annual plan instead of monthly. I only realized 2 days ago. Can I get a refund and switch to monthly?",
        "expected_category": "billing",
        "expected_urgency": "medium",
        "expected_sentiment": "neutral",
        "expected_escalation": False,
    },
    {
        "ticket_id": "B005",
        "customer_email": "eva@test.com",
        "subject": "Do you accept PayPal?",
        "body": "I want to subscribe but I only have a PayPal account. Do you support PayPal payments?",
        "expected_category": "billing",
        "expected_urgency": "low",
        "expected_sentiment": "neutral",
        "expected_escalation": False,
    },
    {
        "ticket_id": "B006",
        "customer_email": "frank@test.com",
        "subject": "Charged after I cancelled",
        "body": "I cancelled my subscription on the 5th but was still charged on the 10th. This is unacceptable. I want a full refund.",
        "expected_category": "billing",
        "expected_urgency": "high",
        "expected_sentiment": "angry",
        "expected_escalation": True,
    },
    {
        "ticket_id": "B007",
        "customer_email": "grace@test.com",
        "subject": "Refund timeline question",
        "body": "I requested a refund 3 days ago. How long does it typically take to process? Just checking.",
        "expected_category": "billing",
        "expected_urgency": "low",
        "expected_sentiment": "neutral",
        "expected_escalation": False,
    },
    {
        "ticket_id": "B008",
        "customer_email": "henry@test.com",
        "subject": "Want to cancel subscription",
        "body": "I would like to cancel my monthly plan. Can you guide me through the cancellation process?",
        "expected_category": "billing",
        "expected_urgency": "low",
        "expected_sentiment": "neutral",
        "expected_escalation": False,
    },
    {
        "ticket_id": "B009",
        "customer_email": "irene@test.com",
        "subject": "Wrong amount charged",
        "body": "I'm on the $9.99 plan but was charged $19.99. This is a mistake. Please correct it immediately.",
        "expected_category": "billing",
        "expected_urgency": "high",
        "expected_sentiment": "negative",
        "expected_escalation": True,
    },
    {
        "ticket_id": "B010",
        "customer_email": "james@test.com",
        "subject": "Invoice for tax purposes",
        "body": "Could you please send me a detailed invoice for my subscription payments this year? I need it for my tax filing.",
        "expected_category": "billing",
        "expected_urgency": "low",
        "expected_sentiment": "neutral",
        "expected_escalation": False,
    },

    # ── TECHNICAL (10) ────────────────────────────────────────────────────
    {
        "ticket_id": "T001",
        "customer_email": "kate@test.com",
        "subject": "App crashes on launch",
        "body": "Every time I open the app it crashes immediately. I'm on Android 13, Pixel 7. Reinstalled twice already. Nothing works.",
        "expected_category": "technical",
        "expected_urgency": "high",
        "expected_sentiment": "negative",
        "expected_escalation": True,
    },
    {
        "ticket_id": "T002",
        "customer_email": "leo@test.com",
        "subject": "How do I clear the cache?",
        "body": "The app seems slow lately. Someone told me clearing the cache might help. How do I do that?",
        "expected_category": "technical",
        "expected_urgency": "low",
        "expected_sentiment": "neutral",
        "expected_escalation": False,
    },
    {
        "ticket_id": "T003",
        "customer_email": "mia@test.com",
        "subject": "This app is absolute garbage — crashes every 5 minutes",
        "body": "I cannot do any work. The app crashes constantly. I have a deadline tomorrow and this is costing me real money. Fix this NOW.",
        "expected_category": "technical",
        "expected_urgency": "critical",
        "expected_sentiment": "angry",
        "expected_escalation": True,
    },
    {
        "ticket_id": "T004",
        "customer_email": "noah@test.com",
        "subject": "Sync not working between devices",
        "body": "My data doesn't sync between my phone and laptop. Changes on one don't appear on the other. It was working fine last week.",
        "expected_category": "technical",
        "expected_urgency": "medium",
        "expected_sentiment": "neutral",
        "expected_escalation": False,
    },
    {
        "ticket_id": "T005",
        "customer_email": "olivia@test.com",
        "subject": "API returning 500 errors",
        "body": "Our integration has been getting 500 errors since this morning. We're blocked on a client deliverable. Need urgent help.",
        "expected_category": "technical",
        "expected_urgency": "critical",
        "expected_sentiment": "negative",
        "expected_escalation": True,
    },
    {
        "ticket_id": "T006",
        "customer_email": "peter@test.com",
        "subject": "What is the API rate limit?",
        "body": "I'm building an integration and need to know the API rate limits for standard plans. Couldn't find it in the docs.",
        "expected_category": "technical",
        "expected_urgency": "low",
        "expected_sentiment": "neutral",
        "expected_escalation": False,
    },
    {
        "ticket_id": "T007",
        "customer_email": "quinn@test.com",
        "subject": "Can't update the app on iPhone",
        "body": "The App Store shows an update available but when I tap Update nothing happens. iPhone 13, iOS 16.",
        "expected_category": "technical",
        "expected_urgency": "medium",
        "expected_sentiment": "neutral",
        "expected_escalation": False,
    },
    {
        "ticket_id": "T008",
        "customer_email": "rachel@test.com",
        "subject": "Login page not loading",
        "body": "The login page just shows a blank white screen on Chrome. Tried Firefox too, same issue. Can't access my account at all.",
        "expected_category": "technical",
        "expected_urgency": "high",
        "expected_sentiment": "negative",
        "expected_escalation": True,
    },
    {
        "ticket_id": "T009",
        "customer_email": "sam@test.com",
        "subject": "App is slower than before",
        "body": "After the last update the app feels noticeably slower. Everything takes a few extra seconds. Not a dealbreaker but worth reporting.",
        "expected_category": "technical",
        "expected_urgency": "low",
        "expected_sentiment": "neutral",
        "expected_escalation": False,
    },
    {
        "ticket_id": "T010",
        "customer_email": "tina@test.com",
        "subject": "Data disappeared after update",
        "body": "I updated the app this morning and now all my saved data is gone. Months of work. I am devastated. Please recover it.",
        "expected_category": "technical",
        "expected_urgency": "critical",
        "expected_sentiment": "angry",
        "expected_escalation": True,
    },

    # ── ACCOUNT (10) ──────────────────────────────────────────────────────
    {
        "ticket_id": "A001",
        "customer_email": "uma@test.com",
        "subject": "Can't log in — locked out",
        "body": "I've been locked out of my account after too many failed attempts. I have an important meeting in an hour and need access urgently.",
        "expected_category": "account",
        "expected_urgency": "critical",
        "expected_sentiment": "negative",
        "expected_escalation": True,
    },
    {
        "ticket_id": "A002",
        "customer_email": "victor@test.com",
        "subject": "How to change my username",
        "body": "I'd like to update my username. Is this possible and if so how do I do it?",
        "expected_category": "account",
        "expected_urgency": "low",
        "expected_sentiment": "neutral",
        "expected_escalation": False,
    },
    {
        "ticket_id": "A003",
        "customer_email": "wendy@test.com",
        "subject": "Delete my account permanently",
        "body": "I want to permanently delete my account and all associated data. Please process this as soon as possible.",
        "expected_category": "account",
        "expected_urgency": "medium",
        "expected_sentiment": "neutral",
        "expected_escalation": False,
    },
    {
        "ticket_id": "A004",
        "customer_email": "xavier@test.com",
        "subject": "How to set up 2FA",
        "body": "I want to make my account more secure. Can you walk me through setting up two-factor authentication?",
        "expected_category": "account",
        "expected_urgency": "low",
        "expected_sentiment": "positive",
        "expected_escalation": False,
    },
    {
        "ticket_id": "A005",
        "customer_email": "yara@test.com",
        "subject": "Someone hacked my account",
        "body": "I received a login notification from a country I've never been to. Someone has accessed my account without my permission. Help me immediately.",
        "expected_category": "account",
        "expected_urgency": "critical",
        "expected_sentiment": "angry",
        "expected_escalation": True,
    },
    {
        "ticket_id": "A006",
        "customer_email": "zach@test.com",
        "subject": "Change email address",
        "body": "I recently changed jobs and want to update my account email to my personal address. How do I do this?",
        "expected_category": "account",
        "expected_urgency": "low",
        "expected_sentiment": "neutral",
        "expected_escalation": False,
    },
    {
        "ticket_id": "A007",
        "customer_email": "amy@test.com",
        "subject": "Password reset email not arriving",
        "body": "I requested a password reset 30 minutes ago but haven't received the email. Checked spam folder too. Still nothing.",
        "expected_category": "account",
        "expected_urgency": "medium",
        "expected_sentiment": "neutral",
        "expected_escalation": False,
    },
    {
        "ticket_id": "A008",
        "customer_email": "ben@test.com",
        "subject": "Transfer account to new email",
        "body": "My old email provider is shutting down. I need to transfer my entire account to a new email address urgently.",
        "expected_category": "account",
        "expected_urgency": "high",
        "expected_sentiment": "negative",
        "expected_escalation": True,
    },
    {
        "ticket_id": "A009",
        "customer_email": "claire@test.com",
        "subject": "How many times can I change username?",
        "body": "I changed my username last week. I'd like to change it again. Is there a limit on how often I can do this?",
        "expected_category": "account",
        "expected_urgency": "low",
        "expected_sentiment": "neutral",
        "expected_escalation": False,
    },
    {
        "ticket_id": "A010",
        "customer_email": "david@test.com",
        "subject": "Disabled account — was not warned",
        "body": "My account was disabled without any warning or explanation. I have not violated any terms. This is completely unfair.",
        "expected_category": "account",
        "expected_urgency": "high",
        "expected_sentiment": "angry",
        "expected_escalation": True,
    },

    # ── SHIPPING (10) ─────────────────────────────────────────────────────
    {
        "ticket_id": "S001",
        "customer_email": "emily@test.com",
        "subject": "Order not arrived — 10 days late",
        "body": "My order #78432 was due 10 days ago. Tracking shows it left the warehouse but nothing since. Where is it?",
        "expected_category": "shipping",
        "expected_urgency": "high",
        "expected_sentiment": "negative",
        "expected_escalation": True,
    },
    {
        "ticket_id": "S002",
        "customer_email": "finn@test.com",
        "subject": "Received wrong item",
        "body": "I ordered a blue medium t-shirt but received a red large. Please send the correct item.",
        "expected_category": "shipping",
        "expected_urgency": "medium",
        "expected_sentiment": "negative",
        "expected_escalation": False,
    },
    {
        "ticket_id": "S003",
        "customer_email": "gina@test.com",
        "subject": "How long does shipping to Canada take?",
        "body": "I'm about to place an order and wondering how long standard shipping takes to Ontario, Canada.",
        "expected_category": "shipping",
        "expected_urgency": "low",
        "expected_sentiment": "neutral",
        "expected_escalation": False,
    },
    {
        "ticket_id": "S004",
        "customer_email": "hank@test.com",
        "subject": "Package says delivered but not here",
        "body": "Tracking shows my package was delivered yesterday but it's not at my door or with any neighbor. It's a $200 item.",
        "expected_category": "shipping",
        "expected_urgency": "high",
        "expected_sentiment": "negative",
        "expected_escalation": True,
    },
    {
        "ticket_id": "S005",
        "customer_email": "iris@test.com",
        "subject": "Can I change my delivery address?",
        "body": "I just placed an order 20 minutes ago and realized I entered the wrong address. Can I change it before it ships?",
        "expected_category": "shipping",
        "expected_urgency": "high",
        "expected_sentiment": "neutral",
        "expected_escalation": True,
    },
    {
        "ticket_id": "S006",
        "customer_email": "jake@test.com",
        "subject": "Item arrived damaged",
        "body": "My order arrived today but the product inside was broken. The box looked fine but the item itself is cracked.",
        "expected_category": "shipping",
        "expected_urgency": "high",
        "expected_sentiment": "negative",
        "expected_escalation": True,
    },
    {
        "ticket_id": "S007",
        "customer_email": "karen@test.com",
        "subject": "Tracking number not working",
        "body": "The tracking number in my confirmation email doesn't show any results on the carrier website. Order placed 3 days ago.",
        "expected_category": "shipping",
        "expected_urgency": "medium",
        "expected_sentiment": "neutral",
        "expected_escalation": False,
    },
    {
        "ticket_id": "S008",
        "customer_email": "liam@test.com",
        "subject": "Do you ship to Australia?",
        "body": "I'm based in Melbourne, Australia. Do you ship there and if so what are the approximate delivery times?",
        "expected_category": "shipping",
        "expected_urgency": "low",
        "expected_sentiment": "neutral",
        "expected_escalation": False,
    },
    {
        "ticket_id": "S009",
        "customer_email": "maya@test.com",
        "subject": "Refund for lost package",
        "body": "My package has been lost for 3 weeks. The carrier confirmed it's lost. I want a full refund or replacement immediately.",
        "expected_category": "shipping",
        "expected_urgency": "critical",
        "expected_sentiment": "angry",
        "expected_escalation": True,
    },
    {
        "ticket_id": "S010",
        "customer_email": "nick@test.com",
        "subject": "Express shipping upgrade possible?",
        "body": "I placed an order yesterday with standard shipping. Is it possible to upgrade to express before it dispatches?",
        "expected_category": "shipping",
        "expected_urgency": "medium",
        "expected_sentiment": "neutral",
        "expected_escalation": False,
    },

    # ── GENERAL (10) ──────────────────────────────────────────────────────
    {
        "ticket_id": "G001",
        "customer_email": "olivia@test.com",
        "subject": "Dark mode feature request",
        "body": "The app is great but I'd really love a dark mode option. Any plans to add this? My eyes would thank you.",
        "expected_category": "general",
        "expected_urgency": "low",
        "expected_sentiment": "positive",
        "expected_escalation": False,
    },
    {
        "ticket_id": "G002",
        "customer_email": "paul@test.com",
        "subject": "Great product — just a suggestion",
        "body": "Love the product overall! One small suggestion — it would be great to have keyboard shortcuts for the most common actions.",
        "expected_category": "general",
        "expected_urgency": "low",
        "expected_sentiment": "positive",
        "expected_escalation": False,
    },
    {
        "ticket_id": "G003",
        "customer_email": "queen@test.com",
        "subject": "Is there a mobile app?",
        "body": "I've been using the web version. Is there an iOS or Android app available? Couldn't find it in the App Store.",
        "expected_category": "general",
        "expected_urgency": "low",
        "expected_sentiment": "neutral",
        "expected_escalation": False,
    },
    {
        "ticket_id": "G004",
        "customer_email": "ryan@test.com",
        "subject": "When is the next update coming?",
        "body": "Really enjoying the product. Just curious — is there a public roadmap or timeline for upcoming features?",
        "expected_category": "general",
        "expected_urgency": "low",
        "expected_sentiment": "positive",
        "expected_escalation": False,
    },
    {
        "ticket_id": "G005",
        "customer_email": "sara@test.com",
        "subject": "Accessibility features needed",
        "body": "I have low vision and the current font size options are not enough. Are there plans to improve accessibility features?",
        "expected_category": "general",
        "expected_urgency": "medium",
        "expected_sentiment": "neutral",
        "expected_escalation": False,
    },
    {
        "ticket_id": "G006",
        "customer_email": "tom@test.com",
        "subject": "Is my data safe?",
        "body": "I store sensitive work files on your platform. Can you tell me about your data encryption and security practices?",
        "expected_category": "general",
        "expected_urgency": "medium",
        "expected_sentiment": "neutral",
        "expected_escalation": False,
    },
    {
        "ticket_id": "G007",
        "customer_email": "uma@test.com",
        "subject": "Partnership inquiry",
        "body": "I run a small agency and would love to discuss a potential partnership or reseller arrangement. Who should I contact?",
        "expected_category": "general",
        "expected_urgency": "low",
        "expected_sentiment": "positive",
        "expected_escalation": False,
    },
    {
        "ticket_id": "G008",
        "customer_email": "vera@test.com",
        "subject": "Your product is terrible",
        "body": "I've been a customer for 6 months and the product keeps getting worse with every update. You're losing customers because of this.",
        "expected_category": "general",
        "expected_urgency": "medium",
        "expected_sentiment": "angry",
        "expected_escalation": True,
    },
    {
        "ticket_id": "G009",
        "customer_email": "will@test.com",
        "subject": "Student discount available?",
        "body": "I'm a university student on a tight budget. Do you offer any student discounts or educational pricing?",
        "expected_category": "general",
        "expected_urgency": "low",
        "expected_sentiment": "neutral",
        "expected_escalation": False,
    },
    {
        "ticket_id": "G010",
        "customer_email": "xena@test.com",
        "subject": "GDPR data request",
        "body": "Under GDPR I'd like to request a full export of all personal data you hold about me. Please process this within the legal timeframe.",
        "expected_category": "general",
        "expected_urgency": "medium",
        "expected_sentiment": "neutral",
        "expected_escalation": False,
    },
]

# ── Evaluation Runner ──────────────────────────────────────────────────────
def run_evaluation():
    print("\n" + "="*60)
    print("  SUPPORT COPILOT — EVALUATION REPORT")
    print("="*60)
    print(f"  Running {len(TEST_CASES)} test cases...\n")

    wf = get_workflow()
    results = []

    for i, tc in enumerate(TEST_CASES):
        print(f"  [{i+1:02d}/{len(TEST_CASES)}] {tc['ticket_id']} — {tc['subject'][:45]}...")
        start = time.time()

        try:
            output = wf.invoke({
                "ticket_id": tc["ticket_id"],
                "customer_email": tc["customer_email"],
                "subject": tc["subject"],
                "body": tc["body"],
                "agent_trace": [],
            })

            latency = round(time.time() - start, 2)
            ctx = "\n".join(d["content"] for d in output.get("retrieved_docs", []))
            hallu = check_hallucination(output.get("draft_response", ""), ctx)

            cat_correct   = output.get("category")   == tc["expected_category"]
            urg_correct   = output.get("urgency")     == tc["expected_urgency"]
            sent_correct  = output.get("sentiment")   == tc["expected_sentiment"]
            esc_correct   = output.get("needs_escalation") == tc["expected_escalation"]

            results.append({
                "id":                tc["ticket_id"],
                "subject":           tc["subject"][:40],
                "exp_cat":           tc["expected_category"],
                "pred_cat":          output.get("category"),
                "cat_correct":       cat_correct,
                "exp_urg":           tc["expected_urgency"],
                "pred_urg":          output.get("urgency"),
                "urg_correct":       urg_correct,
                "exp_sent":          tc["expected_sentiment"],
                "pred_sent":         output.get("sentiment"),
                "sent_correct":      sent_correct,
                "exp_esc":           tc["expected_escalation"],
                "pred_esc":          output.get("needs_escalation"),
                "esc_correct":       esc_correct,
                "hallucinated":      hallu.get("hallucinated", False),
                "hallu_explanation": hallu.get("explanation", ""),
                "latency_s":         latency,
                "docs_retrieved":    len(output.get("retrieved_docs", [])),
                "draft_length":      len(output.get("draft_response", "")),
                "all_correct":       all([cat_correct, urg_correct, sent_correct, esc_correct]),
                "error":             None,
            })

        except Exception as e:
            results.append({
                "id": tc["ticket_id"], "subject": tc["subject"][:40],
                "error": str(e), "all_correct": False,
                "cat_correct": False, "urg_correct": False,
                "sent_correct": False, "esc_correct": False,
                "hallucinated": False, "latency_s": 0,
            })
            print(f"       ❌ ERROR: {e}")

    # ── Print Report ──────────────────────────────────────────────────────
    df = pd.DataFrame(results)
    n  = len(df)
    ok = df[df["error"].isna()] if "error" in df.columns else df

    print("\n" + "="*60)
    print("  ACCURACY METRICS")
    print("="*60)

    cat_acc  = ok["cat_correct"].mean()
    urg_acc  = ok["urg_correct"].mean()
    sent_acc = ok["sent_correct"].mean()
    esc_acc  = ok["esc_correct"].mean()
    all_acc  = ok["all_correct"].mean()
    hallu_rate = ok["hallucinated"].mean()
    avg_lat  = ok["latency_s"].mean()
    p95_lat  = ok["latency_s"].quantile(0.95)

    print(f"  Category classification:   {cat_acc:.0%}  ({ok['cat_correct'].sum()}/{len(ok)} correct)")
    print(f"  Urgency classification:    {urg_acc:.0%}  ({ok['urg_correct'].sum()}/{len(ok)} correct)")
    print(f"  Sentiment classification:  {sent_acc:.0%}  ({ok['sent_correct'].sum()}/{len(ok)} correct)")
    print(f"  Escalation logic:          {esc_acc:.0%}  ({ok['esc_correct'].sum()}/{len(ok)} correct)")
    print(f"  All-4 correct (strict):    {all_acc:.0%}  ({ok['all_correct'].sum()}/{len(ok)} tickets)")
    print(f"\n  Hallucination rate:        {hallu_rate:.0%}  ({ok['hallucinated'].sum()} flagged)")
    print(f"  Avg latency:               {avg_lat:.1f}s")
    print(f"  p95 latency:               {p95_lat:.1f}s")

    print("\n" + "="*60)
    print("  ACCURACY BY CATEGORY")
    print("="*60)
    for cat in ["billing", "technical", "account", "shipping", "general"]:
        subset = ok[ok["exp_cat"] == cat]
        if len(subset) == 0:
            continue
        c = subset["cat_correct"].mean()
        u = subset["urg_correct"].mean()
        s = subset["sent_correct"].mean()
        e = subset["esc_correct"].mean()
        print(f"  {cat.upper():<12}  cat={c:.0%}  urg={u:.0%}  sent={s:.0%}  esc={e:.0%}  (n={len(subset)})")

    print("\n" + "="*60)
    print("  FAILURES — WHERE IT GOT IT WRONG")
    print("="*60)
    failures = ok[~ok["all_correct"]]
    if len(failures) == 0:
        print("  ✅ No failures — perfect score!")
    else:
        for _, row in failures.iterrows():
            wrongs = []
            if not row["cat_correct"]:
                wrongs.append(f"cat: expected={row['exp_cat']} got={row['pred_cat']}")
            if not row["urg_correct"]:
                wrongs.append(f"urg: expected={row['exp_urg']} got={row['pred_urg']}")
            if not row["sent_correct"]:
                wrongs.append(f"sent: expected={row['exp_sent']} got={row['pred_sent']}")
            if not row["esc_correct"]:
                wrongs.append(f"esc: expected={row['exp_esc']} got={row['pred_esc']}")
            print(f"  {row['id']}: {' | '.join(wrongs)}")
            print(f"       \"{row['subject']}\"")

    print("\n" + "="*60)
    print("  HALLUCINATIONS DETECTED")
    print("="*60)
    hallus = ok[ok["hallucinated"] == True]
    if len(hallus) == 0:
        print("  ✅ No hallucinations detected")
    else:
        for _, row in hallus.iterrows():
            print(f"  {row['id']}: {row.get('hallu_explanation', '')[:80]}")

    # ── Save to CSV ───────────────────────────────────────────────────────
    out_path = "notebooks/evaluation_results.csv"
    df.to_csv(out_path, index=False)
    print(f"\n  📄 Full results saved to: {out_path}")
    print("="*60 + "\n")

    return df


if __name__ == "__main__":
    run_evaluation()