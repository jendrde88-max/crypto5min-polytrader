X ARTICLE — PASTE DIRECTLY INTO X ARTICLES EDITOR
====================================================
Title field: I Used to Pour Concrete. Now I Build Trading Bots.
Cover image: Open article_cover.html in browser, screenshot the 1200x480 box
====================================================
COPY EVERYTHING BELOW THIS LINE INTO THE BODY:
====================================================

This is not a flex. This is what happens when you get bored enough to learn Python.


How it started

Two years ago I was mixing concrete for a living. Nothing wrong with that, it paid the bills. But I kept watching crypto Twitter and prediction markets and thinking "someone is making money off this and it is not me."

I had zero coding experience. I did not know what an API was. I did not know what Docker was. I barely knew what a terminal was.

But I had time after work and a cheap laptop, and I figured the worst that could happen was I would learn something useless.


The first bot

I started by building a copy trading bot for Polymarket. The idea was simple: find a wallet that is consistently winning, and mirror its trades automatically.

It worked. Not perfectly, but it worked. People bought it. I listed it on Whop for $29 and sold enough copies to tell myself this was a real thing.

But I kept thinking about the same problem: I was copying someone else's decisions. If they stopped trading, or changed strategy, or just had a bad week, my bot had nothing.

I wanted something that could think for itself.


What I actually built

Crypto5min PolyTrader is the second bot. It does not copy anyone. It looks at BTC price data every 5 minutes, runs it through a prediction model, and says "I think BTC is going UP" or "I think BTC is going DOWN."

Then, if you turn on the advanced mode, it places that bet on Polymarket automatically.

Here is what I spent most of my time on (and it was not the model):

The dashboard. People do not trust a bot they cannot see. The first bot had basically no UI. People would message me asking "is it even running?" So this time I built a real dashboard. You can see the live signal, the equity curve, every trade, every ops event, and even the raw terminal logs.

Safety rails. The model is not always right. Nobody's is. So I built confidence gating (it will not trade if the signal is weak), risk caps (it limits how much USDC goes into any single trade), and cooldowns (it will not spam trades back to back). There is also a max loss circuit breaker.

Paper mode. Before you risk a single dollar, you can run the whole thing in paper mode. It does everything the live bot does except it does not actually place trades. You can watch it for a day or a week and decide if you trust it.

Auto claim. When you win a trade on Polymarket, the winnings sit on chain until you claim them. The bot does that automatically. One less thing to think about.


What the model actually is

People always ask "is this just ChatGPT trading?" No.

It is a gradient boosted classifier trained on BTC candle features. Momentum, volatility, trend. It is not trying to predict the price. It is trying to predict the direction. Up or down. That is it.

Is it right every time? No. Is it right more often than a coin flip? In testing, yes. But testing is not the same as live, which is why paper mode exists and why I do not make profit promises anywhere.


The tech (for people who care)

Python
Docker (one command to deploy)
FastAPI for the web dashboard
HTMX for live updates (no React, no webpack, no build step)
Coinbase API for candle data
Polymarket CLOB API for trade execution
Runs on any $5 VPS

The whole thing ships as a ZIP. You unzip it, run Docker Compose, open the setup wizard in your browser, paste your keys, and it starts running. If you have ever installed anything with Docker before, this takes maybe 10 minutes.


What I learned building this

Transparency beats performance. People would rather see a bot that is honest about what it is doing than one that claims 90% accuracy with no receipts. The dashboard logs everything. Every signal, every trade, every error. Nothing is hidden.

Safety beats returns. Nobody cares about your backtest if they lose money in the first hour. The confidence gating and risk caps are what make people comfortable enough to actually try it. Without those, this would just be another sketchy trading bot.

Self hosting is harder to support but builds trust. When people run the bot on their own machine, they know their keys never leave their server. That matters in crypto. It means more support tickets for me, but the people who want self hosted really want self hosted.

Start with paper mode. Every single customer who had a bad experience with the first bot skipped the testing phase. Now paper mode is the default. You have to actively choose to go live.


The part where I am honest

This bot is not going to make you rich. If anyone tells you their trading bot will make you rich, they are lying to you.

What it does is give you a systematic, rules based way to trade short term BTC direction on Polymarket. It removes emotion from the process. It logs everything so you can review what happened. And it has enough guardrails that a bad streak does not wipe you out.

Crypto is volatile. You can lose money. The model can be wrong. I am not a financial advisor and this is not financial advice.


Try it

If any of this sounds interesting, you can check it out here:

https://whop.com/polycryptotrader/crypto5min-polytrader-3a/

Start in paper mode. Watch it for a few days. Look at the dashboard. Read the logs. Then decide if it is worth turning on.

If you have questions, I am around. I built the whole thing myself and I answer every message.

Not financial advice. Past performance does not guarantee future results. Trading involves risk and you can lose money.


====================================================
FORMATTING GUIDE (apply in X editor after pasting):
====================================================
1. Select each section heading and change from "Body" to a heading size using the dropdown
   Headings: How it started / The first bot / What I actually built / What the model actually is / The tech (for people who care) / What I learned building this / The part where I am honest / Try it

2. Bold these phrases (select text, click B or Ctrl+B):
   - "The dashboard." (first two words of that paragraph)
   - "Safety rails." (first two words)
   - "Paper mode." (first two words)
   - "Auto claim." (first two words)
   - "Transparency beats performance." (first three words)
   - "Safety beats returns." (first three words)
   - "Self hosting is harder to support but builds trust." (whole intro phrase)
   - "Start with paper mode." (first four words)

3. The tech list: select all 7 lines and click the bulleted list button

4. The Whop link will auto-linkify when you paste it

5. Last line (disclaimer): select it and click Italic
