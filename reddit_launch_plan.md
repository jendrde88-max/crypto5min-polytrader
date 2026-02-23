# Reddit & Community Launch Plan

> Copy-paste posts for each community. Tweak the angle per subreddit.
> **Post the r/SideProject one first**, then space the others out over a few days.

---

## 1. r/SideProject (503K members) — PRIMARY

**Rules summary:** "I built..." posts welcome. Story + value required. Purely promotional = removed. Some karma preferred.

### Title

```
I shipped my second Polymarket bot -- this one trades BTC direction every 5 minutes
```

### Body

```
Been building a follow up to my Polymarket copy trading bot.

This one is called Crypto5min PolyTrader. It generates UP or DOWN direction signals for BTC on a rolling 5 minute window, and it has a dashboard that makes it easy to see what it is doing.

What I focused on this time:

- Confidence gating so it only trades when the model is confident enough
- Risk caps and cooldowns so bet sizing does not run away
- Ops visibility so you can see the loops and actions in plain logs
- A terminal style log tab plus an Ops Events tab for debugging
- Optional Polymarket mode (advanced) with live and dry run
- Auto claim winnings on chain for normal wallets (not Safe or multisig wallets)

It is self hosted, Python plus Docker, runs on a cheap VPS.

I am looking for feedback on:

- Is the UI clear for someone who is not technical
- What would you want to see in the first 60 seconds after login
- Any red flags in the idea or the UX

If anyone wants to check it out, I will drop the Whop link in the first comment.

Not financial advice. Crypto is volatile and you can lose money.
```

### First comment (post immediately after)

```
Whop link: https://whop.com/polycryptotrader/crypto5min-polytrader-3a/

Happy to answer questions about how it works, and what I changed compared to the copy trading bot.
```

---

## 2. r/shamelessplug (52K members)

**Rules summary:** Almost anything allowed. No referral/affiliate links, no scams, no brand-new accounts. Active Reddit accounts required.

### Title

```
Crypto5min PolyTrader -- self hosted BTC direction bot with a dashboard
```

### Body

```
Built a self hosted bot that predicts BTC direction every 5 minutes and optionally trades it on Polymarket.

It runs in Docker on a cheap VPS and has a web dashboard with equity curve, trade log, ops events, and a terminal tab.

Key stuff:
- Confidence gating (does not trade on weak signals)
- Risk caps and cooldowns
- Paper mode so you can test before risking anything
- Auto claim winnings on chain

This is my second bot. First one was a Polymarket copy trading bot.

Whop link: https://whop.com/polycryptotrader/crypto5min-polytrader-3a/

Not financial advice. Ask me anything.
```

---

## 3. r/IMadeThis (19K members)

**Rules summary:** Anything personally made is welcome. Overly commercial content performs poorly. Personal stories do well.

### Title

```
I made a BTC direction bot with a real time dashboard
```

### Body

```
I have been building trading bots as a side project. My background is not even in coding (used to pour concrete), so a lot of this has been learning as I go.

This one watches BTC price, runs a prediction every 5 minutes, and optionally trades UP or DOWN on Polymarket. The dashboard shows everything live: equity curve, trades, ops events, and a terminal log.

What I am proud of:
- Confidence gating so it sits on its hands when signals are weak
- Risk caps so it does not blow up a small account
- Paper mode for testing without real money
- A clean dashboard that even I can read

It runs in Docker on a $5 VPS.

Happy to answer questions about how I built it or what I learned along the way.
```

---

## 4. r/buildinpublic (27K members)

**Rules summary:** Share progress, hurdles, successes, lessons. Must relate to "building in public." Posting solely for promotion gets removed.

### Title

```
Building in public: shipped my second trading bot, here is what I learned from the first one
```

### Body

```
A few months ago I launched a Polymarket copy trading bot. It worked, people bought it, but I wanted something that trades its own signals instead of copying someone else.

So I built Crypto5min PolyTrader. It predicts BTC direction every 5 minutes using a lightweight model, and optionally trades it on Polymarket.

What I changed compared to v1:
- Added a real dashboard with equity curve, trade log, and ops events
- Confidence gating so it does not trade on noise
- Risk caps and cooldowns
- Paper mode (dry run) so people can test safely
- Auto claim winnings on chain

Some things I learned the hard way:
- People want to see what the bot is doing, not just trust it
- Self hosted is harder to support but customers who want it prefer it
- Safety rails matter more than returns for convincing someone to try it

Still early. Looking for feedback from anyone building tools around prediction markets or crypto.

Whop link if curious: https://whop.com/polycryptotrader/crypto5min-polytrader-3a/
```

---

## 5. r/LaunchMyStartup (3K members, fast growing)

**Rules summary:** Launching projects is the entire purpose. Share what you built, get feedback. No gatekeeping.

### Title

```
Launching Crypto5min PolyTrader -- BTC direction bot with dashboard
```

### Body

```
Just shipped my second trading bot.

Crypto5min PolyTrader predicts BTC direction every 5 minutes and optionally trades it on Polymarket.

What it does:
- Runs a prediction model on BTC candles
- Shows live signal, equity curve, trade history on a web dashboard
- Safety rails: confidence gating, risk caps, cooldowns
- Paper mode for testing
- Auto claim winnings

Self hosted, Python + Docker, runs on a cheap VPS.

Whop link: https://whop.com/polycryptotrader/crypto5min-polytrader-3a/

Looking for honest feedback. What looks useful, what looks sketchy, what would make you click away.
```

---

## 6. r/RoastMyStartup (10-20K members)

**Rules summary:** Direct promotion is the entire purpose. Expect brutal honest feedback. Do not get defensive.

### Title

```
Roast my BTC direction bot with dashboard
```

### Body

```
Built a self hosted bot that predicts BTC UP or DOWN every 5 minutes and trades it on Polymarket.

Dashboard: https://whop.com/polycryptotrader/crypto5min-polytrader-3a/

What it does:
- Prediction model on BTC 5 min candles
- Live dashboard with equity curve, trades, ops events
- Confidence gating, risk caps, cooldowns, paper mode
- Auto claim winnings on chain
- Self hosted, Docker, runs on a VPS

Price: $100 for 3 months.

Roast away. I want to know what looks wrong, what is confusing, what would stop you from trying it.
```

---

## 7. r/Solopreneur (8K members)

**Rules summary:** One-person businesses only. Journey sharing, tool recs, feedback welcome. Excessive promo removed.

### Title

```
Solo dev shipping trading bots on Whop -- second product just launched
```

### Body

```
I have been building automated trading tools by myself. No team, no funding, just Docker and caffeine.

First product was a Polymarket copy trading bot ($29 one time). Sold some copies, learned a lot about what people actually want.

Second one just launched: Crypto5min PolyTrader. It predicts BTC direction every 5 minutes, shows everything on a live dashboard, and optionally trades on Polymarket. Self hosted, runs on a cheap VPS.

Would love to hear from other solopreneurs:
- How do you handle support when you are a one person operation
- Where do you draw the line between automation and manual intervention
- Any Whop sellers here with tips on listing optimization

Not financial advice, crypto is volatile, etc.
```

---

## Non-Reddit Communities

### Indie Hackers (indiehackers.com)
- Post in the **Product** or **Milestones** section
- Frame it as a build story with metrics if you have them
- Indie Hackers likes transparency: share revenue, user count, timeline
- Tone: casual, honest, builder-to-builder

### Hacker News -- Show HN (news.ycombinator.com)
- Format: `Show HN: Crypto5min PolyTrader -- BTC 5min direction bot with dashboard`
- Keep the description short and technical
- HN readers are skeptical of crypto and trading bots, so lead with the engineering and UX, not profits
- Link directly to the product or a demo, not a sales page if possible

### Product Hunt (producthunt.com)
- Takes more prep (need a good thumbnail, tagline, maker comment)
- Good for a splash of traffic on launch day
- Works best if you can get a few upvotes from friends early

### Twitter/X
- Post a thread about the build journey
- Tag #buildinpublic #indiehackers #polymarket
- Screenshot of the dashboard does well on Twitter

---

## Posting Schedule

| Day | Where | Angle |
|-----|-------|-------|
| Day 1 | r/SideProject | "I built" feedback request |
| Day 1 | r/shamelessplug | Direct link, straight pitch |
| Day 2 | r/buildinpublic | Journey + lessons learned |
| Day 2 | r/IMadeThis | Personal story (concrete to code) |
| Day 3 | r/LaunchMyStartup | Launch announcement |
| Day 3 | r/RoastMyStartup | "Roast me" feedback |
| Day 4 | r/Solopreneur | Solo dev journey |
| Day 5 | Indie Hackers | Product post with metrics |
| Day 7 | Hacker News Show HN | Technical build story |

> Space posts out. Do not carpet bomb everything on the same day.

---

## Likely Questions and Your Replies

**Q: Any proof it works?**
A: I am not making profit promises. The dashboard logs every trade and shows an equity curve. I also kept paper mode and dry run so people can test it safely first.

**Q: How does it avoid wrecking a small account?**
A: It has max USDC per trade, cooldowns, and confidence gating. You can also cap percent sizing unless you enable high risk modes.

**Q: Does it work with Safe or multisig?**
A: The on chain claim and withdraw features require a normal wallet where you control the private key. Safe and multisig are not supported for those actions.

**Q: Why Polymarket and not a real exchange?**
A: Polymarket has binary outcome markets (up or down) on short time windows. That is a cleaner signal than trying to trade spot or futures with leverage. The bot just needs to get direction right more often than not.

**Q: Why $100 for 3 months?**
A: That is less than most trading signal services charge per month. You get the full source, self hosted, no recurring until you renew. And there is a paper mode to test before going live.

**Q: Is this just ChatGPT trading?**
A: No. The model is a gradient boosted classifier trained on BTC candle features (momentum, volatility, trend). It is not an LLM.
