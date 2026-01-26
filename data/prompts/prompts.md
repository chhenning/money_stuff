# Text Chunking

Ask chatgpt to generate system and user prompts

```
```

# Questions per chunk

Ask chatgpt to generate system and user prompts:

```
Can you generate a markdown system prompt (as a Python string) for the following workflow.

- You are given a list of text chunks and for each you need to create relevant questions.
- create one or more questions that accurately reflect the key points, or information contained within a chunk
- this is for my money stuff newsletter project include some relevant example of how

here is an example of the input:

{
  "chunks": [
    {
      "id": 1,
      "chunk": "# AI rollup\n\nPeople have been worried for a while about private equity buying up every company and coming to dominate the economy. “Private equity,” in this worry, tends to mean specifically the large private-equity firms that have their roots in doing leveraged buyouts of mature cash-flowing companies. But the fun hipster alternative is, what if *venture capital*buys up every company and comes to dominate the economy? Historically no one worried about that much, because historically venture capital was about making concentrated bets on small startups that might change the world, not about buying the local pest-control company or medical practice in every town in America. But that’s changing. We have talked a few times about “AI rollups,” where a venture capital firm buys a bunch of small companies, combines them, and sprinkles them with artificial intelligence."
    },
    {
      "id": 2,
      "chunk": "One way to think about it is that each of PE and VC has a powerful general-purpose technology that it can apply indiscriminately to every company. PE’s magic technology is leverage: You buy the local plumber or pest control company or medical practice, you put a lot of non-recourse debt on it, you get a lot of upside if it does well and limited downside if it does poorly. VC’s magic technology is artificial intelligence: You buy the local plumber or pest control company or medical practice, you replace the customer-service reps and bookkeepers with AI agents, you cut costs and improve profits, and *eventually* you also replace the plumbers and exterminators and doctors with AI and then you really start to make money."
    },
    {
      "id": 3,
      "chunk": "Here’s a Financial Times story about AI rollups:\n\n> Top venture capital firms are borrowing a strategy from the private equity playbook, pumping money into tech start-ups so they can “roll up” rivals to build a sector-dominating conglomerate. ...\n>\n> The approach mirrors the strategies long deployed by private equity investors, which have built behemoths in fragmented industries such as healthcare, waste management or building services by agglomerating smaller businesses and centralising operating costs.\n>\n> It marks a new direction for VCs, which traditionally target fast-growing technology start-ups in nascent industries. The roll-up strategy creates an avenue for VCs to generate liquidity from their portfolios at a time when initial public offerings and dealmaking have slowed.\n>\n> Where private equity firms typically make heavy use of debt and slash costs in a roll-up, VCs claim improvements to efficiency and margins will come from infusing technology into the companies.\n>\n> [Thrive Capital-backed wealth startup] Savvy, for instance, is using AI to take on back office tasks such as pulling data for the half a dozen forms that might be needed for any one transaction."
    }
  ]
}


```