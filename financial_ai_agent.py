# Financial AI Agent - Phidata Style Multi-Agent System
# 3 Agents: 1) Price Agent 2) News Agent 3) Analyst Agent

import yfinance as yf
import datetime

print("=== Financial AI Agent - Phidata Style ===")
print("Agents: Price Agent + News Agent + Analyst Agent\n")

# AGENT 1: Price Agent - Stock ka data lana
def price_agent(symbol):
    print(f"[Price Agent] {symbol} ka data la raha hun...")
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="5d")
        if hist.empty:
            raise Exception("No data")
        current = hist['Close'].iloc[-1]
        prev = hist['Close'].iloc[-2]
        change = ((current - prev) / prev) * 100
        return {
            "symbol": symbol,
            "price": round(current, 2),
            "change": round(change, 2),
            "high_5d": round(hist['High'].max(), 2),
            "low_5d": round(hist['Low'].min(), 2),
        }
    except:
        # Agar internet na ho to demo data
        print("  -> Demo data use kar raha hun (internet slow hai)")
        return {"symbol": symbol, "price": 245.50, "change": 2.35, "high_5d": 250.10, "low_5d": 238.20}

# AGENT 2: News / Sentiment Agent - Market ka mood batana
def news_agent(symbol):
    print(f"[News Agent] {symbol} ki market news check kar raha hun...")
    # Simple rule-based sentiment - Real project me is jagah News API lagti hai
    headlines = [
        f"{symbol} shows strong buying interest from investors",
        f"Analysts positive on {symbol} after strong earnings",
        f"Market volatility affects {symbol} short-term"
    ]
    # Agar positive words zyada hon to sentiment Positive
    score = 72  # Demo sentiment score
    sentiment = "BULLISH 🟢" if score > 60 else "BEARISH 🔴"
    return {"headlines": headlines, "sentiment_score": score, "sentiment": sentiment}

# AGENT 3: Analyst Agent - Final Decision banana
def analyst_agent(price_data, news_data):
    print(f"[Analyst Agent] Dono agents ki report mila ke decision bana raha hun...\n")
    print("="*50)
    print(f"📊 STOCK REPORT: {price_data['symbol']}")
    print("="*50)
    print(f"Current Price: ${price_data['price']}")
    print(f"Change: {price_data['change']}%")
    print(f"5-Day High: ${price_data['high_5d']} | Low: ${price_data['low_5d']}")
    print(f"\n📰 Market Sentiment: {news_data['sentiment']} ({news_data['sentiment_score']}/100)")
    for h in news_data['headlines']:
        print(f" - {h}")

    # Final Recommendation Logic
    if price_data['change'] > 0 and news_data['sentiment_score'] > 60:
        rec = "BUY ✅ - Trend up hai aur sentiment positive hai"
    elif price_data['change'] < -2:
        rec = "SELL ❌ - Price gir raha hai, wait karo"
    else:
        rec = "HOLD ⏸️ - Market sideways hai, abhi wait karo"

    print(f"\n🤖 AI RECOMMENDATION: {rec}")
    print("="*50)
    return rec

# MAIN - User se poochna
if __name__ == "__main__":
    symbol = input("Stock Symbol daalo (e.g. AAPL, TSLA, GOOGL): ").upper().strip()
    if not symbol:
        symbol = "AAPL"
    
    price = price_agent(symbol)
    news = news_agent(symbol)
    analyst_agent(price, news)
    print("\n[DONE] Financial AI Agent Complete!")